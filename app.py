from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

GEMINI_API_KEY = "API_Key"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_Key}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_input = request.form.get("msg")

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_input}
                ]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(GEMINI_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        try:
            bot_reply = data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            bot_reply = "Sorry, I couldn't understand the response."
    else:
        bot_reply = f"Error: {response.status_code}"

    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
