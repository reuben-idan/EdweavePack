#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test imports first
try:
    print("Testing imports...")
    from app.core.database import get_db
    print("OK Database import OK")
    
    from app.models.user import User
    print("OK User model import OK")
    
    from app.schemas.auth import UserCreate
    print("OK UserCreate schema import OK")
    
    from app.api.auth import get_password_hash
    print("OK Password hash function import OK")
    
except Exception as e:
    print(f"Import error: {e}")
    import traceback
    print(traceback.format_exc())
    exit(1)

# Test registration logic directly
def test_registration_logic():
    print("\nTesting registration logic...")
    
    try:
        # Get database session
        db = next(get_db())
        
        # Test data
        user_data = UserCreate(
            email="test@example.com",
            full_name="Test User",
            password="testpassword123",
            institution="Test Institution",
            role="teacher"
        )
        
        print(f"User data: {user_data}")
        
        # Clean email
        email = user_data.email.strip().lower()
        print(f"Cleaned email: {email}")
        
        # Check existing user
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print("Deleting existing user...")
            db.delete(existing_user)
            db.commit()
        
        # Create user
        print("Creating user...")
        db_user = User(
            email=email,
            name=user_data.full_name.strip(),
            hashed_password=get_password_hash(user_data.password),
            institution=user_data.institution or "Not specified",
            role=user_data.role or "teacher",
            is_active=True
        )
        
        print(f"User object created: {db_user}")
        
        db.add(db_user)
        print("User added to session")
        
        db.commit()
        print("Changes committed")
        
        db.refresh(db_user)
        print(f"User created with ID: {db_user.id}")
        
        # Clean up
        db.delete(db_user)
        db.commit()
        print("Test user cleaned up")
        
        print("OK Registration logic test PASSED")
        
    except Exception as e:
        print(f"Registration logic error: {e}")
        import traceback
        print(traceback.format_exc())
        if 'db' in locals():
            db.rollback()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    test_registration_logic()