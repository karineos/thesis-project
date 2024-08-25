from flask import Flask, request, jsonify, render_template
from openai import AzureOpenAI

app = Flask(__name__)

# Initialize the Azure OpenAI client
client = AzureOpenAI(
     api_key="a284de3e1b2348b0b0151b2e67a63a5c",
    api_version="2024-02-01",
    azure_endpoint="https://thesisproject.openai.azure.com/"
)

# Initialize the conversation context with a more empathetic system message

# Initialize conversation with a greeting
conversation = [{"role": "system", "content": "Hi! How can I help you today?"}]

@app.route('/')
def index():
    return render_template('testing.html')  # Render the 'testing.html' file

@app.route('/process_message', methods=['POST'])
def process_message():
    global conversation  # Use global conversation variable

    data = request.get_json()
    user_message = data['message']

    # Add user's message to the conversation
    conversation.append({"role": "user", "content": user_message})

    # Call the get_route function with the conversation
    route = get_route(conversation)

    # Add the chatbot's response to the conversation
    conversation.append({"role": "system", "content": route})

    return jsonify(response=route)

def is_in_doha(location):
    # Implement your logic to check if the location is within Doha, Qatar
    # For simplicity, let's assume all locations are within Doha for this example
    return True

def get_route(conversation):
    # Check if both origin and destination are within Doha, Qatar
    if is_in_doha(conversation[0]["content"]) and is_in_doha(conversation[1]["content"]):
        # Use chat completion to get the route directions
       response = client.chat.completions.create(
        model="thesis",  # Use the deployment name you have set up in Azure
        messages=conversation
    )
       return response.choices[0].message.content.strip()
    else:
        return "Sorry, the origin or destination is not within Doha, Qatar."

if __name__ == '__main__':
    app.run(debug=True)
