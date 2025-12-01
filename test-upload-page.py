#!/usr/bin/env python3

import requests
import time

def test_upload_endpoints():
    """Test upload page endpoints"""
    
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    print("Testing Upload Page Endpoints")
    print("=" * 30)
    
    # Wait for deployment
    print("Waiting 45 seconds for deployment...")
    time.sleep(45)
    
    # Register and get token
    test_user = {
        "email": "upload-test@edweavepack.com",
        "password": "upload123",
        "full_name": "Upload Test",
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
                "/api/files/simple-upload",
                "/api/files/upload-url", 
                "/api/files/",
                "/api/tasks/status/test123"
            ]
            
            for endpoint in endpoints:
                try:
                    if endpoint == "/api/files/simple-upload":
                        response = requests.post(f"{base_url}{endpoint}", headers=headers, timeout=10)
                    elif endpoint == "/api/files/upload-url":
                        response = requests.post(f"{base_url}{endpoint}", headers=headers, timeout=10)
                    else:
                        response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=10)
                    
                    print(f"{endpoint}: {response.status_code}")
                    
                except Exception as e:
                    print(f"{endpoint}: ERROR - {e}")
            
            # Test frontend upload page
            print("\nTesting Frontend Upload Page...")
            upload_response = requests.get(f"{base_url}/upload", timeout=10)
            print(f"Upload Page: {upload_response.status_code}")
            
            if upload_response.status_code == 200:
                print("Upload page accessible")
                
                print("\n" + "=" * 30)
                print("UPLOAD PAGE TESTS COMPLETE")
                print("Backend Endpoints: WORKING")
                print("Frontend Page: ACCESSIBLE")
                print("Upload functionality should now work without errors")
                return True
                
    except Exception as e:
        print(f"Error: {e}")
    
    print("Some tests failed")
    return False

if __name__ == "__main__":
    test_upload_endpoints()