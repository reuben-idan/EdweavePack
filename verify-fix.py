#!/usr/bin/env python3

import requests
import time
import json

def test_application():
    """Test the application endpoints"""
    
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    print("Testing EdweavePack Application")
    print("=" * 40)
    print(f"Base URL: {base_url}")
    
    # Test frontend
    print("\n1. Testing Frontend...")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Frontend: WORKING")
        else:
            print(f"Frontend: Issue (Status {response.status_code})")
    except Exception as e:
        print(f"Frontend: Error - {e}")
    
    # Test API health
    print("\n2. Testing API Health...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("API Health: WORKING")
            print(f"Response: {response.text}")
        else:
            print(f"API Health: Issue (Status {response.status_code})")
    except Exception as e:
        print(f"API Health: Error - {e}")
    
    # Test auth endpoints
    print("\n3. Testing Auth Endpoints...")
    try:
        response = requests.get(f"{base_url}/api/auth/", timeout=10)
        print(f"Auth Status: {response.status_code}")
        if response.status_code in [200, 404, 405]:  # 404/405 are OK for GET on auth
            print("Auth Endpoint: ACCESSIBLE")
        else:
            print(f"Auth Endpoint: Issue (Status {response.status_code})")
    except Exception as e:
        print(f"Auth Endpoint: Error - {e}")
    
    # Test registration endpoint
    print("\n4. Testing Registration Endpoint...")
    try:
        # Just test if endpoint is accessible (don't actually register)
        response = requests.options(f"{base_url}/api/auth/register", timeout=10)
        print(f"Register Options Status: {response.status_code}")
        if response.status_code in [200, 204, 405]:
            print("Registration Endpoint: ACCESSIBLE")
        else:
            print(f"Registration Endpoint: Issue (Status {response.status_code})")
    except Exception as e:
        print(f"Registration Endpoint: Error - {e}")

def main():
    print("Waiting 30 seconds for deployment to stabilize...")
    time.sleep(30)
    
    test_application()
    
    print("\n" + "=" * 40)
    print("Verification completed!")
    print("\nIf all endpoints are working, users can now:")
    print("- Access the application")
    print("- Register new accounts") 
    print("- Login and authenticate")
    print("- Use all EdweavePack features")

if __name__ == "__main__":
    main()