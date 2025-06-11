import streamlit as st
from response_handler import FitnessAIAssistant

# Authentication check
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.switch_page("Login.py")

st.markdown("""
<style>
    .chat-container {
        max-width: 800px;
        margin: auto;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background: #E0E7FF;
        margin-left: 2rem;
    }
    .bot-message {
        background: #F3F4F6;
        margin-right: 2rem;
    }
    .suggestions {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    .suggestion-chip {
        background: #4F46E5;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

def init_chat():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "handler" not in st.session_state:
        st.session_state.handler = FitnessAIAssistant()
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = None

def main():
    st.title("SmartFit Coach AI Assistant")
    st.markdown("### Your 24/7 Fitness Guide")
    init_chat()
    
    # Chat interface
    st.markdown("### Chat with your AI Fitness Coach")
    st.markdown("Ask questions about squat form, workout advice, or training tips!")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    user_input = st.chat_input("Type your question here...")
    
    if user_input:
        # Add user message to chat
        st.chat_message("user").write(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Get AI response
        response = st.session_state.handler.process_query(
            user_input, 
            st.session_state.chatbot
        )
        
        # Display AI response
        with st.chat_message("assistant"):
            st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()