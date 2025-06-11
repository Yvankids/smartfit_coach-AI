import streamlit as st
from database.db_handler import DatabaseHandler
import hashlib
from datetime import datetime
import time
import requests

# Must be the first Streamlit command
st.set_page_config(
    page_title="SmartFit Coach - Login",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide sidebar and other elements before login
st.markdown("""
<style>
    /* Hide sidebar completely */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    /* Hide hamburger menu */
    button[kind="header"] {
        display: none !important;
    }
    /* Hide main menu and footer */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
</style>
""", unsafe_allow_html=True)

# Clear any existing session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def main():
    st.title("🏋️ SmartFit Coach")
    st.subheader("Welcome to your AI Fitness Companion")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                if username and password:
                    db = DatabaseHandler()
                    if db.verify_user(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("Login successful!")
                        st.switch_page("pages/1_🏠️_Demo.py")
                    else:
                        st.error("Invalid credentials")
                else:
                    st.warning("Please fill in all fields")

    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Choose Username")
            new_password = st.text_input("Choose Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            register = st.form_submit_button("Register")

            if register:
                if not all([new_username, new_password, confirm_password]):
                    st.warning("Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    db = DatabaseHandler()
                    if db.create_user(new_username, new_password):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Username already exists")

if __name__ == "__main__":
    main()