#!/usr/bin/env python3

import requests
import time
import json

def wait_for_deployment():
    """Wait for deployment to complete"""
    print("Waiting for deployment to complete...")
    for i in range(12):  # 2 minutes max
        try:
            response = requests.get("http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com/api/health", timeout=5)
            if response.status_code == 200:
                print(f"Deployment ready after {i*10} seconds")
                return True
        except:
            pass
        
        print(f"Waiting... ({i*10}s)")
        time.sleep(10)
    
    return False

def test_complete_auth_flow():
    """Test complete authentication flow"""
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    print("\n=== Testing Complete Auth Flow ===")
    
    # Test user data
    test_user = {
        "email": "demo@edweavepack.com",
        "password": "demo123",
        "full_name": "Demo Teacher",
        "role": "teacher"
    }
    
    try:
        # 1. Test registration
        print("1. Testing Registration...")
        reg_response = requests.post(f"{base_url}/api/auth/register", json=test_user, timeout=10)
        print(f"   Status: {reg_response.status_code}")
        
        if reg_response.status_code == 200:
            print("   ✓ Registration: SUCCESS")
            reg_data = reg_response.json()
            token = reg_data.get("access_token")
            print(f"   Token received: {token[:20]}...")
            
            # 2. Test login
            print("\n2. Testing Login...")
            login_data = {"email": test_user["email"], "password": test_user["password"]}
            login_response = requests.post(f"{base_url}/api/auth/token", json=login_data, timeout=10)
            print(f"   Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                print("   ✓ Login: SUCCESS")
                login_data = login_response.json()
                new_token = login_data.get("access_token")
                
                # 3. Test protected endpoint
                print("\n3. Testing Protected Endpoint...")
                headers = {"Authorization": f"Bearer {new_token}"}
                me_response = requests.get(f"{base_url}/api/auth/me", headers=headers, timeout=10)
                print(f"   Status: {me_response.status_code}")
                
                if me_response.status_code == 200:
                    print("   ✓ Protected Endpoint: SUCCESS")
                    user_data = me_response.json()
                    print(f"   User: {user_data.get('full_name')} ({user_data.get('email')})")
                    
                    # 4. Test curriculum endpoint
                    print("\n4. Testing Curriculum Endpoint...")
                    curr_response = requests.get(f"{base_url}/api/curriculum/", headers=headers, timeout=10)
                    print(f"   Status: {curr_response.status_code}")
                    
                    if curr_response.status_code == 200:
                        print("   ✓ Curriculum Endpoint: SUCCESS")
                        return True
                    else:
                        print("   ✗ Curriculum Endpoint: FAILED")
                else:
                    print("   ✗ Protected Endpoint: FAILED")
            else:
                print("   ✗ Login: FAILED")
                print(f"   Response: {login_response.text}")
        else:
            print("   ✗ Registration: FAILED")
            print(f"   Response: {reg_response.text}")
            
    except Exception as e:
        print(f"Auth test error: {e}")
    
    return False

def test_frontend_integration():
    """Test frontend can connect to backend"""
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    print("\n=== Testing Frontend Integration ===")
    
    try:
        # Test frontend loads
        response = requests.get(base_url, timeout=10)
        print(f"Frontend Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Frontend: ACCESSIBLE")
            
            # Check if it contains React app
            if "EdweavePack" in response.text or "react" in response.text.lower():
                print("✓ React App: LOADED")
                return True
            else:
                print("? React App: UNKNOWN")
        else:
            print("✗ Frontend: FAILED")
            
    except Exception as e:
        print(f"Frontend test error: {e}")
    
    return False

def main():
    print("EdweavePack Final Authentication Test")
    print("=" * 45)
    
    # Wait for deployment
    if not wait_for_deployment():
        print("❌ Deployment not ready")
        return
    
    # Test auth flow
    auth_success = test_complete_auth_flow()
    
    # Test frontend
    frontend_success = test_frontend_integration()
    
    print("\n" + "=" * 45)
    print("🎯 FINAL RESULTS:")
    print(f"   Authentication: {'✅ WORKING' if auth_success else '❌ FAILED'}")
    print(f"   Frontend: {'✅ WORKING' if frontend_success else '❌ FAILED'}")
    
    if auth_success and frontend_success:
        print("\n🚀 SUCCESS! EdweavePack is fully operational!")
        print("🌐 URL: http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com")
        print("📝 Users can now:")
        print("   • Register new accounts")
        print("   • Login and authenticate") 
        print("   • Access protected features")
        print("   • Use all EdweavePack functionality")
    else:
        print("\n⚠️  Some issues remain - check logs for details")

if __name__ == "__main__":
    main()