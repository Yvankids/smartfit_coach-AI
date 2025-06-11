import streamlit as st
from functools import wraps

def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'authenticated' not in st.session_state or not st.session_state.authenticated:
            st.switch_page("Login.py")
        return func(*args, **kwargs)
    return wrapper