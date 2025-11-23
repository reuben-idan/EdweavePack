#!/usr/bin/env python3
"""
Simple test script for registration endpoint
"""

import requests
import json
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_registration_endpoint():
    """Test registration endpoint with sample data"""
    
    # Test data
    test_user = {
        "email": "testuser@edweavepack.com",
        "full_name": "Test User",
        "password": "testpassword123",
        "institution": "Test University",
        "role": "teacher"
    }
    
    base_url = "http://localhost:8000"
    
    try:
        print("[TEST] Testing user registration endpoint...")
        print(f"[DATA] Registration data: {json.dumps(test_user, indent=2)}")
        
        # Test registration
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"[RESPONSE] Status Code: {response.status_code}")
        print(f"[RESPONSE] Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("[SUCCESS] Registration successful!")
            print(f"[TOKEN] Access token: {data.get('access_token', 'None')[:30]}...")
            print(f"[TOKEN] Token type: {data.get('token_type', 'None')}")
            
            # Test token by getting profile
            token = data.get('access_token')
            if token:
                print("[TEST] Testing token with profile endpoint...")
                profile_response = requests.get(
                    f"{base_url}/api/auth/me",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10
                )
                
                if profile_response.status_code == 200:
                    profile_data = profile_response.json()
                    print("[SUCCESS] Profile fetch successful!")
                    print(f"[PROFILE] User data: {json.dumps(profile_data, indent=2)}")
                else:
                    print(f"[ERROR] Profile fetch failed: {profile_response.status_code}")
                    print(f"[ERROR] Response: {profile_response.text}")
            
            return True
            
        else:
            print(f"[ERROR] Registration failed with status {response.status_code}")
            print(f"[ERROR] Response text: {response.text}")
            
            try:
                error_data = response.json()
                print(f"[ERROR] Error details: {json.dumps(error_data, indent=2)}")
            except:
                print("[ERROR] Could not parse error response as JSON")
            
            return False
                
    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection failed - backend server not running on localhost:8000")
        print("[INFO] Start the server with: python start_server.py")
        return False
        
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

def test_duplicate_registration():
    """Test duplicate email handling"""
    
    test_user = {
        "email": "testuser@edweavepack.com",  # Same email as above
        "full_name": "Another User",
        "password": "differentpassword",
        "institution": "Different University",
        "role": "teacher"
    }
    
    base_url = "http://localhost:8000"
    
    try:
        print("\n[TEST] Testing duplicate email registration...")
        
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"[RESPONSE] Status Code: {response.status_code}")
        
        if response.status_code == 400:
            error_data = response.json()
            print("[SUCCESS] Duplicate email correctly rejected!")
            print(f"[ERROR] Message: {error_data.get('detail')}")
            return True
        else:
            print(f"[ERROR] Expected 400 for duplicate email, got {response.status_code}")
            print(f"[ERROR] Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Duplicate test failed: {e}")
        return False

def main():
    """Run all tests"""
    
    print("=" * 60)
    print("EdweavePack Registration Endpoint Test")
    print("=" * 60)
    
    # Test 1: Normal registration
    success1 = test_registration_endpoint()
    
    # Test 2: Duplicate email
    success2 = test_duplicate_registration()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("[SUCCESS] All registration tests passed!")
    else:
        print("[ERROR] Some tests failed. Check output above.")
    print("=" * 60)

if __name__ == "__main__":
    main()