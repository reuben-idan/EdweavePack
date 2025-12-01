#!/usr/bin/env python3

import subprocess
import boto3
import time

def rebuild_backend():
    """Rebuild backend with auth endpoints"""
    
    print("=== Rebuilding Backend with Auth ===")
    
    # Build backend image
    result = subprocess.run([
        "docker", "build", "-t", "edweavepack-backend:latest", "."
    ], cwd="backend", capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Build failed: {result.stderr}")
        return False
    
    print("Backend built successfully")
    
    # Tag image
    result = subprocess.run([
        "docker", "tag", "edweavepack-backend:latest", 
        "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-backend:latest"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Tag failed: {result.stderr}")
        return False
    
    print("Image tagged successfully")
    
    # Push image
    result = subprocess.run([
        "docker", "push", 
        "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-backend:latest"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Push failed: {result.stderr}")
        return False
    
    print("Image pushed successfully")
    return True

def update_service():
    """Update ECS service"""
    try:
        ecs = boto3.client('ecs', region_name='eu-north-1')
        
        cluster_name = 'edweavepack-cluster'
        service_name = 'edweavepack-service'
        
        print(f"Updating service: {service_name}")
        
        response = ecs.update_service(
            cluster=cluster_name,
            service=service_name,
            forceNewDeployment=True
        )
        
        print("Service update initiated")
        return True
        
    except Exception as e:
        print(f"Service update failed: {e}")
        return False

def test_auth():
    """Test auth endpoints"""
    import requests
    
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    print("=== Testing Auth Endpoints ===")
    
    # Test registration
    try:
        test_user = {
            "email": "test@edweavepack.com",
            "password": "testpass123",
            "full_name": "Test User",
            "role": "teacher"
        }
        
        response = requests.post(f"{base_url}/api/auth/register", json=test_user, timeout=10)
        print(f"Registration Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Registration: WORKING")
            data = response.json()
            token = data.get("access_token")
            
            # Test login
            login_data = {"email": test_user["email"], "password": test_user["password"]}
            login_response = requests.post(f"{base_url}/api/auth/token", json=login_data, timeout=10)
            print(f"Login Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                print("Login: WORKING")
            else:
                print("Login: FAILED")
                
        else:
            print(f"Registration failed: {response.text}")
            
    except Exception as e:
        print(f"Auth test error: {e}")

def main():
    print("EdweavePack Auth Fix Deployment")
    print("=" * 40)
    
    # Rebuild backend
    if not rebuild_backend():
        print("Failed to rebuild backend")
        return
    
    # Update service
    if not update_service():
        print("Failed to update service")
        return
    
    print("\nWaiting 60 seconds for deployment...")
    time.sleep(60)
    
    # Test auth
    test_auth()
    
    print("\n" + "=" * 40)
    print("Auth deployment completed!")
    print("Users can now register and login at:")
    print("http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com")

if __name__ == "__main__":
    main()