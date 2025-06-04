import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class ProgressVisualizer:
    def create_progress_dashboard(self, user_data: Optional[Dict] = None) -> Dict:
        """Create visualization dashboard for user progress"""
        # Initialize default data if none provided
        if user_data is None:
            user_data = self._create_default_data()

        figures = {}
        
        # Workout Progress Chart
        figures['workout'] = self._create_workout_chart(user_data)
        
        # Body Composition Chart
        figures['body'] = self._create_body_composition_chart(user_data)
        
        return figures

    def _create_default_data(self) -> Dict:
        """Create default data structure for new users"""
        today = datetime.now()
        dates = [(today - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(7)]
        
        return {
            'dates': dates,
            'workout_scores': [0] * 7,  # Initialize with zeros
            'weight': [0] * 7,
            'muscle_mass': [0] * 7,
            'body_fat': [0] * 7
        }

    def _create_workout_chart(self, user_data: Dict) -> go.Figure:
        """Create workout progress chart"""
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=user_data['dates'],
                y=user_data['workout_scores'],
                mode='lines+markers',
                name='Workout Performance'
            )
        )
        fig.update_layout(
            title='Workout Progress',
            xaxis_title='Date',
            yaxis_title='Performance Score',
            showlegend=True
        )
        return fig

    def _create_body_composition_chart(self, user_data: Dict) -> go.Figure:
        """Create body composition progress chart"""
        fig = px.line(
            user_data,
            x='dates',
            y=['weight', 'muscle_mass', 'body_fat'],
            title='Body Composition Progress'
        )
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Measurements',
            showlegend=True
        )
        return fig