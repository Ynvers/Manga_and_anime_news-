import streamlit as st
from server import get_news  # Import the function from server.py

st.set_page_config(
    page_title="Anime & Manga News",
    page_icon="°",
    layout="centered",
)

st.title("🌸 Anime & Manga News")
st.write("Ask anything about the latest news in the world of anime and manga!")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for msg in st.session_state.chat_history:
    if msg['role'] == 'user':
        with st.chat_message("user"):
            st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            st.markdown(f'<div class="server-msg">{msg["content"]}</div>', unsafe_allow_html=True)


# User query input
query = st.chat_input(
    "Enter your question"
)

if query:
    # Add user query to chat history
    st.session_state.chat_history.append({'role': 'user', 'content': query})
    with st.spinner("Traitement de votre requête par Senk..."):
        news = get_news(query)
        # Add server response to chat history
        st.session_state.chat_history.append({'role': 'server', 'content': news})
        st.rerun()  # Rerun to update chat history display

st.markdown("""
    <style>
    body, .stApp {
        background-color: #111 !important;
    }
    .user-msg {
        background: #2563eb;
        color: #fff;
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 8px;
        max-width: 70%;
        align-self: flex-end;
    }
    .server-msg {
        background: #a21caf;
        color: #111;
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 8px;
        max-width: 70%;
        align-self: flex-start;
    }
    .stChatMessage {
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)
