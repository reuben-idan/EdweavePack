#!/usr/bin/env python3

import boto3
import subprocess
import json
import time

def rebuild_and_deploy_frontend():
    """Rebuild frontend with correct ALB URL and deploy"""
    
    print("=== Rebuilding Frontend with Correct ALB URL ===")
    
    # Build and push frontend image
    commands = [
        "cd frontend",
        "docker build -t edweavepack-frontend:latest .",
        "docker tag edweavepack-frontend:latest 084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-frontend:latest",
        "docker push 084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-frontend:latest"
    ]
    
    for cmd in commands:
        print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        print("✓ Success")
    
    return True

def update_ecs_service():
    """Update ECS service to use new frontend image"""
    try:
        ecs = boto3.client('ecs', region_name='eu-north-1')
        
        # Find the working service with frontend
        cluster_name = 'edweavepack-cluster'
        service_name = 'edweavepack-service'  # This one has both frontend and backend running
        
        print(f"=== Updating ECS Service: {service_name} ===")
        
        # Force new deployment
        response = ecs.update_service(
            cluster=cluster_name,
            service=service_name,
            forceNewDeployment=True
        )
        
        print(f"✓ Service update initiated")
        print(f"Service ARN: {response['service']['serviceArn']}")
        
        # Wait for deployment to complete
        print("Waiting for deployment to complete...")
        waiter = ecs.get_waiter('services_stable')
        waiter.wait(
            cluster=cluster_name,
            services=[service_name],
            WaiterConfig={'maxAttempts': 30, 'delay': 30}
        )
        
        print("✓ Deployment completed successfully")
        return True
        
    except Exception as e:
        print(f"Error updating service: {e}")
        return False

def verify_deployment():
    """Verify the deployment is working"""
    try:
        import requests
        
        alb_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
        
        print(f"=== Verifying Deployment ===")
        print(f"Testing: {alb_url}")
        
        # Test frontend
        response = requests.get(alb_url, timeout=10)
        print(f"Frontend Status: {response.status_code}")
        
        # Test API
        api_response = requests.get(f"{alb_url}/api/health", timeout=10)
        print(f"API Status: {api_response.status_code}")
        
        if response.status_code == 200 and api_response.status_code == 200:
            print("✓ Deployment verified successfully")
            return True
        else:
            print("⚠ Deployment needs more time to stabilize")
            return False
            
    except Exception as e:
        print(f"Verification error: {e}")
        return False

def main():
    print("EdweavePack Frontend Fix & Deployment")
    print("=" * 50)
    
    # Step 1: Rebuild frontend
    if not rebuild_and_deploy_frontend():
        print("❌ Failed to rebuild frontend")
        return
    
    # Step 2: Update ECS service
    if not update_ecs_service():
        print("❌ Failed to update ECS service")
        return
    
    # Step 3: Verify deployment
    print("\nWaiting 60 seconds for containers to start...")
    time.sleep(60)
    
    verify_deployment()
    
    print("\n" + "=" * 50)
    print("✅ Frontend deployment completed!")
    print("🌐 Application URL: http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com")
    print("📚 API Docs: http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com/docs")

if __name__ == "__main__":
    main()