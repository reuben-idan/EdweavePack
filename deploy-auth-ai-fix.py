#!/usr/bin/env python3

import subprocess
import boto3
import time

def rebuild_and_deploy():
    """Rebuild backend with auth fixes and AWS AI"""
    
    print("=== Rebuilding Backend with Auth & AI ===")
    
    # Build backend
    result = subprocess.run([
        "docker", "build", "-t", "edweavepack-backend:latest", "."
    ], cwd="backend", capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Build failed: {result.stderr}")
        return False
    
    print("Backend built successfully")
    
    # Tag and push
    subprocess.run([
        "docker", "tag", "edweavepack-backend:latest", 
        "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-backend:latest"
    ])
    
    subprocess.run([
        "docker", "push", 
        "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-backend:latest"
    ])
    
    print("Image pushed successfully")
    
    # Update ECS service
    ecs = boto3.client('ecs', region_name='eu-north-1')
    
    ecs.update_service(
        cluster='edweavepack-cluster',
        service='edweavepack-service',
        forceNewDeployment=True
    )
    
    print("Service updated")
    return True

def test_auth_and_ai():
    """Test authentication and AI features"""
    import requests
    
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    print("=== Testing Auth & AI ===")
    
    # Test registration
    test_user = {
        "email": "ai-teacher@edweavepack.com",
        "password": "aitest123",
        "full_name": "AI Teacher",
        "role": "teacher"
    }
    
    try:
        # Register
        reg_response = requests.post(f"{base_url}/api/auth/register", json=test_user, timeout=10)
        print(f"Registration: {reg_response.status_code}")
        
        if reg_response.status_code == 200:
            token = reg_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test AI curriculum generation
            curriculum_data = {
                "title": "AI-Enhanced Math Curriculum",
                "subject": "Mathematics",
                "grade_level": "Grade 8"
            }
            
            curr_response = requests.post(f"{base_url}/api/curriculum/", 
                                        json=curriculum_data, headers=headers, timeout=30)
            print(f"AI Curriculum Generation: {curr_response.status_code}")
            
            if curr_response.status_code == 200:
                print("AI Features: WORKING")
                return True
                
    except Exception as e:
        print(f"Test error: {e}")
    
    return False

def main():
    print("EdweavePack Auth & AI Fix")
    print("=" * 30)
    
    if not rebuild_and_deploy():
        print("Deployment failed")
        return
    
    print("Waiting 60 seconds for deployment...")
    time.sleep(60)
    
    if test_auth_and_ai():
        print("\nSUCCESS! Auth and AI features working")
        print("URL: http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com")
    else:
        print("Some issues remain")

if __name__ == "__main__":
    main()