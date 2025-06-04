import streamlit as st
from fitness_planner import FitnessPlanner, UserProfile
from nutrition_tracker import NutritionTracker
from datetime import datetime
from workout_algorithm import WorkoutOptimizer
from nutrition.food_database import NutritionDatabase
from ml_engine import FitnessML
from visualization import ProgressVisualizer
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class UserProfile:
    age: int
    weight: float
    height: float
    gender: str
    goal: str
    diet_preference: str
    activity_level: str
    experience_level: str

def display_workout_plan(plan: Dict):
    """Display the workout plan with all metrics"""
    st.header("🎯 Your Personalized Fitness Plan", divider="rainbow")
    
    # Create three columns for key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Daily Calories Target",
            value=f"{plan.get('daily_calories', 0)} kcal",
            delta="Recommended intake"
        )
    
    with col2:
        hydration = plan.get('hydration', {})
        st.metric(
            label="Water Intake",
            value=f"{hydration.get('daily_total_ml', 0)/1000:.1f} L",
            delta="Daily target"
        )
    
    with col3:
        st.metric(
            label="Active Days",
            value="5 days/week",
            delta="Recommended frequency"
        )

    # Macro Distribution
    st.subheader("📊 Macro Distribution")
    
    # Calculate macro percentages
    protein_pct = int(plan['macros']['protein']*4*100/plan['daily_calories'])
    carbs_pct = int(plan['macros']['carbs']*4*100/plan['daily_calories'])
    fats_pct = int(plan['macros']['fats']*9*100/plan['daily_calories'])
    
    # Display macros as progress bars
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🥩 Protein")
        st.progress(protein_pct/100)
        st.write(f"{protein_pct}% ({plan['macros']['protein']}g)")
        
    with col2:
        st.subheader("🌾 Carbs")
        st.progress(carbs_pct/100)
        st.write(f"{carbs_pct}% ({plan['macros']['carbs']}g)")
        
    with col3:
        st.subheader("🥑 Fats")
        st.progress(fats_pct/100)
        st.write(f"{fats_pct}% ({plan['macros']['fats']}g)")

    # Optional: Add pie chart for macro distribution
    import plotly.graph_objects as go
    
    fig = go.Figure(data=[go.Pie(
        labels=['Protein', 'Carbs', 'Fats'],
        values=[protein_pct, carbs_pct, fats_pct],
        hole=.3
    )])
    fig.update_layout(title_text="Macro Distribution")
    st.plotly_chart(fig)

    # Weekly Schedule Section
    st.subheader("📅 Weekly Workout Schedule")
    
    weekly_schedule = plan.get('weekly_schedule', {})
    if weekly_schedule:
        for day, workout in weekly_schedule.items():
            with st.expander(f"{day} - {workout['type'].title()}"):
                if workout['type'] != 'rest':
                    for exercise in workout['exercises']:
                        if workout['type'] == 'strength':
                            st.write(f"• {exercise['name']}")
                            st.write(f"  Sets: {exercise.get('sets', '-')}")
                            st.write(f"  Reps: {exercise.get('reps', '-')}")
                        else:  # cardio
                            st.write(f"• {exercise['name']}")
                            st.write(f"  Duration: {exercise.get('duration', '-')}")
                            st.write(f"  Intensity: {exercise.get('intensity', '-')}")
                else:
                    st.write("Rest & Recovery Day 🌟")
    else:
        st.warning("No weekly schedule available")

    # Hydration Guide
    st.subheader("💧 Hydration Guide")
    st.info(f"Daily Target: {plan['hydration']['daily_total_ml']/1000:.1f} liters")
    for rec in plan['hydration']['recommendations']:
        st.markdown(f"- {rec}")

