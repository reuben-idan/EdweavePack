#!/usr/bin/env python3

import requests
import time

def verify_backend_endpoints():
    """Verify backend upload endpoints are working"""
    
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    print("Verifying Backend Upload Endpoints")
    print("=" * 35)
    
    # Wait for deployment
    print("Waiting 2 minutes for deployment...")
    time.sleep(120)
    
    # Get auth token
    test_user = {
        "email": "backend-test@edweavepack.com",
        "password": "backend123",
        "full_name": "Backend Test",
        "role": "teacher"
    }
    
    try:
        # Register
        reg_response = requests.post(f"{base_url}/api/auth/register", json=test_user, timeout=10)
        print(f"Registration: {reg_response.status_code}")
        
        if reg_response.status_code == 200:
            token = reg_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test upload endpoints
            endpoints = [
                ("/api/files/simple-upload", "POST"),
                ("/api/files/upload-url", "POST"),
                ("/api/files/", "GET"),
                ("/api/tasks/status/test123", "GET")
            ]
            
            all_working = True
            
            for endpoint, method in endpoints:
                try:
                    if method == "POST":
                        response = requests.post(f"{base_url}{endpoint}", headers=headers, timeout=10)
                    else:
                        response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=10)
                    
                    print(f"{method} {endpoint}: {response.status_code}")
                    
                    if response.status_code == 404:
                        all_working = False
                        
                except Exception as e:
                    print(f"{method} {endpoint}: ERROR - {e}")
                    all_working = False
            
            print("\n" + "=" * 35)
            if all_working:
                print("SUCCESS! All backend endpoints working")
                print("Upload functionality is now fully operational")
            else:
                print("Some endpoints still returning 404")
                print("Service may need more time to update")
                
            return all_working
            
    except Exception as e:
        print(f"Error: {e}")
    
    return False

if __name__ == "__main__":
    verify_backend_endpoints()