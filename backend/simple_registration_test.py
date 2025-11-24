#!/usr/bin/env python3

import requests
import json

def test_registration():
    """Test user registration endpoint"""
    
    # Test data
    test_user = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123",
        "institution": "Test University",
        "role": "teacher"
    }
    
    base_url = "http://localhost:8000"
    
    try:
        print("Testing user registration...")
        print(f"Sending registration request: {json.dumps(test_user, indent=2)}")
        
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("Registration successful!")
            print(f"Access token received: {data.get('access_token', 'None')[:20]}...")
            print(f"Token type: {data.get('token_type', 'None')}")
            
        else:
            print("Registration failed!")
            print(f"Response: {response.text}")
            
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                pass
                
    except requests.exceptions.ConnectionError:
        print("Connection error - make sure the backend server is running on localhost:8000")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_registration()