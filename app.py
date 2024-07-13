from flask import Flask, request, jsonify
import requests
import openai

app = Flask(__name__)

# Configure OpenAI API key
openai.api_key = 'your_openai_api_key'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    user_message = data['message']
    
    # Process message with Rasa
    rasa_response = process_with_rasa(user_message)
    
    # If Rasa can't handle, fallback to OpenAI
    if rasa_response is None:
        response = process_with_openai(user_message)
    else:
        response = rasa_response

    return jsonify({'response': response})

def process_with_rasa(message):
    rasa_url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {"sender": "user", "message": message}
    response = requests.post(rasa_url, json=payload)
    
    if response.status_code == 200 and response.json():
        return response.json()[0].get('text')
    return None

def process_with_openai(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        max_tokens=150
    )
    return response.choices[0].text.strip()

if __name__ == '__main__':
    app.run(port=5000)
