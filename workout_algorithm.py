from typing import Dict, List
from dataclasses import dataclass
import numpy as np

# Define UserProfile structure locally instead of importing
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

@dataclass
class ExerciseMetrics:
    difficulty: float
    effectiveness: float
    user_rating: float
    completion_rate: float

class WorkoutOptimizer:
    def __init__(self):
        self.exercise_metrics = {}
        self.user_progress = {}
        self.performance_thresholds = {
            'beginner': {'low': 0.3, 'high': 0.7},
            'intermediate': {'low': 0.5, 'high': 0.8},
            'advanced': {'low': 0.7, 'high': 0.9}
        }

    def _calculate_performance(self, history: List[Dict]) -> float:
        """Calculate user performance score based on workout history"""
        if not history:
            return 0.5  # Default middle performance for new users
        
        recent_workouts = history[-5:]  # Look at last 5 workouts
        scores = []
        
        for workout in recent_workouts:
            completion_rate = workout.get('exercises_completed', 0) / workout.get('total_exercises', 1)
            form_score = workout.get('form_score', 0.5)
            intensity_adherence = workout.get('intensity_adherence', 0.5)
            
            workout_score = (completion_rate * 0.4 + 
                           form_score * 0.4 + 
                           intensity_adherence * 0.2)
            scores.append(workout_score)
        
        return np.mean(scores) if scores else 0.5

    def _determine_adaptation_rate(self, performance_score: float) -> float:
        """Determine how quickly to progress the workout difficulty"""
        if performance_score > 0.8:
            return 0.1  # Fast progression
        elif performance_score > 0.6:
            return 0.05  # Moderate progression
        else:
            return 0.02  # Slow progression

    def _adjust_intensity(self, adaptation_rate: float) -> Dict:
        """Adjust workout intensity based on adaptation rate"""
        return {
            'resistance': min(0.9, 0.6 + adaptation_rate),
            'tempo': 'moderate' if adaptation_rate < 0.05 else 'fast',
            'rest_reduction': adaptation_rate * 100  # seconds to reduce rest
        }

    def _adjust_volume(self, performance_score: float) -> Dict:
        """Adjust workout volume based on performance"""
        base_sets = 3
        base_reps = 10
        
        if performance_score > 0.8:
            sets_adjustment = 1
            reps_adjustment = 2
        elif performance_score > 0.6:
            sets_adjustment = 0
            reps_adjustment = 1
        else:
            sets_adjustment = -1
            reps_adjustment = -2
            
        return {
            'sets': max(2, base_sets + sets_adjustment),
            'reps': max(6, base_reps + reps_adjustment)
        }

    def optimize_workout(self, user_profile: UserProfile, history: List[Dict]) -> Dict:
        """Generate optimized workout based on user profile and history"""
        performance_score = self._calculate_performance(history)
        adaptation_rate = self._determine_adaptation_rate(performance_score)
        
        # Generate weekly schedule
        weekly_schedule = self._create_weekly_schedule(user_profile)
        
        return {
            'daily_calories': self._calculate_daily_calories(user_profile),
            'macros': self._calculate_macros(user_profile, self._calculate_daily_calories(user_profile)),
            'intensity': self._adjust_intensity(adaptation_rate),
            'volume': self._adjust_volume(performance_score),
            'weekly_schedule': weekly_schedule,
            'rest_periods': 60 + (1 - performance_score) * 60,
            'hydration': self._calculate_hydration(user_profile)
        }

    def _create_weekly_schedule(self, user_profile: UserProfile) -> Dict:
        """Create a weekly workout schedule based on user's experience level"""
        schedule = {
            'Monday': {'type': 'strength', 'exercises': self._select_exercises(user_profile)},
            'Tuesday': {'type': 'cardio', 'exercises': self._get_cardio_exercises(user_profile)},
            'Wednesday': {'type': 'rest', 'exercises': []},
            'Thursday': {'type': 'strength', 'exercises': self._select_exercises(user_profile)},
            'Friday': {'type': 'cardio', 'exercises': self._get_cardio_exercises(user_profile)},
            'Saturday': {'type': 'strength', 'exercises': self._select_exercises(user_profile)},
            'Sunday': {'type': 'rest', 'exercises': []}
        }
        return schedule

    def _get_cardio_exercises(self, user_profile: UserProfile) -> List[Dict]:
        """Select cardio exercises based on user's level"""
        cardio_exercises = {
            'beginner': [
                {'name': 'Walking', 'duration': '30 mins', 'intensity': 'moderate'},
                {'name': 'Stationary Bike', 'duration': '20 mins', 'intensity': 'low'},
                {'name': 'Elliptical', 'duration': '15 mins', 'intensity': 'moderate'}
            ],
            'intermediate': [
                {'name': 'Jogging', 'duration': '30 mins', 'intensity': 'moderate'},
                {'name': 'Jump Rope', 'duration': '15 mins', 'intensity': 'high'},
                {'name': 'Swimming', 'duration': '30 mins', 'intensity': 'moderate'}
            ],
            'advanced': [
                {'name': 'HIIT Training', 'duration': '25 mins', 'intensity': 'high'},
                {'name': 'Sprinting Intervals', 'duration': '20 mins', 'intensity': 'high'},
                {'name': 'Boxing', 'duration': '30 mins', 'intensity': 'high'}
            ]
        }
        return cardio_exercises.get(user_profile.experience_level, cardio_exercises['beginner'])

    def _calculate_daily_calories(self, user_profile: UserProfile) -> int:
        """Calculate daily caloric needs"""
        # Harris-Benedict BMR formula
        if user_profile.gender.lower() == 'male':
            bmr = 88.362 + (13.397 * user_profile.weight) + (4.799 * user_profile.height) - (5.677 * user_profile.age)
        else:
            bmr = 447.593 + (9.247 * user_profile.weight) + (3.098 * user_profile.height) - (4.330 * user_profile.age)
        
        activity_multipliers = {
            'sedentary': 1.2,
            'moderate': 1.55,
            'active': 1.725
        }
        
        return int(bmr * activity_multipliers.get(user_profile.activity_level, 1.2))

    def _calculate_macros(self, user_profile: UserProfile, daily_calories: int) -> Dict:
        """Calculate macro nutrient distribution"""
        macro_ratios = {
            'weight_loss': {'protein': 0.4, 'carbs': 0.3, 'fats': 0.3},
            'muscle_gain': {'protein': 0.3, 'carbs': 0.5, 'fats': 0.2},
            'endurance': {'protein': 0.25, 'carbs': 0.55, 'fats': 0.2}
        }
        
        ratios = macro_ratios.get(user_profile.goal, macro_ratios['weight_loss'])
        return {
            'protein': int((daily_calories * ratios['protein']) / 4),
            'carbs': int((daily_calories * ratios['carbs']) / 4),
            'fats': int((daily_calories * ratios['fats']) / 9)
        }

    def _calculate_hydration(self, user_profile: UserProfile) -> Dict:
        """Calculate daily hydration needs"""
        base_water = user_profile.weight * 0.033  # 33ml per kg of body weight
        
        return {
            'daily_total_ml': int(base_water * 1000),  # Convert to ml
            'recommendations': [
                "Drink 500ml of water upon waking",
                "Drink 250ml 30 minutes before each meal",
                "Drink 500ml during workout",
                "Sip remaining amount throughout the day"
            ]
        }

    def _select_exercises(self, user_profile: UserProfile) -> List[Dict]:
        """Select appropriate exercises based on user profile"""
        exercises = {
            'beginner': [
                {'name': 'Bodyweight Squats', 'sets': 3, 'reps': '10-12'},
                {'name': 'Push-ups', 'sets': 3, 'reps': '8-10'},
                {'name': 'Walking Lunges', 'sets': 2, 'reps': '10 each leg'}
            ],
            'intermediate': [
                {'name': 'Barbell Squats', 'sets': 4, 'reps': '8-10'},
                {'name': 'Bench Press', 'sets': 4, 'reps': '8-10'},
                {'name': 'Romanian Deadlifts', 'sets': 3, 'reps': '10-12'}
            ],
            'advanced': [
                {'name': 'Front Squats', 'sets': 5, 'reps': '5-8'},
                {'name': 'Weighted Pull-ups', 'sets': 4, 'reps': '6-8'},
                {'name': 'Clean and Press', 'sets': 4, 'reps': '6-8'}
            ]
        }
        
        return exercises.get(user_profile.experience_level, exercises['beginner'])