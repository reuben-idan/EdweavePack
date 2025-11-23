#!/usr/bin/env python3
"""
Test script to verify registration endpoint works correctly
"""

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
        print("🧪 Testing user registration...")
        print(f"📤 Sending registration request: {json.dumps(test_user, indent=2)}")
        
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📥 Response status: {response.status_code}")
        print(f"📥 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Registration successful!")
            print(f"🔑 Access token received: {data.get('access_token', 'None')[:20]}...")
            print(f"🔑 Token type: {data.get('token_type', 'None')}")
            
            # Test the token by getting user profile
            token = data.get('access_token')
            if token:
                print("\n🧪 Testing token by fetching user profile...")
                profile_response = requests.get(
                    f"{base_url}/api/auth/me",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if profile_response.status_code == 200:
                    profile_data = profile_response.json()
                    print(f"✅ Profile fetch successful!")
                    print(f"👤 User: {profile_data}")
                else:
                    print(f"❌ Profile fetch failed: {profile_response.status_code}")
                    print(f"📄 Error: {profile_response.text}")
            
        else:
            print(f"❌ Registration failed!")
            print(f"📄 Response: {response.text}")
            
            try:
                error_data = response.json()
                print(f"📄 Error details: {json.dumps(error_data, indent=2)}")
            except:
                pass
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - make sure the backend server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_duplicate_registration():
    """Test duplicate email registration"""
    
    test_user = {
        "email": "test@example.com",
        "full_name": "Test User 2",
        "password": "testpassword456",
        "institution": "Test University 2",
        "role": "teacher"
    }
    
    base_url = "http://localhost:8000"
    
    try:
        print("\n🧪 Testing duplicate email registration...")
        
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 400:
            error_data = response.json()
            print(f"✅ Duplicate email correctly rejected!")
            print(f"📄 Error message: {error_data.get('detail')}")
        else:
            print(f"❌ Expected 400 status for duplicate email, got {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing duplicate registration: {e}")

if __name__ == "__main__":
    test_registration()
    test_duplicate_registration()