def set_page_style():
    """Configure the page style and layout"""
    st.set_page_config(
        page_title="AI Fitness Planner",
        page_icon="💪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stMetricValue {
            font-size: 24px;
            color: #0088ff;
        }
        .stProgress {
            height: 20px;
        }
        .stProgress > div > div {
            background-color: #0088ff;
        }
        h1 {
            color: #1f1f1f;
        }
        .stAlert {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.title("SmartFit Coach Planner")
    st.subheader("Personalized Workout & Nutrition Plans")

    # Initialize advanced features
    optimizer = WorkoutOptimizer()
    nutrition_db = NutritionDatabase()
    ml_engine = FitnessML()
    visualizer = ProgressVisualizer()
    
    # Move form submission handling to a separate function
    def handle_form_submit(user_inputs):
        user = UserProfile(
            age=user_inputs['age'],
            weight=user_inputs['weight'],
            height=user_inputs['height'],
            gender=user_inputs['gender'],
            goal=user_inputs['goal'],
            diet_preference=user_inputs['diet'],
            activity_level=user_inputs['activity'],
            experience_level=user_inputs['experience']
        )
        
        planner = FitnessPlanner()
        return planner.generate_workout_plan(user)

    # User Profile Input Form
    with st.form("user_profile"):
        st.header("Your Profile")
        
        user_inputs = {
            'age': st.number_input("Age", 18, 100, 25),
            'weight': st.number_input("Weight (kg)", 30.0, 200.0, 70.0),
            'height': st.number_input("Height (cm)", 100.0, 250.0, 170.0),
            'gender': st.selectbox("Gender", ["Male", "Female", "Other"]),
            'goal': st.selectbox("Fitness Goal", ["weight_loss", "muscle_gain", "endurance"]),
            'diet': st.selectbox("Diet Preference", ["regular", "vegetarian", "vegan", "keto"]),
            'activity': st.selectbox("Activity Level", ["sedentary", "moderate", "active"]),
            'experience': st.selectbox("Experience Level", ["beginner", "intermediate", "advanced"])
        }
        
        submit = st.form_submit_button("Generate Plan")

    # Handle form submission and display results outside the form
    if submit:
        plan = handle_form_submit(user_inputs)
        if plan:
            display_workout_plan(plan)
            
            pdf_data = generate_pdf_report(plan)
            if pdf_data:
                st.download_button(
                    label="📥 Download Complete Plan (PDF)",
                    data=pdf_data,
                    file_name=f"fitness_plan_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    help="Download your personalized fitness plan as a PDF file"
                )
            else:
                st.error("Failed to generate PDF. Please try again.")

    # Add tabs for different features
    tab1, tab2, tab3 = st.tabs(["Workout Plan", "Nutrition", "Progress"])
    
    # Prepare dummy or placeholder variables for demonstration
    # Replace these with actual user/workout data as needed
    user_profile = None
    workout_history = None
    daily_calories = None
    macros = None
    user_data = None

    with tab1:
        # Only call if user_profile and workout_history are available
        if submit:
            user_profile = UserProfile(
                age=user_inputs['age'],
                weight=user_inputs['weight'],
                height=user_inputs['height'],
                gender=user_inputs['gender'],
                goal=user_inputs['goal'],
                diet_preference=user_inputs['diet'],
                activity_level=user_inputs['activity'],
                experience_level=user_inputs['experience']
            )
            workout_history = []  # Replace with actual workout history if available
            optimized_plan = optimizer.optimize_workout(user_profile, workout_history)
            display_workout_plan(optimized_plan)
        else:
            st.info("Please generate a plan to see your optimized workout.")

    with tab2:
        if submit:
            daily_calories = plan['daily_calories']
            macros = plan['macros']
            meal_suggestions = nutrition_db.get_meal_suggestions(daily_calories, macros)
            display_nutrition_plan(meal_suggestions)
        else:
            st.info("Please generate a plan to see nutrition suggestions.")

    with tab3:
        st.subheader("📊 Progress Tracking")
        
        # Initialize progress visualizer
        visualizer = ProgressVisualizer()
        
        # For new users, we'll show empty charts
        progress_charts = visualizer.create_progress_dashboard()
        
        # Display charts
        st.plotly_chart(progress_charts['workout'], use_container_width=True)
        st.plotly_chart(progress_charts['body'], use_container_width=True)
        
        # Add placeholder for future tracking
        st.info("Start tracking your progress to see your fitness journey!")
        
        # Add tracking button
        if st.button("Record Today's Progress"):
            st.session_state.show_tracking_form = True
            
        # Show tracking form
        if getattr(st.session_state, 'show_tracking_form', False):
            with st.form("progress_tracking"):
                st.number_input("Weight (kg)", min_value=0.0, step=0.1)
                st.number_input("Body Fat %", min_value=0.0, max_value=100.0, step=0.1)
                st.number_input("Workout Performance Score", min_value=0.0, max_value=10.0, step=0.1)
                submitted = st.form_submit_button("Save Progress")
                
                if submitted:
                    st.success("Progress recorded successfully!")
                    # Here you would save the data to your database

def display_nutrition_plan(meal_suggestions):
    """Display nutrition plan and meal suggestions."""
    st.header("🍽️ Nutrition Plan")
    for meal in meal_suggestions:
        st.subheader(meal.get('name', 'Meal'))
        st.write(f"Calories: {meal.get('calories', '-')}")
        st.write(f"Macros: {meal.get('macros', '-')}")
        st.write("Foods:")
        for food in meal.get('foods', []):
            st.markdown(f"- {food}")

def generate_pdf_report(plan: dict) -> bytes:
    """
    Placeholder function to generate a PDF report from the plan.
    Replace this with actual PDF generation logic as needed.
    """
    import io
    # For now, just return a simple PDF-like byte string
    buffer = io.BytesIO()
    buffer.write(b"%PDF-1.4\n%Fake PDF content for plan\n")
    buffer.seek(0)
    return buffer.read()

if __name__ == "__main__":
    main()