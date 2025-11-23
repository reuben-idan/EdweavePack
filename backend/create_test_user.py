#!/usr/bin/env python3

from app.core.database import SessionLocal, engine
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_user():
    """Create a test user for testing"""
    db = SessionLocal()
    
    try:
        # Check if user exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("Test user already exists")
            return
        
        # Create test user
        hashed_password = pwd_context.hash("testpassword")
        
        test_user = User(
            email="test@example.com",
            name="Test User",
            hashed_password=hashed_password,
            institution="Test Institution",
            role="teacher",
            is_active=True
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"Test user created: {test_user.email}")
        print(f"Password: testpassword")
        
    except Exception as e:
        print(f"Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()