#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import get_db
from app.models.curriculum import Assessment, Question, Curriculum
from app.models.user import User

def create_test_assessment():
    """Create a test assessment with ID 2"""
    db = next(get_db())
    
    try:
        # Check if assessment 2 exists
        existing = db.query(Assessment).filter(Assessment.id == 2).first()
        if existing:
            print("Assessment 2 already exists")
            return
        
        # Get or create a test user
        user = db.query(User).first()
        if not user:
            print("No users found. Please create a user first.")
            return
        
        # Get or create a test curriculum
        curriculum = db.query(Curriculum).first()
        if not curriculum:
            curriculum = Curriculum(
                title="Test Curriculum",
                description="Test curriculum for assessment",
                subject="Python Programming",
                grade_level="Beginner",
                user_id=user.id,
                source_content="Test content"
            )
            db.add(curriculum)
            db.commit()
            db.refresh(curriculum)
        
        # Create assessment with ID 2
        assessment = Assessment(
            id=2,
            title="Python Fundamentals Quiz",
            description="Test your knowledge of Python basics",
            curriculum_id=curriculum.id,
            assessment_type="quiz",
            total_points=50,
            time_limit=30
        )
        
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        
        # Create test questions
        questions = [
            Question(
                assessment_id=2,
                question_text="What is the correct way to create a list in Python?",
                question_type="multiple_choice",
                options=["list = []", "list = ()", "list = {}", "list = \"\""],
                correct_answer="list = []",
                points=5
            ),
            Question(
                assessment_id=2,
                question_text="Which keyword is used to define a function in Python?",
                question_type="multiple_choice", 
                options=["function", "def", "define", "func"],
                correct_answer="def",
                points=5
            )
        ]
        
        for question in questions:
            db.add(question)
        
        db.commit()
        print("Test assessment 2 created successfully")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_assessment()