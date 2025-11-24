#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.schemas.auth import UserCreate
import json

def test_pydantic_validation():
    """Test Pydantic validation for UserCreate"""
    print("=== Testing Pydantic Validation ===")
    
    test_data = {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "testpassword123",
        "institution": "Test Institution",
        "role": "teacher"
    }
    
    try:
        print(f"Input data: {json.dumps(test_data, indent=2)}")
        
        # Test UserCreate validation
        user_create = UserCreate(**test_data)
        print(f"UserCreate object: {user_create}")
        print(f"Email: {user_create.email}")
        print(f"Full name: {user_create.full_name}")
        print(f"Password: {'*' * len(user_create.password)}")
        print(f"Institution: {user_create.institution}")
        print(f"Role: {user_create.role}")
        
        print("OK Pydantic validation passed")
        
    except Exception as e:
        print(f"ERROR Pydantic validation failed: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_pydantic_validation()