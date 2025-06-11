import streamlit as st

def clear_session():
    """Clear sensitive session data"""
    keys_to_keep = {'authenticated', 'username'}
    for key in list(st.session_state.keys()):
        if key not in keys_to_keep:
            del st.session_state[key]

def logout():
    """Handle user logout"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.switch_page("Login.py")