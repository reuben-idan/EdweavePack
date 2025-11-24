#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, SessionLocal
from app.models.user import User
from app.schemas.auth import UserCreate
from app.api.auth import get_password_hash
from sqlalchemy import text
import traceback

def test_database_connection():
    """Test database connection"""
    try:
        print("Testing database connection...")
        db = SessionLocal()
        result = db.execute(text("SELECT 1")).fetchone()
        print(f"✓ Database connection successful: {result}")
        db.close()
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        traceback.print_exc()
        return False

def test_user_creation():
    """Test user creation directly"""
    try:
        print("\nTesting user creation...")
        
        # Test data
        user_data = {
            "email": "debug@test.com",
            "full_name": "Debug User",
            "password": "testpassword123",
            "institution": "Test Institution",
            "role": "teacher"
        }
        
        db = SessionLocal()
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data["email"]).first()
        if existing_user:
            print(f"User already exists, deleting: {existing_user.email}")
            db.delete(existing_user)
            db.commit()
        
        # Create new user
        hashed_password = get_password_hash(user_data["password"])
        
        db_user = User(
            email=user_data["email"],
            name=user_data["full_name"],
            hashed_password=hashed_password,
            institution=user_data["institution"],
            role=user_data["role"],
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        print(f"✓ User created successfully: {db_user.id}, {db_user.email}")
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ User creation failed: {e}")
        traceback.print_exc()
        if 'db' in locals():
            db.rollback()
            db.close()
        return False

def test_password_hashing():
    """Test password hashing"""
    try:
        print("\nTesting password hashing...")
        password = "testpassword123"
        hashed = get_password_hash(password)
        print(f"✓ Password hashing successful: {len(hashed)} chars")
        return True
    except Exception as e:
        print(f"✗ Password hashing failed: {e}")
        traceback.print_exc()
        return False

def check_database_tables():
    """Check if database tables exist"""
    try:
        print("\nChecking database tables...")
        db = SessionLocal()
        
        # Check if users table exists
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")).fetchone()
        if result:
            print("✓ Users table exists")
            
            # Check table structure
            columns = db.execute(text("PRAGMA table_info(users)")).fetchall()
            print("Table columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
        else:
            print("✗ Users table does not exist")
            
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Table check failed: {e}")
        traceback.print_exc()
        return False

def create_tables():
    """Create database tables"""
    try:
        print("\nCreating database tables...")
        from app.models import Base
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created successfully")
        return True
    except Exception as e:
        print(f"✗ Table creation failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== EdweavePack Registration Debug ===")
    
    # Run all tests
    tests = [
        test_database_connection,
        check_database_tables,
        create_tables,
        test_password_hashing,
        test_user_creation
    ]
    
    for test in tests:
        try:
            success = test()
            if not success:
                print(f"\n❌ Test {test.__name__} failed - stopping here")
                break
        except Exception as e:
            print(f"\n❌ Test {test.__name__} crashed: {e}")
            traceback.print_exc()
            break
    
    print("\n=== Debug Complete ===")