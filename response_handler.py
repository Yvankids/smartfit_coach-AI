from typing import List, Dict
import re
from datetime import datetime

class ResponseHandler:
    def __init__(self):
        self.context = {
            'current_topic': None,
            'user_level': 'beginner',
            'last_query_time': None,
            'query_count': 0,
            'topics_discussed': set()
        }
        self.conversation_history = []
        self.response_templates = self._initialize_templates()

    def _initialize_templates(self) -> Dict:
        return {
            'workout_plan': {
                'default': "Here's a personalized workout plan:\n\n{details}",
                'beginner': self._get_beginner_template(),
                'advanced': self._get_advanced_template()
            },
            'nutrition': {
                'default': "Nutrition advice:\n\n{details}",
                'meal_plan': self._get_meal_plan_template()
            }
        }

    def process_query(self, query: str, chat_bot) -> str:
        # Track conversation
        self.conversation_history.append(query)
        
        # Analyze intent
        intent = self._determine_intent(query)
        
        # Get personalized response
        response = self._generate_response(intent, query, chat_bot)
        
        # Update context
        self._update_context(query, intent)
        
        return response
    
    def _determine_intent(self, query: str) -> str:
        intents = {
            'workout_plan': r'(workout|exercise|training) (plan|program|routine)',
            'nutrition': r'(food|diet|nutrition|eat|macro)',
            'form_check': r'(form|technique|how to)',
            'progress': r'(progress|improvement|gains)',
            'injury': r'(pain|injury|hurt|sore)'
        }
        
        for intent, pattern in intents.items():
            if re.search(pattern, query, re.IGNORECASE):
                return intent
        return 'general'

    def _generate_response(self, intent: str, query: str, chat_bot) -> str:
        """Generate contextual response based on intent and query"""
        # Get basic template
        template = self.response_templates.get(intent, {}).get('default')
        
        if not template:
            return self._get_fallback_response()

        # Extract specific details based on intent
        if intent == 'workout_plan':
            details = self._get_workout_details(query, chat_bot)
        elif intent == 'nutrition':
            details = self._get_nutrition_details(query, chat_bot)
        elif intent == 'form_check':
            details = self._get_form_details(query, chat_bot)
        else:
            details = self._get_general_details(query, chat_bot)

        # Format response with details
        response = template.format(
            details=details,
            exercise=self._extract_exercise(query),
            time=datetime.now().strftime("%H:%M")
        )

        return response

    def _get_workout_details(self, query: str, chat_bot) -> str:
        """Extract workout-specific details from chatbot"""
        if 'beginner' in query.lower():
            return chat_bot.knowledge_base['workout_types']['strength']['beginner']
        elif 'cardio' in query.lower():
            return chat_bot.knowledge_base['workout_types']['cardio']['beginner']
        return chat_bot.knowledge_base['workout_types']['strength']['beginner']

    def _get_nutrition_details(self, query: str, chat_bot) -> str:
        """Extract nutrition-specific details from chatbot"""
        if 'macro' in query.lower():
            return chat_bot.knowledge_base['nutrition']['macros']
        elif 'meal' in query.lower():
            return chat_bot.knowledge_base['nutrition']['meal_timing']
        return chat_bot.knowledge_base['nutrition']['general']

    def _get_form_details(self, query: str, chat_bot) -> str:
        """Extract form guidance details from chatbot"""
        exercise = self._extract_exercise(query)
        return chat_bot.knowledge_base['form_guidance'].get(exercise, 
            chat_bot.knowledge_base['form_guidance']['squat'])

    def _get_general_details(self, query: str, chat_bot) -> str:
        """Get general response when no specific intent is matched"""
        return ("I can help you with workout plans, nutrition advice, and form checks. "
                "What would you like to know more about?")

    def _extract_exercise(self, query: str) -> str:
        """Extract exercise name from query"""
        exercises = ['squat', 'deadlift', 'bench press', 'push up']
        for exercise in exercises:
            if exercise in query.lower():
                return exercise
        return 'squat'  # default exercise

    def _get_fallback_response(self) -> str:
        """Provide fallback response when intent is not recognized"""
        return ("I'm not sure I understand. I can help you with:\n"
                "- Workout planning\n"
                "- Nutrition advice\n"
                "- Form checks\n"
                "- Progress tracking\n"
                "Please try asking about one of these topics!")

    def _get_beginner_template(self) -> str:
        return """# Beginner Workout Plan 🏋️‍♂️

## Week 1-4 Foundation
- 3 workouts per week
- Rest day between sessions
- Focus on form and technique

### Workout A
1. **Bodyweight Squats**: 3x10
2. **Push-ups** (modified if needed): 3x8
3. **Walking Lunges**: 2x10 each leg
4. **Plank Hold**: 3x20 seconds

### Workout B
1. **Glute Bridges**: 3x12
2. **Wall Push-ups**: 3x10
3. **Bird Dogs**: 2x10 each side
4. **Superman Holds**: 3x15 seconds

## Tips
- Warm up for 5-10 minutes
- Stay hydrated
- Rest 60-90 seconds between sets"""

    def _get_advanced_template(self) -> str:
        return """# Advanced Training Program 💪

## 5-Day Split
### Day 1: Push
- **Bench Press**: 4x8-10
- **Overhead Press**: 4x8-10
- **Incline DB Press**: 3x10-12
- **Lateral Raises**: 3x12-15

### Day 2: Pull
- **Barbell Rows**: 4x8-10
- **Pull-ups**: 4x8-10
- **Face Pulls**: 3x12-15
- **Bicep Curls**: 3x10-12

### Day 3: Legs
- **Squats**: 5x5
- **Romanian Deadlifts**: 4x8-10
- **Bulgarian Split Squats**: 3x12
- **Calf Raises**: 4x15-20"""

    def _get_meal_plan_template(self) -> str:
        return """# Daily Meal Plan 🥗

## Pre-Workout
- Oatmeal with banana
- Greek yogurt
- Coffee or green tea

## Post-Workout
- Protein shake
- Sweet potato
- Grilled chicken breast

## Evening Meal
- Salmon or lean beef
- Brown rice
- Mixed vegetables
- Healthy fats (avocado/nuts)

## Supplements
- Whey protein
- Creatine monohydrate
- Multivitamin"""

    def _update_context(self, query: str, intent: str) -> None:
        """Update conversation context based on user query and intent"""
        current_time = datetime.now()
        
        # Update basic context
        self.context.update({
            'current_topic': intent,
            'last_query_time': current_time,
            'query_count': self.context['query_count'] + 1
        })
        
        # Add topic to discussed set
        self.context['topics_discussed'].add(intent)
        
        # Update user level based on query complexity
        if any(term in query.lower() for term in ['advanced', 'professional', 'expert']):
            self.context['user_level'] = 'advanced'
        elif any(term in query.lower() for term in ['intermediate', 'experienced']):
            self.context['user_level'] = 'intermediate'
        
        # Trim conversation history if too long
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]