import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Get API Key from Environment Variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def chat_with_gpt(user_input):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)  # Create OpenAI client
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an instructional coach helping teachers with classroom strategies."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content  # Correct OpenAI API format

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "Missing message"}), 400

    response = chat_with_gpt(user_input)
    return jsonify({"response": response})

@app.route("/")
def home():
    return "Chatbot is running! Send a POST request to /chat."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render’s assigned port
    print(f"🔥 Chatbot is starting on port {port}...")  # Debug message
    app.run(host="0.0.0.0", port=port, debug=True)

