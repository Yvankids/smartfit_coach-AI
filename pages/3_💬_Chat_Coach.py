import streamlit as st
from fitness_chatbot import FitnessChat
from response_handler import ResponseHandler

def init_chat():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = FitnessChat()
    if 'handler' not in st.session_state:
        st.session_state.handler = ResponseHandler()

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