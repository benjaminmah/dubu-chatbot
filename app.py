import os
import openai

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from datastore.chroma_datastore import ChromaDataStore
from utils.embeddings_function import OpenAIEmbeddingFunction
from utils.file_processing import *
from utils.doc_splitter import DocSplitter
from utils.ingredients import Ingredients
from transformers import GPT2Tokenizer


# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv('OPENAI_KEY')

# Set the OpenAI API key
openai.api_key = api_key

app = Flask(__name__)

# Set up OpenAI credentials
# openai.api_key = 'YOUR_OPENAI_API_KEY'

@app.route('/')
def index():
    ingredients.reset_ingredients()
    if datastore.collection != None:
        datastore.remove_collection('test')
    return render_template('index.html')

@app.route('/new-page')
def new_page():
    return render_template('new-page.html')

@app.route('/start-cooking', methods=['POST'])
def start_cooking():
    ingredients.reset_ingredients()
    if datastore.collection != None:
        datastore.remove_collection('test')
        
    selected_ingredients = request.form.get('selectedIngredients')
    file = request.files.get('file')

    # Process the selected ingredients and file here
    print(selected_ingredients)
    
    selected_ingredients_list = list(selected_ingredients.split(','))
    if file:
        # Save the file or perform other operations
        file.save('/Users/benjaminmah/Documents/GITHUB/dubu-chatbot/files/user-file.pdf')

    
    # split pdf, upsert to db
    docs = get_documents_from_file('/Users/benjaminmah/Documents/GITHUB/dubu-chatbot/files/user-file.pdf')
    docs = doc_splitter.split_documents(docs)
    docs = doc_splitter.doc_renum_id(docs, "doc")

    print(f"Collection will be named: {COLLECTION_NAME}")

    datastore.add_collection(COLLECTION_NAME)
    datastore.upsert(docs, COLLECTION_NAME)

    ingredients.add_ingredients(selected_ingredients_list)
    ingredients.create_string()

    return {'message': 'Cooking started'}

@app.route('/pass-user-message', methods=['POST'])
def pass_user_message():
    user_message = request.json.get('message')
    chat_history = request.json.get('chatMessages')
    # Generate a response using OpenAI
    response = generate_response(user_message, chat_history)

    return jsonify({'answer': response})

def generate_response(user_message, chat_history):
    query_results = datastore.query(user_message, num_results=1, embeddings=None, collection_name='test')
    docs = query_results.get("documents")
    context = docs[0]
    response = generate_answer(user_message, context, chat_history)
    return response

def generate_answer(user_message, context, chat_history):
    user_prompt = f"CONTEXT: {context}\nQUERY: {user_message}\nANSWER:"
    response = get_completion(user_prompt, chat_history)
    return response

def get_completion(user_prompt, chat_history):
    print(f"\n\nINGREDIENTS >> {ingredients.ingredients}\n\n")
    # Determine the number of messages to extract from chat history (max 4 -> user, assistant, user, assistant)
    num_messages = min(len(chat_history), 4)
    messages_to_pass = chat_history[-num_messages:]

    print(f"\n\n STRING INGREDIENTS {ingredients.string_ingredients}\n\n")
    system_message = f"""You are a customer service bot. You are to only ANSWER the QUERY using the provided CONTEXT and chat history. If the ANSWER is not found in the CONTEXT or chat history, the ANSWER is "I don't know". Your tone should be{ingredients.string_ingredients} You must abide by this tone."""
    system_content = {"role": "system", "content": system_message}

    messages_to_pass.insert(0, system_content)

    messages_to_pass.append({"role": "user", "content": user_prompt})
    # Clean up line breaks from the user message content
    for message in messages_to_pass:
        if message['role'] == 'user':
            message['content'] = message['content'].replace("\n", "")

    print(f"\n\n MESSAGES TO SEND TO BOT >> {messages_to_pass}\n\n")
    

    response = openai.ChatCompletion.create(
        model=ENGINE_NAME, messages=messages_to_pass, temperature=0,
    )
    # except:
    #     return "An error occured while retrieving completion"
    
    message_content = response["choices"][0]["message"]["content"]

    return message_content

if __name__ == '__main__':
    print("Initializing embedding function...")
    embeddings_func = OpenAIEmbeddingFunction()
    print("Initializing datastore...")
    datastore = ChromaDataStore(
        embeddings_func
    )
    print("Initializing tokenizer...")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    print("Initializing docsplitter...")
    doc_splitter = DocSplitter(tokenizer, 200, 50)
    print("Resetting datastore...")
    datastore.delete_everything()
    print("Initializing ingredients...")
    ingredients = Ingredients()
    print("Removing old files...")
    if os.path.exists('/Users/benjaminmah/Documents/GITHUB/dubu-chatbot/files/user-file.pdf'):
        os.remove('/Users/benjaminmah/Documents/GITHUB/dubu-chatbot/files/user-file.pdf')

    COLLECTION_NAME = "test"
    ENGINE_NAME = "gpt-3.5-turbo"
    app.run()
