import streamlit as st
from pathlib import Path

def load_css():
    css_file = Path(__file__).parent.parent / "static/styles.css"
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def page_header(title, subtitle=None):
    st.markdown(f"""
        <div class="main-header">
            <h1>{title}</h1>
            {f"<p>{subtitle}</p>" if subtitle else ""}
        </div>
    """, unsafe_allow_html=True)

def metric_card(label, value, delta=None):
    st.markdown(f"""
        <div class="card">
            <div class="metric-container">
                <h3>{label}</h3>
                <h2>{value}</h2>
                {f"<p>{delta}</p>" if delta else ""}
            </div>
        </div>
    """, unsafe_allow_html=True)