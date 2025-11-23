#!/usr/bin/env python3
"""
Comprehensive fix for registration issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base, SessionLocal
from app.models.user import User
from app.schemas.auth import UserCreate
from passlib.context import CryptContext
import traceback

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def fix_database_schema():
    """Fix database schema issues"""
    try:
        print("[INFO] Creating all database tables...")
        Base.metadata.create_all(bind=engine)
        print("[SUCCESS] Database tables created successfully!")
        
        # Verify tables exist
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"[INFO] Created tables: {tables}")
        
        if 'users' in tables:
            columns = inspector.get_columns('users')
            print("[INFO] Users table structure:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Database schema fix failed: {e}")
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        return False

def test_user_creation():
    """Test user creation with all required fields"""
    db = SessionLocal()
    
    try:
        print("[TEST] Testing user creation...")
        
        # Clean up any existing test user
        existing_user = db.query(User).filter(User.email == "test@edweavepack.com").first()
        if existing_user:
            print("[INFO] Removing existing test user...")
            db.delete(existing_user)
            db.commit()
        
        # Create test user with all fields
        hashed_password = pwd_context.hash("testpassword123")
        
        test_user = User(
            email="test@edweavepack.com",
            name="Test User",
            hashed_password=hashed_password,
            institution="Test University",
            role="teacher",
            is_active=True
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"[SUCCESS] Test user created successfully!")
        print(f"  - ID: {test_user.id}")
        print(f"  - Email: {test_user.email}")
        print(f"  - Name: {test_user.name}")
        print(f"  - Institution: {test_user.institution}")
        print(f"  - Role: {test_user.role}")
        print(f"  - Active: {test_user.is_active}")
        
        # Test password verification
        is_valid = pwd_context.verify("testpassword123", test_user.hashed_password)
        print(f"  - Password verification: {'PASS' if is_valid else 'FAIL'}")
        
        # Clean up
        db.delete(test_user)
        db.commit()
        print("[INFO] Test user cleaned up")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] User creation test failed: {e}")
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        db.rollback()
        return False
        
    finally:
        db.close()

def test_registration_data():
    """Test registration with sample data"""
    
    sample_data = {
        "email": "newuser@edweavepack.com",
        "full_name": "New User",
        "password": "securepassword123",
        "institution": "Sample University",
        "role": "teacher"
    }
    
    print(f"[TEST] Testing registration with data: {sample_data}")
    
    try:
        # Validate UserCreate schema
        user_create = UserCreate(**sample_data)
        print(f"[SUCCESS] UserCreate schema validation passed")
        print(f"  - Email: {user_create.email}")
        print(f"  - Full Name: {user_create.full_name}")
        print(f"  - Institution: {user_create.institution}")
        print(f"  - Role: {user_create.role}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Registration data test failed: {e}")
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")
        return False

def main():
    """Run all fixes and tests"""
    
    print("=" * 60)
    print("EdweavePack Registration Fix Script")
    print("=" * 60)
    
    success = True
    
    # Fix 1: Database Schema
    print("\n1. Fixing Database Schema...")
    if not fix_database_schema():
        success = False
    
    # Fix 2: Test User Creation
    print("\n2. Testing User Creation...")
    if not test_user_creation():
        success = False
    
    # Fix 3: Test Registration Data
    print("\n3. Testing Registration Data...")
    if not test_registration_data():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("[SUCCESS] All registration fixes completed successfully!")
        print("Registration should now work properly.")
    else:
        print("[ERROR] Some fixes failed. Check the output above.")
    print("=" * 60)

if __name__ == "__main__":
    main()