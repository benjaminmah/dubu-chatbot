import chromadb
from chromadb.config import Settings
from typing import Dict

class ChromaDataStore:
    def __init__(self, embedding_function):
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            persist_directory='/Users/benjaminmah/Documents/GITHUB/dubu-chatbot/datastore',
        ))
        self.collection = None
        self.embedding_function = embedding_function
    
    def add_collection(self, collection_name=None):
        if collection_name:
            self.collection = self.client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function,
                get_or_create=True,
            )

            print(f"Collection created. Details: \n Name: {self.collection.name}", flush=True)
        
    def remove_collection(self, collection_name=None):
        if collection_name:
            self.client.delete_collection(collection_name)
            print(f"Deleted collection {collection_name}", flush=True)

    def reset_collection(self, collection_name=None):
        if collection_name:
            self.remove_collection(collection_name)
            self.add_collection(collection_name)
    
    def upsert(self, documents, collection_name=None):
        if collection_name:
            self.collection.add(
                documents=[doc.page_content for doc in documents],
                metadatas=[doc.metadata for doc in documents],
                ids=[str(doc.metadata.get("id")) for doc in documents]
            )
    
    def query(self, texts, num_results=1, embeddings=None, collection_name=None) -> Dict:
        results = self.collection.query(query_texts=texts, n_results=num_results, query_embeddings=embeddings)

        results["ids"] = (
            results.get("ids")[0] if results.get("ids") != None else None
        )
        results["embeddings"] = (
            results.get("embeddings")[0] if results.get("embeddings") != None else None
        )
        results["documents"] = (
            results.get("documents")[0] if results.get("documents") != None else None
        )
        results["metadatas"] = (
            results.get("metadatas")[0] if results.get("metadatas") != None else None
        )
        results["distances"] = (
            results.get("distances")[0] if results.get("distances") != None else None
        )

        return results
    
    def delete_everything(self):
        self.client.reset()
        

    
