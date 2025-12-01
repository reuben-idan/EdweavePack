#!/usr/bin/env python3

import requests
import time

def final_backend_test():
    """Final test of backend upload endpoints"""
    
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    print("Final Backend Upload Test")
    print("=" * 25)
    
    # Wait for service restart
    print("Waiting 4 minutes for service restart...")
    time.sleep(240)
    
    # Test auth first
    test_user = {
        "email": "final-backend-test@edweavepack.com",
        "password": "final123",
        "full_name": "Final Backend Test",
        "role": "teacher"
    }
    
    try:
        # Register
        reg_response = requests.post(f"{base_url}/api/auth/register", json=test_user, timeout=10)
        print(f"Registration: {reg_response.status_code}")
        
        if reg_response.status_code == 200:
            token = reg_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test all upload endpoints
            print("\nTesting Upload Endpoints:")
            
            # Test file upload
            upload_response = requests.post(f"{base_url}/api/files/simple-upload", headers=headers, timeout=10)
            print(f"File Upload: {upload_response.status_code}")
            
            # Test URL upload
            url_response = requests.post(f"{base_url}/api/files/upload-url", headers=headers, timeout=10)
            print(f"URL Upload: {url_response.status_code}")
            
            # Test file list
            list_response = requests.get(f"{base_url}/api/files/", headers=headers, timeout=10)
            print(f"File List: {list_response.status_code}")
            
            # Test task status
            task_response = requests.get(f"{base_url}/api/tasks/status/test123", headers=headers, timeout=10)
            print(f"Task Status: {task_response.status_code}")
            
            # Check if all working
            all_endpoints = [upload_response.status_code, url_response.status_code, 
                           list_response.status_code, task_response.status_code]
            
            if all(status == 200 for status in all_endpoints):
                print("\n" + "=" * 25)
                print("SUCCESS!")
                print("All backend upload endpoints working")
                print("Upload page functionality fully operational")
                return True
            else:
                print(f"\nSome endpoints not working: {all_endpoints}")
                
    except Exception as e:
        print(f"Error: {e}")
    
    return False

if __name__ == "__main__":
    final_backend_test()