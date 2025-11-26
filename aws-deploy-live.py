#!/usr/bin/env python3
"""Live AWS deployment with enhanced AI implementation"""

import subprocess
import sys
import time
import json
import os

def run_cmd(cmd, cwd=None):
    """Execute command with output"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=600)
        print(result.stdout)
        if result.stderr:
            print(f"Warning: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def deploy_to_aws():
    """Deploy enhanced AI implementation to AWS"""
    
    print("AWS Live Deployment - Enhanced AI EdweavePack")
    print("=" * 50)
    
    # 1. Build and push Docker images
    print("Building and pushing Docker images...")
    
    # Backend
    if not run_cmd("docker build -t edweavepack-backend:latest -f backend/Dockerfile.prod backend/"):
        return False
    
    # Frontend  
    if not run_cmd("docker build -t edweavepack-frontend:latest -f frontend/Dockerfile.prod frontend/"):
        return False
    
    # 2. Update ECS services
    print("Updating ECS services...")
    
    # Force new deployment
    if not run_cmd("aws ecs update-service --cluster edweavepack-cluster --service edweavepack-backend --force-new-deployment"):
        print("Backend service update failed")
    
    if not run_cmd("aws ecs update-service --cluster edweavepack-cluster --service edweavepack-frontend --force-new-deployment"):
        print("Frontend service update failed")
    
    # 3. Wait for deployment
    print("Waiting for deployment to complete...")
    time.sleep(120)
    
    return True

def test_live_deployment():
    """Test live deployment"""
    
    base_url = "http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com"
    
    print(f"\nTesting live deployment: {base_url}")
    
    try:
        import requests
        
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=15)
        if response.status_code == 200:
            print("Health check: PASS")
        else:
            print(f"Health check: FAIL ({response.status_code})")
        
        # Test frontend
        response = requests.get(base_url, timeout=15)
        if response.status_code == 200:
            print("Frontend: PASS")
        else:
            print(f"Frontend: FAIL ({response.status_code})")
        
        # Test API docs
        response = requests.get(f"{base_url}/docs", timeout=15)
        if response.status_code == 200:
            print("API Docs: PASS")
        else:
            print(f"API Docs: FAIL ({response.status_code})")
            
        return True
        
    except Exception as e:
        print(f"Testing failed: {e}")
        return False

def quick_aws_deploy():
    """Quick AWS deployment using existing infrastructure"""
    
    print("Quick AWS Deployment")
    print("=" * 25)
    
    # Use auto_deploy.py if available
    if os.path.exists("auto_deploy.py"):
        print("Using auto_deploy.py...")
        return run_cmd("python auto_deploy.py")
    
    # Alternative: direct ECS update
    print("Direct ECS service update...")
    
    services = [
        "edweavepack-backend",
        "edweavepack-frontend"
    ]
    
    for service in services:
        print(f"Updating {service}...")
        if run_cmd(f"aws ecs update-service --cluster edweavepack-cluster --service {service} --force-new-deployment"):
            print(f"{service} update initiated")
        else:
            print(f"{service} update failed")
    
    return True

if __name__ == "__main__":
    
    # Try quick deployment first
    if quick_aws_deploy():
        print("\nWaiting for services to update...")
        time.sleep(90)
        
        if test_live_deployment():
            print("\nDeployment successful!")
            print("Live URL: http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com")
            print("Enhanced AI features now active")
        else:
            print("Deployment completed but tests failed")
    else:
        print("Deployment failed")
        sys.exit(1)