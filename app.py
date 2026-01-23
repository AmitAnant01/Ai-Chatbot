import streamlit as st
import requests
import time  # Added for typing animation

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="Advanced AI Chatbot",
    page_icon="",
    layout="wide"
)

# CUSTOM CSS 
st.markdown("""
<style>
body {
    background-color: #0f1117;
    color: #eaeaea;
}

.main {
    background-color: #0f1117;
}

.chat-bubble-user {
    background: linear-gradient(135deg, #4f46e5, #3b82f6);
    color: white;
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 10px;
    width: fit-content;
    max-width: 75%;
}

.chat-bubble-ai {
    background-color: #1e1e2e;
    color: #eaeaea;
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 10px;
    width: fit-content;
    max-width: 75%;
    border: 1px solid #2a2a40;
}

.input-container {
    position: fixed;
    bottom: 10px;
    width: 90%;
    display: flex;
    justify-content: center;
}
input, button {
    padding: 10px;
    border-radius: 10px;
    border: none;
    outline: none;
}

input {
    flex: 1;
    margin-right: 10px;
}

button {
    background-color: #4f46e5;
    color: white;
    cursor: pointer;
}
}
</style>
""", unsafe_allow_html=True)


if st.button("Clear Chat"):
        st.session_state.history = []


st.markdown("## 🤖 Advanced AI Chatbot")
st.caption("Note: This will provide info up to October 2023 only.")

 
if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='chat-bubble-user'><b>You:</b><br>{msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-bubble-ai'><b>AI:</b><br>{msg['content']}</div>",
            unsafe_allow_html=True
        )

# ------------------ INPUT ------------------
user_input = st.chat_input("Ask anything...")

if user_input:
    st.session_state.history.append(
        {"role": "user", "content": user_input}
    )

    try:
        res = requests.post(
            API_URL,
            json={
                "message": user_input,
                "history": st.session_state.history,
                
            },
            timeout=60
        )

        if res.status_code == 200:
            full_reply = res.json()["reply"]
        else:
            full_reply = "Backend error. Check FastAPI terminal."

    except Exception as e:
        full_reply = f"Request failed: {e}"

    
    placeholder = st.empty()  # temporary container for typing effect
    typed_text = ""
    for char in full_reply:
        typed_text += char
        placeholder.markdown(
            f"<div class='chat-bubble-ai'><b>AI:</b><br>{typed_text}</div>",
            unsafe_allow_html=True
        )
        time.sleep(0.02)  # adjust typing speed here

    st.session_state.history.append(
        {"role": "assistant", "content": full_reply}
    )

    st.rerun()
