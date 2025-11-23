#!/usr/bin/env python3
"""
Debug script to check database connection and table structure
"""

from app.core.database import engine, SessionLocal
from app.models.user import User
from sqlalchemy import inspect, text
import traceback

def debug_database():
    """Debug database connection and structure"""
    
    try:
        print("[DEBUG] Debugging database connection...")
        
        # Test basic connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("[SUCCESS] Database connection successful!")
        
        # Check if tables exist
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"[INFO] Existing tables: {tables}")
        
        if 'users' in tables:
            print("[SUCCESS] Users table exists!")
            
            # Check table structure
            columns = inspector.get_columns('users')
            print("[INFO] Users table columns:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")
        else:
            print("[ERROR] Users table does not exist!")
            print("[INFO] Creating tables...")
            from app.models import Base
            Base.metadata.create_all(bind=engine)
            print("[SUCCESS] Tables created!")
        
        # Test user creation
        print("\n[TEST] Testing user creation...")
        db = SessionLocal()
        
        try:
            # Check if test user exists
            existing_user = db.query(User).filter(User.email == "debug@test.com").first()
            if existing_user:
                print("[INFO] Removing existing test user...")
                db.delete(existing_user)
                db.commit()
            
            # Create test user
            test_user = User(
                email="debug@test.com",
                name="Debug User",
                hashed_password="test_hash",
                institution="Debug University",
                role="teacher",
                is_active=True
            )
            
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            
            print(f"[SUCCESS] Test user created successfully! ID: {test_user.id}")
            
            # Clean up
            db.delete(test_user)
            db.commit()
            print("[INFO] Test user cleaned up")
            
        except Exception as e:
            print(f"[ERROR] Error creating test user: {e}")
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            db.rollback()
        finally:
            db.close()
            
    except Exception as e:
        print(f"[ERROR] Database debug failed: {e}")
        print(f"[DEBUG] Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    debug_database()