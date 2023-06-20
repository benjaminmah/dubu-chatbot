# Demo 🎥
Click below to watch the demo! ⬇️

[![Watch the video](https://img.youtube.com/vi/aZ_y1hcKdSA/maxresdefault.jpg)](https://www.youtube.com/watch?v=aZ_y1hcKdSA)

# Purpose 🧠
Unique and simple customer service chatbot creation full-stack application tailored to any business! Businesses can upload files about information regarding their company, mix and match chatbot tones, and start experimenting with their own chatbot.

The name "dubu" comes from 두부, the Korean word for tofu. Tofu is seen as a base for countless recipes around the world and can be customized with an assortment of ingredients. Likewise, Dubu Chatbot is able to be customized with different ingredients (tones) and read from a secret recipe (any PDF file of your choice). Dubu Chatbot will communicate with you in the selected combination of ingredients and only answer questions pertaining to the secret recipe to ensure the reliability of your virtual customer service representative.

All elements (front-end and back-end) were created by Benjamin Mah.

# Features 🤩
‣ Select up to 8 different chatbot ingredients/tones, ranging from Professional to Playful\
‣ Mix and match any ingredient/tones, and feel free to add your own by editing index.html and ingredients.py\
‣ Upload any PDF file of your choice, it will be automatically parsed, embedded by OpenAI's ada-002 embedding model, and stored on a vector database\
‣ Ask any question (can be both related and unrelated to the document), your question will be semantically matched to a chunk\
‣ Your question and the chunk will be passed through OpenAI's GPT-3.5 completion model for accurate answers\
‣ Return to the main page or clear the chat at any time with the easy-to-use UI

# How to Use 📄
1. Clone this repo
2. Install dependencies by running $pip install -r requirements.txt in your virtual environment (note: dependency installation may be a bit different for Windows OS)
3. Paste your OpenAI API key into the .env file
4. Run $python app.py in your environment
5. On any browser, go to http://127.0.0.1:5000
6. Have fun!

