#!/usr/bin/env python3

import requests
import json

BASE_URL = "http://localhost:8000"

def test_forgot_password():
    """Test forgot password endpoint"""
    print("Testing forgot password...")
    
    # Test with existing user email
    response = requests.post(f"{BASE_URL}/api/auth/forgot-password", 
                           json={"email": "test@example.com"})
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 200

def test_profile_update():
    """Test profile update endpoint"""
    print("\nTesting profile update...")
    
    # First login to get token
    login_data = {
        "username": "test@example.com",
        "password": "testpassword"
    }
    
    login_response = requests.post(f"{BASE_URL}/api/auth/token", data=login_data)
    
    if login_response.status_code != 200:
        print("Login failed, cannot test profile update")
        return False
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test profile update
    profile_data = {
        "fullName": "Updated Name",
        "email": "test@example.com",
        "institution": "Updated Institution"
    }
    
    response = requests.put(f"{BASE_URL}/api/auth/profile", 
                          json=profile_data, headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return response.status_code == 200

if __name__ == "__main__":
    print("Testing authentication endpoints...")
    
    # Test endpoints
    forgot_success = test_forgot_password()
    profile_success = test_profile_update()
    
    print(f"\nResults:")
    print(f"Forgot Password: {'✓' if forgot_success else '✗'}")
    print(f"Profile Update: {'✓' if profile_success else '✗'}")