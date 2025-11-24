#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app
import json

def test_registration_direct():
    """Test registration using FastAPI TestClient to see actual errors"""
    print("=== Testing Registration Direct ===")
    
    client = TestClient(app)
    
    test_data = {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "testpassword123",
        "institution": "Test Institution",
        "role": "teacher"
    }
    
    try:
        print(f"Sending registration request...")
        print(f"Data: {json.dumps(test_data, indent=2)}")
        
        response = client.post("/api/auth/register", json=test_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_registration_direct()