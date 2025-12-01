#!/usr/bin/env python3

import requests
import time

def test_auth_fix():
    """Test authentication fix"""
    
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    print("Testing Authentication Fix")
    print("=" * 30)
    
    # Wait for deployment
    print("Waiting 45 seconds for deployment...")
    time.sleep(45)
    
    # Test user
    test_user = {
        "email": "auth-fix-test@edweavepack.com",
        "password": "authfix123",
        "full_name": "Auth Fix Test",
        "role": "teacher"
    }
    
    try:
        # Registration
        print("1. Testing Registration...")
        reg_response = requests.post(f"{base_url}/api/auth/register", json=test_user, timeout=10)
        print(f"   Status: {reg_response.status_code}")
        
        if reg_response.status_code == 200:
            print("   Registration: SUCCESS")
            
            # Login
            print("\n2. Testing Login...")
            login_data = {"username": test_user["email"], "password": test_user["password"]}
            login_response = requests.post(f"{base_url}/api/auth/token", data=login_data, timeout=10)
            print(f"   Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                print("   Login: SUCCESS")
                token = login_response.json()["access_token"]
                headers = {"Authorization": f"Bearer {token}"}
                
                # Test protected endpoint
                print("\n3. Testing Protected Access...")
                me_response = requests.get(f"{base_url}/api/auth/me", headers=headers, timeout=10)
                print(f"   Status: {me_response.status_code}")
                
                if me_response.status_code == 200:
                    print("   Protected Access: SUCCESS")
                    user_info = me_response.json()
                    print(f"   User: {user_info['full_name']}")
                    
                    # Test AI features
                    print("\n4. Testing AI Curriculum...")
                    curriculum_data = {
                        "title": "Test AI Curriculum",
                        "subject": "Science",
                        "grade_level": "Grade 7"
                    }
                    
                    ai_response = requests.post(f"{base_url}/api/curriculum/", 
                                              json=curriculum_data, headers=headers, timeout=30)
                    print(f"   Status: {ai_response.status_code}")
                    
                    if ai_response.status_code == 200:
                        print("   AI Curriculum: SUCCESS")
                        
                        print("\n" + "=" * 30)
                        print("AUTHENTICATION FIXED!")
                        print("Registration: WORKING")
                        print("Login: WORKING")
                        print("Protected Access: WORKING")
                        print("AWS AI Features: WORKING")
                        print("\nEdweavePack is ready for use!")
                        print("URL: http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com")
                        return True
                        
    except Exception as e:
        print(f"Error: {e}")
    
    print("Authentication still has issues")
    return False

if __name__ == "__main__":
    test_auth_fix()