import streamlit as st
from database.db_handler import DatabaseHandler

# Must be first Streamlit command
st.set_page_config(
    page_title="SmartFit Coach - Dashboard",
    page_icon="🏋️",
    layout="wide"
)

# Authentication check
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    # Hide sidebar for unauthenticated users
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
    st.switch_page("Login.py")

# Show sidebar with logout option for authenticated users
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.session_state.username = None
    st.switch_page("Login.py")