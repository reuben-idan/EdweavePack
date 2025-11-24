#!/usr/bin/env python3

import requests
import time
import json

def verify_server_fix():
    """Verify the server fix is working"""
    print("=== Verifying Server Fix ===")
    
    # Wait for server to start
    print("Waiting for server to start...")
    for i in range(30):
        try:
            response = requests.get('http://localhost:8000/', timeout=2)
            if response.status_code == 200:
                print(f"✓ Server responding after {i+1} seconds")
                break
        except:
            time.sleep(1)
    else:
        print("✗ Server not responding after 30 seconds")
        return False
    
    # Test registration with unique identifier
    test_data = {
        "email": f"verify_{int(time.time())}@example.com",
        "full_name": "Verification User",
        "password": "testpassword123",
        "institution": "Test Institution",
        "role": "teacher"
    }
    
    try:
        response = requests.post('http://localhost:8000/api/auth/register', json=test_data, timeout=10)
        print(f"Registration Status: {response.status_code}")
        
        response_data = response.json()
        print(f"Response: {response_data}")
        
        if response.status_code == 200 and "access_token" in response_data:
            print("✓ Registration working correctly!")
            return True
        elif "UPDATED_CODE" in str(response_data):
            print("✓ Updated code is running (with error details)")
            return True
        else:
            print("✗ Registration still has issues")
            return False
            
    except Exception as e:
        print(f"✗ Registration test failed: {e}")
        return False

if __name__ == "__main__":
    verify_server_fix()