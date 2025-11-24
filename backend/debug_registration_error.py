#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.database import get_db, engine
from app.models.user import User
from app.schemas.auth import UserCreate
from app.api.auth import get_password_hash
import traceback

def test_registration():
    """Test registration process step by step"""
    print("=== Registration Debug Test ===")
    
    # Test database connection
    try:
        print("1. Testing database connection...")
        db = next(get_db())
        result = db.execute(text("SELECT 1")).fetchone()
        print(f"   OK Database connection successful: {result}")
        
        # Check if users table exists
        print("2. Checking users table...")
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")).fetchone()
        if result:
            print("   OK Users table exists")
        else:
            print("   ERROR Users table does not exist")
            return
            
        # Check table structure
        print("3. Checking table structure...")
        result = db.execute(text("PRAGMA table_info(users)")).fetchall()
        print(f"   Table columns: {[row[1] for row in result]}")
        
    except Exception as e:
        print(f"   ERROR Database error: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return
    
    # Test user creation
    try:
        print("4. Testing user creation...")
        
        test_email = "test@example.com"
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == test_email).first()
        if existing_user:
            print(f"   Deleting existing test user: {test_email}")
            db.delete(existing_user)
            db.commit()
        
        # Create test user
        test_user = User(
            email=test_email,
            name="Test User",
            hashed_password=get_password_hash("testpassword123"),
            institution="Test Institution",
            role="teacher",
            is_active=True
        )
        
        print(f"   Creating user: {test_user.email}")
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"   OK User created successfully with ID: {test_user.id}")
        
        # Clean up
        db.delete(test_user)
        db.commit()
        print("   OK Test user cleaned up")
        
    except Exception as e:
        print(f"   ERROR User creation error: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        db.rollback()
    
    finally:
        db.close()

if __name__ == "__main__":
    test_registration()