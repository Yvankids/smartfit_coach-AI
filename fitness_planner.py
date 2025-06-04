import numpy as np
from dataclasses import dataclass
from typing import List, Dict
import json
import datetime

@dataclass
class UserProfile:
    age: int
    weight: float
    height: float
    gender: str
    goal: str
    diet_preference: str
    activity_level: str
    restrictions: List[str]

class FitnessPlanner:
    def __init__(self):
        self.workout_types = {
            'weight_loss': {
                'cardio_ratio': 0.6,
                'strength_ratio': 0.4,
                'intensity': 'moderate to high'
            },
            'muscle_gain': {
                'cardio_ratio': 0.2,
                'strength_ratio': 0.8,
                'intensity': 'high'
            },
            'endurance': {
                'cardio_ratio': 0.7,
                'strength_ratio': 0.3,
                'intensity': 'moderate'
            }
        }
        
        self.performance_history = []
        
        self.exercise_database = {
            'strength': {
                'weight_loss': [
                    {'name': 'Squats', 'sets': 3, 'reps': '12-15', 'rest': '60s'},
                    {'name': 'Push-ups', 'sets': 3, 'reps': '10-12', 'rest': '60s'},
                    {'name': 'Lunges', 'sets': 3, 'reps': '12 each leg', 'rest': '45s'},
                    {'name': 'Plank', 'sets': 3, 'reps': '30-45s hold', 'rest': '30s'}
                ],
                'muscle_gain': [
                    {'name': 'Squats', 'sets': 4, 'reps': '8-10', 'rest': '90s'},
                    {'name': 'Push-ups', 'sets': 4, 'reps': '8-10', 'rest': '90s'},
                    {'name': 'Dumbbell Rows', 'sets': 4, 'reps': '8-10', 'rest': '90s'},
                    {'name': 'Core Work', 'sets': 3, 'reps': '12-15', 'rest': '60s'}
                ],
                'endurance': [
                    {'name': 'Circuit Training', 'sets': 3, 'reps': '15-20', 'rest': '30s'},
                    {'name': 'Bodyweight Exercises', 'sets': 3, 'reps': '15-20', 'rest': '30s'},
                    {'name': 'High-Rep Squats', 'sets': 3, 'reps': '15-20', 'rest': '30s'}
                ]
            },
            'cardio': {
                'weight_loss': [
                    {'name': 'HIIT Intervals', 'duration': '20 mins', 'intensity': 'high'},
                    {'name': 'Jump Rope', 'duration': '10 mins', 'intensity': 'moderate'},
                    {'name': 'Burpees', 'duration': '10 mins', 'intensity': 'high'}
                ],
                'muscle_gain': [
                    {'name': 'Light Jogging', 'duration': '15 mins', 'intensity': 'low'},
                    {'name': 'Stair Climbing', 'duration': '10 mins', 'intensity': 'moderate'}
                ],
                'endurance': [
                    {'name': 'Running', 'duration': '30 mins', 'intensity': 'moderate'},
                    {'name': 'Cycling', 'duration': '45 mins', 'intensity': 'moderate'},
                    {'name': 'Swimming', 'duration': '30 mins', 'intensity': 'moderate'}
                ]
            }
        }
        
        self.hydration_factors = {
            'sedentary': 30,
            'moderate': 35,
            'active': 40
        }

    def generate_workout_plan(self, user: UserProfile) -> Dict:
        base_plan = self.workout_types[user.goal]
        
        workout_plan = {
            'weekly_schedule': self._create_weekly_schedule(user, base_plan),
            'daily_calories': self._calculate_daily_calories(user),
            'macros': self._calculate_macros(user),
            'hydration': self._calculate_hydration(user)
        }
        
        return workout_plan
    
    def _get_exercises(self, workout_type: str, user: UserProfile) -> List[Dict]:
        """
        Get exercises based on workout type and user goals
        """
        try:
            exercises = self.exercise_database[workout_type][user.goal]
            return exercises
        except KeyError:
            return []
    
    def _create_weekly_schedule(self, user: UserProfile, base_plan: Dict) -> Dict:
        """
        Create a weekly workout schedule based on user profile and base plan
        """
        schedule = {
            'Monday': {'type': 'strength', 'exercises': self._get_exercises('strength', user)},
            'Tuesday': {'type': 'cardio', 'exercises': self._get_exercises('cardio', user)},
            'Wednesday': {'type': 'rest', 'exercises': []},
            'Thursday': {'type': 'strength', 'exercises': self._get_exercises('strength', user)},
            'Friday': {'type': 'cardio', 'exercises': self._get_exercises('cardio', user)},
            'Saturday': {'type': 'strength', 'exercises': self._get_exercises('strength', user)},
            'Sunday': {'type': 'rest', 'exercises': []}
        }
        return schedule
    
    def _calculate_daily_calories(self, user: UserProfile) -> int:
        # Basic BMR calculation using Harris-Benedict equation
        if user.gender.lower() == 'male':
            bmr = 88.362 + (13.397 * user.weight) + (4.799 * user.height) - (5.677 * user.age)
        else:
            bmr = 447.593 + (9.247 * user.weight) + (3.098 * user.height) - (4.330 * user.age)
            
        activity_multipliers = {
            'sedentary': 1.2,
            'moderate': 1.55,
            'active': 1.725
        }
        
        return int(bmr * activity_multipliers[user.activity_level])
    
    def _calculate_macros(self, user: UserProfile) -> Dict:
        """Calculate macro nutrients based on user's goals and daily calories"""
        daily_calories = self._calculate_daily_calories(user)
        
        # Define macro ratios based on goals
        macro_ratios = {
            'weight_loss': {
                'protein': 0.40,  # 40% protein
                'carbs': 0.35,    # 35% carbs
                'fats': 0.25      # 25% fats
            },
            'muscle_gain': {
                'protein': 0.30,  # 30% protein
                'carbs': 0.50,    # 50% carbs
                'fats': 0.20      # 20% fats
            },
            'endurance': {
                'protein': 0.25,  # 25% protein
                'carbs': 0.55,    # 55% carbs
                'fats': 0.20      # 20% fats
            }
        }
        
        # Get ratios for user's goal (default to weight_loss if goal not found)
        ratios = macro_ratios.get(user.goal, macro_ratios['weight_loss'])
        
        # Calculate macros in grams
        macros = {
            'protein': int((daily_calories * ratios['protein']) / 4),  # 4 calories per gram
            'carbs': int((daily_calories * ratios['carbs']) / 4),     # 4 calories per gram
            'fats': int((daily_calories * ratios['fats']) / 9)        # 9 calories per gram
        }
        
        return macros
    
    def _calculate_hydration(self, user: UserProfile) -> Dict:
        """
        Calculate daily hydration needs based on:
        - Weight
        - Activity level
        - Climate (default to moderate)
        Returns daily water intake in ml and recommended drinking schedule
        """
        # Base calculation: weight in kg * activity factor (ml)
        base_hydration = user.weight * self.hydration_factors[user.activity_level]
        
        # Add exercise adjustment
        if user.goal in ['endurance', 'weight_loss']:
            base_hydration += 500  # Extra 500ml for high activity goals
        
        schedule = {
            'daily_total_ml': int(base_hydration),
            'hourly_target_ml': int(base_hydration / 16),  # Assuming 16 waking hours
            'recommendations': [
                "Drink 500ml of water upon waking",
                "Drink 250ml 30 minutes before each meal",
                "Drink 500ml during each workout",
                "Sip remaining amount throughout the day"
            ]
        }
        
        return schedule