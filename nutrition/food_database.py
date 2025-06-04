from sqlalchemy import create_engine, text, Table, Column, Integer, Float, String, MetaData
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from typing import List, Dict
import logging

class NutritionDatabase:
    def __init__(self):
        self.engine = create_engine('sqlite:///nutrition.db')
        self.metadata = MetaData()
        self._initialize_database()
    
    def _initialize_database(self):
        try:
            # Define the table structure
            food_items = Table(
                'food_items', 
                self.metadata,
                Column('id', Integer, primary_key=True),
                Column('name', String),
                Column('calories', Float),
                Column('protein', Float),
                Column('carbs', Float),
                Column('fats', Float),
                Column('category', String)
            )
            
            # Create the table
            self.metadata.create_all(self.engine)
            
            # Add some sample data if table is empty
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM food_items"))
                count = result.scalar()
                
                if count == 0:
                    sample_data = [
                        {'name': 'Chicken Breast', 'calories': 165, 'protein': 31, 'carbs': 0, 'fats': 3.6, 'category': 'protein'},
                        {'name': 'Brown Rice', 'calories': 216, 'protein': 4.5, 'carbs': 45, 'fats': 1.8, 'category': 'carbs'},
                        {'name': 'Salmon', 'calories': 208, 'protein': 22, 'carbs': 0, 'fats': 13, 'category': 'protein'},
                        {'name': 'Sweet Potato', 'calories': 103, 'protein': 2, 'carbs': 24, 'fats': 0, 'category': 'carbs'}
                    ]
                    
                    conn.execute(
                        food_items.insert(),
                        sample_data
                    )
                    conn.commit()
                    
        except SQLAlchemyError as e:
            logging.error(f"Database initialization failed: {str(e)}")
            raise
    
    def get_meal_suggestions(self, calories: float, macros: Dict) -> List[Dict]:
        try:
            query = text("""
                SELECT * FROM food_items 
                WHERE calories <= :cal_limit 
                AND protein >= :protein_min
                ORDER BY protein DESC
            """)
            
            with self.engine.connect() as conn:
                result = conn.execute(
                    query, 
                    {"cal_limit": calories * 0.4, "protein_min": macros['protein'] * 0.2}
                )
                return [dict(row) for row in result]
                
        except SQLAlchemyError as e:
            logging.error(f"Query failed: {str(e)}")
            return []