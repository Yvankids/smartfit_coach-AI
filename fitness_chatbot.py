import streamlit as st
import random
import time
from typing import Dict, List, Optional
import json
import re

class FitnessChat:
    def __init__(self):
        self.responses = {
            'squat_form': [
                "For proper squat form:\n- Keep your feet shoulder-width apart\n- Keep your back straight\n- Lower until thighs are parallel to ground\n- Keep knees aligned with toes",
                "Common squat mistakes to avoid:\n- Knees caving in\n- Rounding your back\n- Not going deep enough\n- Rising too quickly"
            ],
            'workout_advice': [
                "I recommend:\n- 3 sets of 12-15 squats\n- Rest 60-90 seconds between sets\n- Focus on form over speed",
                "Start with bodyweight squats before adding weights. Master the form first!"
            ],
            'greeting': [
                "Hello! I'm your AI Fitness Coach. How can I help you today?",
                "Welcome! Ready to work on your fitness goals?"
            ],
            'default': [
                "I'm not sure about that. Try asking about squat form, workout advice, or common mistakes.",
                "Could you rephrase that? I'm best at helping with squat technique and training advice."
            ]
        }
        
        self.knowledge_base = {
            'workout_types': {
                'strength': self._get_strength_info(),
                'cardio': self._get_cardio_info(),
                'flexibility': self._get_flexibility_info(),
                'hiit': self._get_hiit_info()
            },
            'nutrition': {
                'macros': self._get_macro_info(),
                'meal_timing': self._get_meal_timing_info(),
                'supplements': self._get_supplement_info(),
                'diets': self._get_diet_info()
            },
            'injury_prevention': self._get_injury_prevention_info(),
            'recovery': self._get_recovery_info(),
            'form_guidance': self._get_form_guidance()
        }

    def get_response(self, user_input: str) -> str:
        """Process user input and return relevant fitness advice"""
        # Normalize input
        user_input = user_input.lower().strip()
        
        # Check for specific question types
        if self._is_about_workout(user_input):
            return self._handle_workout_query(user_input)
        elif self._is_about_nutrition(user_input):
            return self._handle_nutrition_query(user_input)
        elif self._is_about_injury(user_input):
            return self._handle_injury_query(user_input)
        
        # Default response with suggestions
        return self._get_default_response()

    def _is_about_workout(self, query: str) -> bool:
        workout_keywords = [
            'workout', 'exercise', 'training', 'sets', 'reps',
            'cardio', 'strength', 'weight', 'muscle', 'gym'
        ]
        return any(keyword in query for keyword in workout_keywords)

    def _handle_workout_query(self, query: str) -> str:
        if 'beginner' in query:
            return self.knowledge_base['workout_types']['strength']['beginner']
        elif 'form' in query:
            return self.knowledge_base['form_guidance']['general']
        # Add more specific workout responses
        
    def _get_strength_info(self) -> Dict:
        return {
            'beginner': """Here's a beginner strength training guide:
1. Start with bodyweight exercises
2. Focus on form over weight
3. Recommended routine:
   - Push-ups: 3 sets of 8-12 reps
   - Squats: 3 sets of 12-15 reps
   - Planks: 3 sets of 30 seconds
4. Rest 60-90 seconds between sets""",
            'intermediate': "...",
            'advanced': "..."
        }

    def _get_cardio_info(self) -> Dict:
        return {
            'beginner': """Beginner Cardio Guide:
- Start with walking: 20-30 minutes, 3-4 times per week
- Gradually increase duration and intensity
- Target heart rate: 50-65% of max
- Include light jogging when comfortable
- Cool down with 5-minute walk""",
            'intermediate': """Intermediate Cardio Training:
- Mix of running, cycling, swimming
- 30-45 minutes per session
- Target heart rate: 65-75% of max
- Include interval training
- 4-5 sessions per week""",
            'advanced': """Advanced Cardio Programming:
- High-intensity intervals
- Complex cardio circuits
- 45-60 minute sessions
- Target heart rate: 75-85% of max
- Include sprint work"""
        }

    def _get_flexibility_info(self) -> Dict:
        return {
            'general': """Flexibility Training:
- Dynamic stretching before workouts
- Static stretching post-workout
- Hold stretches 15-30 seconds
- Focus on major muscle groups
- Include yoga or mobility work""",
            'routines': {
                'morning': "Light dynamic stretches\nSun salutations\nJoint mobility",
                'pre_workout': "Dynamic stretching\nMobility drills\nActivation exercises",
                'post_workout': "Static stretching\nFoam rolling\nCool-down routine"
            }
        }

    def _get_hiit_info(self) -> Dict:
        return {
            'basics': """HIIT Fundamentals:
- Work/rest ratio: 1:2 for beginners
- 20-30 minute sessions
- 2-3 times per week
- Include recovery days
- Progress gradually""",
            'workouts': {
                'beginner': "30s work / 60s rest x 8 rounds",
                'intermediate': "40s work / 40s rest x 10 rounds",
                'advanced': "45s work / 15s rest x 12 rounds"
            }
        }

    def _get_macro_info(self) -> Dict:
        return {
            'protein': "1.6-2.2g per kg body weight",
            'carbs': "3-7g per kg based on activity",
            'fats': "0.5-1.5g per kg body weight",
            'timing': "Protein every 3-4 hours\nCarbs around workouts"
        }

    def _get_meal_timing_info(self) -> Dict:
        return {
            'pre_workout': "2-3 hours before: Full meal\n30-60 mins before: Light snack",
            'post_workout': "Within 30 mins: Quick carbs + protein\n2 hours after: Full meal",
            'general': "Eat every 3-4 hours\nStay hydrated throughout day"
        }

    def _get_supplement_info(self) -> Dict:
        return {
            'basics': """Essential Supplements:
- Protein powder: 20-30g per serving
- Creatine: 5g daily
- Multivitamin: Daily with meal
- Fish oil: 1-2g EPA/DHA daily""",
            'advanced': "Pre-workout\nBCAAs\nBeta-alanine"
        }

    def _get_diet_info(self) -> Dict:
        return {
            'weight_loss': "Caloric deficit 20-25%\nHigh protein\nComplex carbs",
            'muscle_gain': "Caloric surplus 10-20%\nHigh protein\nTimed carbs",
            'maintenance': "Balanced macros\nWhole foods\nRegular meals"
        }

    def _get_injury_prevention_info(self) -> Dict:
        return {
            'warmup': "Dynamic stretching\nMobility work\nLight cardio",
            'recovery': "Rest days\nSleep 7-9 hours\nProper nutrition",
            'form': "Start light\nPerfect form\nGradual progression"
        }

    def _get_recovery_info(self) -> Dict:
        return {
            'methods': """Recovery Techniques:
- Sleep: 7-9 hours nightly
- Nutrition: Post-workout meal
- Hydration: 2.5-3.5L daily
- Active recovery: Light movement
- Stretching: Daily flexibility work""",
            'timing': "Rest 48h between muscle groups\nDeload every 4-6 weeks"
        }

    def _get_form_guidance(self) -> Dict:
        return {
            'squat': """Perfect Squat Form:
1. Feet shoulder-width apart
2. Toes slightly pointed out
3. Keep chest up
4. Push knees out as you descend
5. Go parallel or below
6. Drive through your heels""",
            'deadlift': "...",
            'bench_press': "..."
        }