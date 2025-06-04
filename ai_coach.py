import numpy as np
from gtts import gTTS
import os
import cv2

class AICoach:
    def __init__(self):
        self.feedback_history = []
        self.feedback_messages = {
            'squat_depth': [
                "Lower your squat. Aim for thighs parallel to ground.",
                "Perfect squat depth! Keep it up!",
                "You're going too low. Control your descent."
            ],
            'knee_alignment': [
                "Keep your knees aligned with your toes.",
                "Watch your knees - they're caving inward.",
                "Great knee position!"
            ],
            'back_posture': [
                "Keep your back straight.",
                "Chest up, core engaged.",
                "Excellent posture!"
            ],
            'general': [
                "Remember to breathe.",
                "Keep your movements controlled.",
                "Maintain good form throughout."
            ]
        }
        self.last_feedback_time = 0
        self.feedback_cooldown = 3  # seconds between feedback

    def analyze_form(self, angles, positions, current_time):
        """
        Analyze squat form and provide feedback
        """
        if current_time - self.last_feedback_time < self.feedback_cooldown:
            return []

        feedback = []
        hip_angle = angles.get('hip_angle', 0)
        knee_angle = angles.get('knee_angle', 0)
        
        # Analyze form and generate feedback
        if hip_angle < 90:
            feedback.append(self.feedback_messages['squat_depth'][0])
        elif knee_angle < 150:
            feedback.append(self.feedback_messages['knee_alignment'][0])

        if feedback:
            self.last_feedback_time = current_time
            self.feedback_history.append(feedback[0])
        
        return feedback

    def get_session_summary(self):
        """
        Generate a summary of the training session
        """
        return {
            'total_feedback': len(self.feedback_history),
            'common_issues': self._get_common_issues(),
            'feedback_history': self.feedback_history
        }

    def _get_common_issues(self):
        """
        Identify most common form issues
        """
        if not self.feedback_history:
            return []
        
        from collections import Counter
        return Counter(self.feedback_history).most_common(3)