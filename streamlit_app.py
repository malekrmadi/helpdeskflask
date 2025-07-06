import streamlit as st
import requests

st.set_page_config(page_title="Gemini Chat", page_icon="🤖")
st.title("🤖 Gemini AI Assistant")

# URL du backend Flask
BACKEND_URL = "http://localhost:5000/chat"

if "history" not in st.session_state:
    st.session_state.history = []

def add_message(role: str, content: str):
    st.session_state.history.append({"role": role, "content": content})

# Zone de saisie utilisateur
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Vous :", "")
    submitted = st.form_submit_button("Envoyer")
    if submitted and user_input.strip():
        add_message("user", user_input)

        try:
            res = requests.post(BACKEND_URL, json={"message": user_input}, timeout=30)
            if res.ok:
                assistant_reply = res.json().get("response", "")
            else:
                assistant_reply = f"Erreur backend {res.status_code}"
        except requests.exceptions.RequestException as exc:
            assistant_reply = f"Échec de la requête : {exc}"

        add_message("assistant", assistant_reply)

# Affiche l’historique de la conversation
for msg in st.session_state.history:
    role = "👤 Vous" if msg["role"] == "user" else "🤖 Assistant"
    st.markdown(f"**{role} :** {msg['content']}")

st.markdown("---")
st.markdown("ℹ️ Clé API Gemini requise (variable d’environnement `GEMINI_API_KEY`).")
