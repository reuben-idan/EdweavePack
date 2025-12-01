#!/usr/bin/env python3

import requests
import time

def debug_auth():
    """Debug authentication issue"""
    
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    print("Debugging Authentication")
    print("=" * 25)
    
    # Wait for deployment
    print("Waiting 30 seconds...")
    time.sleep(30)
    
    # Check debug endpoint
    try:
        debug_response = requests.get(f"{base_url}/api/debug/users", timeout=10)
        print(f"Debug endpoint: {debug_response.status_code}")
        if debug_response.status_code == 200:
            print(f"Users in DB: {debug_response.json()}")
        
        # Register a user
        test_user = {
            "email": "debug-user@test.com",
            "password": "debug123",
            "full_name": "Debug User",
            "role": "teacher"
        }
        
        print("\nRegistering user...")
        reg_response = requests.post(f"{base_url}/api/auth/register", json=test_user, timeout=10)
        print(f"Registration: {reg_response.status_code}")
        
        if reg_response.status_code == 200:
            # Check users again
            debug_response2 = requests.get(f"{base_url}/api/debug/users", timeout=10)
            if debug_response2.status_code == 200:
                print(f"Users after registration: {debug_response2.json()}")
            
            # Try login
            print("\nTrying login...")
            login_data = {"username": test_user["email"], "password": test_user["password"]}
            login_response = requests.post(f"{base_url}/api/auth/token", data=login_data, timeout=10)
            print(f"Login: {login_response.status_code}")
            
            if login_response.status_code != 200:
                print(f"Login error: {login_response.text}")
            else:
                print("Login successful!")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_auth()