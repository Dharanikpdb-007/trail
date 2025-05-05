import streamlit as st
import os
from chatbot import DogCareBot
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()
bot = DogCareBot(api_key)


# Set page config
st.set_page_config(
    page_title="Dog Pet Care Assistant",
    page_icon="🐕",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🐕 Dog Pet Care Assistant")
st.markdown("Your friendly assistant for all dog care questions and advice!")

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about dog care..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    response = bot.process_query(prompt)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Sidebar with help information
with st.sidebar:
    st.header("Available Commands")
    st.markdown("""
    - Type 'categories' to see all topics
    - Type 'help' for usage instructions
    - Ask about specific breeds
    - Ask about feeding, training, health, or grooming
    """)

    st.header("Example Questions")
    st.markdown("""
    - "How often should I feed my dog?"
    - "What's the best way to train a puppy?"
    - "Tell me about Labrador breed"
    - "How do I groom my dog properly?"
    """)
