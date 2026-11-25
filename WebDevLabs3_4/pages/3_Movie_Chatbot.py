
import asyncio
import os
import streamlit as st
from app_style import setup
from chat_logic import create_agent

setup("Movie Chatbot")
st.title("Let's talk movies.")
st.write("Discuss themes, animation, or what you enjoy watching.")


if "chat_bubbles" not in st.session_state:
    st.session_state.chat_bubbles = []
if "model_history" not in st.session_state:
    st.session_state.model_history = []
if st.sidebar.button("Clear conversation"):
    st.session_state.chat_bubbles = []
    st.session_state.model_history = []
    st.rerun()

try:
    api_key = st.secrets.get("GOOGLE_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")
    model_name = st.secrets.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
    api_key = os.getenv("GOOGLE_API_KEY", "")
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
ready = bool(api_key and api_key != "PASTE_YOUR_KEY_HERE")
if not ready:
    st.info("Add your Gemini API key to .streamlit/secrets.toml (or Streamlit Cloud Settings → Secrets) to enable chat. See README.md for setup.")
for message in st.session_state.chat_bubbles:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What kind of movies do you enjoy?", disabled=not ready, max_chars=4000)
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    try:
        
        async def get_reply():
            agent = create_agent(api_key, model_name)
            return await agent.run(prompt, message_history=st.session_state.model_history)
        with st.spinner("Thinking about cinema…"):
            result = asyncio.run(get_reply())
        
        st.session_state.model_history = result.all_messages()
        st.session_state.chat_bubbles.extend([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": result.output},
        ])
        with st.chat_message("assistant"):
            st.markdown(result.output)
    except Exception:
        
        st.error("Sorry, the chatbot could not respond. Please try again shortly. If this continues, check your Gemini key, quota, and model name. This message was not added to conversation memory.")
st.caption("Chat memory lasts for this browser session and is removed by Clear conversation. Messages are sent to Google Gemini.")
