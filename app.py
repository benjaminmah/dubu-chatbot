import os
import openai

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv


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
    return render_template('index.html')

@app.route('/new-page')
def new_page():
    return render_template('new-page.html')

@app.route('/start-cooking', methods=['POST'])
def start_cooking():
    selected_ingredients = request.form.get('selectedIngredients')
    file = request.files.get('file')

    # Process the selected ingredients and file here
    print(selected_ingredients)
    if file:
        # Save the file or perform other operations
        file.save('/Users/benjaminmah/Documents/GITHUB/dubu-chatbot/files/user-file.pdf')

    return {'message': 'Cooking started'}

@app.route('/pass-user-message', methods=['POST'])
def pass_user_message():
    user_message = request.json.get('message')
    chat_messages = request.json.get('chatMessages')
    # Generate a response using OpenAI
    response = generate_response(user_message)

    return jsonify({'answer': response})

def generate_response(user_message):
    # Use OpenAI to generate a response based on the user message
    # Replace this placeholder code with your actual OpenAI implementation
    # response = openai.Completion.create(
    #     engine='text-davinci-003',
    #     prompt=user_message,
    #     max_tokens=1000
    # )
    response = 'idk loool i gotta get this openai thing figured out'
    return response

if __name__ == '__main__':
    app.run()
