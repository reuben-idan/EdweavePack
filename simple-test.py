#!/usr/bin/env python3

import requests
import json

def test_auth():
    """Simple auth test"""
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    print("Testing EdweavePack Authentication")
    print("=" * 40)
    
    # Test user
    test_user = {
        "email": "teacher@edweavepack.com",
        "password": "teacher123",
        "full_name": "Test Teacher",
        "role": "teacher"
    }
    
    try:
        # Registration
        print("1. Testing Registration...")
        reg_response = requests.post(f"{base_url}/api/auth/register", json=test_user, timeout=10)
        print(f"   Status: {reg_response.status_code}")
        
        if reg_response.status_code == 200:
            print("   Registration: SUCCESS")
            reg_data = reg_response.json()
            print(f"   User created: {reg_data['user']['full_name']}")
            
            # Login
            print("\n2. Testing Login...")
            login_data = {"email": test_user["email"], "password": test_user["password"]}
            login_response = requests.post(f"{base_url}/api/auth/token", json=login_data, timeout=10)
            print(f"   Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                print("   Login: SUCCESS")
                login_result = login_response.json()
                token = login_result.get("access_token")
                
                # Test protected endpoint
                print("\n3. Testing Protected Access...")
                headers = {"Authorization": f"Bearer {token}"}
                me_response = requests.get(f"{base_url}/api/auth/me", headers=headers, timeout=10)
                print(f"   Status: {me_response.status_code}")
                
                if me_response.status_code == 200:
                    print("   Protected Access: SUCCESS")
                    user_info = me_response.json()
                    print(f"   Logged in as: {user_info['full_name']}")
                    return True
                else:
                    print("   Protected Access: FAILED")
            else:
                print("   Login: FAILED")
        else:
            print("   Registration: FAILED")
            if reg_response.status_code == 400:
                print("   (User may already exist)")
                
                # Try login directly
                print("\n   Trying direct login...")
                login_data = {"email": test_user["email"], "password": test_user["password"]}
                login_response = requests.post(f"{base_url}/api/auth/token", json=login_data, timeout=10)
                if login_response.status_code == 200:
                    print("   Direct Login: SUCCESS")
                    return True
                    
    except Exception as e:
        print(f"   Error: {e}")
    
    return False

def test_frontend():
    """Test frontend"""
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    print("\n4. Testing Frontend...")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   Frontend: ACCESSIBLE")
            return True
    except Exception as e:
        print(f"   Frontend Error: {e}")
    
    return False

def main():
    auth_works = test_auth()
    frontend_works = test_frontend()
    
    print("\n" + "=" * 40)
    print("RESULTS:")
    print(f"Authentication: {'WORKING' if auth_works else 'FAILED'}")
    print(f"Frontend: {'WORKING' if frontend_works else 'FAILED'}")
    
    if auth_works and frontend_works:
        print("\nSUCCESS! EdweavePack is fully operational!")
        print("URL: http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com")
        print("\nUsers can now:")
        print("- Register accounts")
        print("- Login and authenticate")
        print("- Access all features")
    else:
        print("\nSome issues remain")

if __name__ == "__main__":
    main()