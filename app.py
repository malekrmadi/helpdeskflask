import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# Configure l'API Gemini avec ta clé
genai.configure(api_key=os.getenv("apikey"))

# Crée le modèle et la session de chat
model = genai.GenerativeModel("gemini-1.5-flash")
chat_session = model.start_chat(history=[])

app = Flask(__name__)
CORS(app)  # Autorise les appels depuis Streamlit (autre port)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "Champ 'message' requis"}), 400

    try:
        response = chat_session.send_message(user_message)
        assistant_reply = response.text
    except Exception as e:
        assistant_reply = f"Erreur : {e}"

    return jsonify({"response": assistant_reply})

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
