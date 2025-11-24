#!/usr/bin/env python3

import requests
import json

def test_frontend_registration():
    """Test registration using the frontend's updated endpoint"""
    print("=== Testing Frontend Registration (Port 8002) ===")
    
    url = "http://localhost:8002/test-register"
    
    test_data = {
        "email": "frontend_test@example.com",
        "full_name": "Frontend Test User",
        "password": "testpassword123",
        "institution": "Test Institution",
        "role": "teacher"
    }
    
    try:
        response = requests.post(url, json=test_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✓ Registration working with temporary endpoint")
            return True
        else:
            print("✗ Registration failed")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    test_frontend_registration()