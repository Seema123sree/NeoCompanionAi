from flask import Flask, request, jsonify  
from transformers import pipeline  
from datetime import datetime, timedelta

app = Flask(name)

Load the Hugging Face AI model for emotionally supportive responses

chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

Temporary storage for user messages (this will reset if the server restarts)

user_messages = {}

Free plan limit

FREE_MESSAGE_LIMIT = 35

@app.route("/chat", methods=["POST"]) def chat(): data = request.json user_id = data.get("user_id")  # Unique identifier for users message = data.get("message") premium = data.get("premium", False)  # Check if the user is a premium user

if not user_id or not message:
    return jsonify({"error": "Missing user_id or message"}), 400

# Check message limits for free users
if not premium:
    if user_id not in user_messages:
        user_messages[user_id] = {"count": 0, "reset_time": datetime.now() + timedelta(days=1)}
    
    user_data = user_messages[user_id]
    
    # Reset counter if it's a new day
    if datetime.now() > user_data["reset_time"]:
        user_messages[user_id] = {"count": 0, "reset_time": datetime.now() + timedelta(days=1)}
    
    if user_messages[user_id]["count"] >= FREE_MESSAGE_LIMIT:
        return jsonify({"error": "Message limit reached. Upgrade to premium for unlimited messages."}), 403
    
    user_messages[user_id]["count"] += 1

# Generate AI response
response = chatbot(message, max_length=100, num_return_sequences=1)[0]['generated_text']
return jsonify({"response": response})

if name == "main": app.run(host="0.0.0.0", port=5000)

