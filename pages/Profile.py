import streamlit as st
import plotly.express as px
from PIL import Image
import io
from database.db_handler import DatabaseHandler

# Authentication check
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.switch_page("Login.py")

st.markdown("""
<style>
    .profile-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stats-card {
        background: linear-gradient(135deg, #4F46E5, #3B82F6);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .progress-container {
        margin-top: 2rem;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🎯 Profile & Progress")
    
    # Profile Section
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<div class='profile-container'>", unsafe_allow_html=True)
        profile_pic = st.file_uploader("Update Profile Picture", type=['jpg', 'png'])
        if profile_pic:
            image = Image.open(profile_pic)
            st.image(image, width=200)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        with st.form("profile_form"):
            full_name = st.text_input("Full Name")
            col_a, col_b = st.columns(2)
            with col_a:
                height = st.number_input("Height (cm)", min_value=0.0)
                current_weight = st.number_input("Current Weight (kg)", min_value=0.0)
            with col_b:
                target_weight = st.number_input("Target Weight (kg)", min_value=0.0)
                experience = st.selectbox("Experience Level", 
                    ["Beginner", "Intermediate", "Advanced"])
            
            fitness_goal = st.selectbox("Fitness Goal",
                ["Weight Loss", "Muscle Gain", "Endurance", "General Fitness"])
            
            if st.form_submit_button("Save Changes"):
                # Save profile changes to database
                pass
    
    # Progress Tracking
    st.markdown("### 📊 Progress Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["Weight Progress", "Workout Stats", "Form Analysis"])
    
    with tab1:
        # Sample data - replace with actual database data
        weight_data = {'date': ['2023-01-01', '2023-02-01', '2023-03-01'],
                      'weight': [80, 78, 75]}
        fig = px.line(weight_data, x='date', y='weight', 
                     title='Weight Progress Over Time')
        st.plotly_chart(fig)
    
    with tab2:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
                <div class='stats-card'>
                    <h3>Total Workouts</h3>
                    <h2>24</h2>
                </div>
                """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div class='stats-card'>
                    <h3>Avg. Duration</h3>
                    <h2>45 min</h2>
                </div>
                """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
                <div class='stats-card'>
                    <h3>Calories Burned</h3>
                    <h2>12,450</h2>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        # Form analysis progress chart
        form_data = {'exercise': ['Squats', 'Deadlifts', 'Pushups'],
                    'score': [85, 92, 78]}
        fig = px.bar(form_data, x='exercise', y='score',
                    title='Form Analysis Scores')
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()