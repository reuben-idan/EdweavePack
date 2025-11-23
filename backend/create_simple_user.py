#!/usr/bin/env python3

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from passlib.context import CryptContext

# Simple setup without complex relationships
DATABASE_URL = "sqlite:///./edweavepack.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SimpleUser(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    institution = Column(String, nullable=True)
    role = Column(String, default="teacher")
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_user():
    """Create a test user"""
    # Create table
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if user exists
        existing_user = db.query(SimpleUser).filter(SimpleUser.email == "test@example.com").first()
        if existing_user:
            print("Test user already exists")
            return
        
        # Create test user
        hashed_password = pwd_context.hash("testpassword")
        
        test_user = SimpleUser(
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