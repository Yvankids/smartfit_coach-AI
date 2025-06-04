import streamlit as st


st.title('AI Fitness Trainer: Squats Analysis')


recorded_file = 'output_sample.mp4'
sample_vid = st.empty()
sample_vid.video(recorded_file)


st.sidebar.title("AI Coach Settings")
enable_audio = st.sidebar.checkbox("Enable Voice Feedback", value=False)
feedback_frequency = st.sidebar.slider("Feedback Frequency (seconds)", 1, 10, 3)







