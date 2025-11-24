#!/usr/bin/env python3

import requests
import json

def test_new_registration():
    """Test the new registration endpoint on port 8002"""
    print("=== Testing New Registration Endpoint ===")
    
    url = "http://localhost:8002/test-register"
    
    test_data = {
        "email": "newtest@example.com",
        "full_name": "New Test User",
        "password": "testpassword123",
        "institution": "Test Institution",
        "role": "teacher"
    }
    
    try:
        response = requests.post(url, json=test_data, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_new_registration()