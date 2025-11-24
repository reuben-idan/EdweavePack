#!/usr/bin/env python3

import requests
import json

def test_registration_endpoint():
    """Test the registration endpoint directly"""
    print("=== Testing Registration Endpoint ===")
    
    url = "http://localhost:8000/api/auth/register"
    
    test_data = {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "testpassword123",
        "institution": "Test Institution",
        "role": "teacher"
    }
    
    try:
        print(f"Sending POST request to: {url}")
        print(f"Data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(url, json=test_data, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"Response JSON: {json.dumps(response_json, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server. Is it running on localhost:8000?")
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_registration_endpoint()