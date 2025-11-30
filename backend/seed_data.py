#!/usr/bin/env python3
"""Seed database with test data"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from datetime import datetime

# Add app to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.user import User
from app.models.curriculum import Curriculum, Assessment
from app.core.database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_seed_data():
    """Create seed data for testing"""
    
    # Get database URL
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL not set")
        sys.exit(1)
    
    # Create engine and session
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create test users
        users_data = [
            {
                "email": "teacher1@edweavepack.com",
                "name": "Alice Johnson",
                "hashed_password": pwd_context.hash("password123"),
                "institution": "Demo High School",
                "role": "teacher"
            },
            {
                "email": "teacher2@edweavepack.com", 
                "name": "Bob Smith",
                "hashed_password": pwd_context.hash("password123"),
                "institution": "Demo Elementary",
                "role": "teacher"
            },
            {
                "email": "admin@edweavepack.com",
                "name": "Admin User",
                "hashed_password": pwd_context.hash("admin123"),
                "institution": "EdweavePack",
                "role": "admin"
            }
        ]
        
        created_users = []
        for user_data in users_data:
            # Check if user exists
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing:
                user = User(**user_data)
                db.add(user)
                db.flush()
                created_users.append(user)
                print(f"Created user: {user.email}")
            else:
                created_users.append(existing)
                print(f"User exists: {existing.email}")
        
        # Create test curricula
        curricula_data = [
            {
                "title": "Introduction to Python Programming",
                "subject": "Computer Science",
                "grade_level": "9-12",
                "description": "Learn Python basics with AI-powered curriculum",
                "content_data": {
                    "modules": [
                        {"title": "Variables and Data Types", "duration": "2 hours"},
                        {"title": "Control Structures", "duration": "3 hours"},
                        {"title": "Functions", "duration": "2 hours"}
                    ]
                },
                "ai_generated": True,
                "amazon_q_powered": True,
                "created_by": created_users[0].id,
                "status": "active"
            },
            {
                "title": "Algebra Fundamentals",
                "subject": "Mathematics", 
                "grade_level": "8-9",
                "description": "Master algebraic concepts with interactive content",
                "content_data": {
                    "modules": [
                        {"title": "Linear Equations", "duration": "4 hours"},
                        {"title": "Quadratic Functions", "duration": "5 hours"},
                        {"title": "Systems of Equations", "duration": "3 hours"}
                    ]
                },
                "ai_generated": True,
                "amazon_q_powered": True,
                "created_by": created_users[1].id,
                "status": "active"
            },
            {
                "title": "Cell Biology Basics",
                "subject": "Biology",
                "grade_level": "10-11", 
                "description": "Explore cellular structures and functions",
                "content_data": {
                    "modules": [
                        {"title": "Cell Structure", "duration": "3 hours"},
                        {"title": "Cell Division", "duration": "2 hours"},
                        {"title": "Cellular Respiration", "duration": "4 hours"}
                    ]
                },
                "ai_generated": True,
                "amazon_q_powered": True,
                "created_by": created_users[0].id,
                "status": "active"
            }
        ]
        
        created_curricula = []
        for curriculum_data in curricula_data:
            curriculum = Curriculum(**curriculum_data)
            db.add(curriculum)
            db.flush()
            created_curricula.append(curriculum)
            print(f"Created curriculum: {curriculum.title}")
        
        # Create test assessments
        assessments_data = [
            {
                "title": "Python Basics Quiz",
                "curriculum_id": created_curricula[0].id,
                "assessment_data": {
                    "questions": [
                        {
                            "question": "What is a variable in Python?",
                            "type": "multiple_choice",
                            "options": ["A container for data", "A function", "A loop", "A class"],
                            "correct": 0
                        },
                        {
                            "question": "Which keyword is used to define a function?",
                            "type": "multiple_choice", 
                            "options": ["func", "def", "function", "define"],
                            "correct": 1
                        }
                    ]
                },
                "total_points": 100,
                "time_limit": 30,
                "ai_generated": True,
                "created_by": created_users[0].id
            },
            {
                "title": "Algebra Assessment",
                "curriculum_id": created_curricula[1].id,
                "assessment_data": {
                    "questions": [
                        {
                            "question": "Solve for x: 2x + 5 = 15",
                            "type": "short_answer",
                            "correct": "5"
                        },
                        {
                            "question": "What is the slope of y = 3x + 2?",
                            "type": "short_answer",
                            "correct": "3"
                        }
                    ]
                },
                "total_points": 100,
                "time_limit": 45,
                "ai_generated": True,
                "created_by": created_users[1].id
            }
        ]
        
        for assessment_data in assessments_data:
            assessment = Assessment(**assessment_data)
            db.add(assessment)
            print(f"Created assessment: {assessment.title}")
        
        # Commit all changes
        db.commit()
        
        # Verify data
        user_count = db.query(User).count()
        curriculum_count = db.query(Curriculum).count()
        assessment_count = db.query(Assessment).count()
        
        print(f"\n✅ Seed data created successfully:")
        print(f"   Users: {user_count}")
        print(f"   Curricula: {curriculum_count}")
        print(f"   Assessments: {assessment_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Seed data creation failed: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = create_seed_data()
    sys.exit(0 if success else 1)