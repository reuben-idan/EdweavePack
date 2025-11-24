#!/usr/bin/env python3

import subprocess
import sys
import os
import time
import json

def run_command(cmd, cwd=None):
    """Run command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=300)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"

def check_aws_credentials():
    """Check if AWS credentials are configured"""
    success, stdout, stderr = run_command("aws sts get-caller-identity")
    if success:
        print("OK AWS credentials configured")
        return True
    else:
        print("ERROR AWS credentials not configured")
        return False

def build_and_push_images():
    """Build and push Docker images to ECR"""
    print("Building Docker images...")
    
    # Get ECR login
    success, token, _ = run_command("aws ecr get-login-password --region eu-north-1")
    if not success:
        return False
    
    # Login to ECR
    ecr_url = "084828575963.dkr.ecr.eu-north-1.amazonaws.com"
    success, _, _ = run_command(f'echo {token.strip()} | docker login --username AWS --password-stdin {ecr_url}')
    if not success:
        return False
    
    # Build backend
    print("Building backend image...")
    success, _, _ = run_command("docker build -t edweavepack-backend .", cwd="backend")
    if not success:
        return False
    
    # Build frontend  
    print("Building frontend image...")
    success, _, _ = run_command("docker build -t edweavepack-frontend .", cwd="frontend")
    if not success:
        return False
    
    # Tag and push backend
    backend_repo = f"{ecr_url}/edweavepack-backend"
    run_command(f"docker tag edweavepack-backend:latest {backend_repo}:latest")
    success, _, _ = run_command(f"docker push {backend_repo}:latest")
    if not success:
        return False
    
    # Tag and push frontend
    frontend_repo = f"{ecr_url}/edweavepack-frontend"
    run_command(f"docker tag edweavepack-frontend:latest {frontend_repo}:latest")
    success, _, _ = run_command(f"docker push {frontend_repo}:latest")
    if not success:
        return False
    
    print("OK Images pushed to ECR")
    return True

def update_ecs_service():
    """Force ECS service update"""
    print("Updating ECS service...")
    success, _, _ = run_command("aws ecs update-service --cluster edweavepack-cluster --service edweavepack-service --force-new-deployment --region eu-north-1")
    if success:
        print("OK ECS service updated")
        return True
    return False

def wait_for_deployment():
    """Wait for deployment to complete"""
    print("Waiting for deployment to complete...")
    for i in range(30):  # Wait up to 15 minutes
        success, stdout, _ = run_command("aws ecs describe-services --cluster edweavepack-cluster --services edweavepack-service --region eu-north-1")
        if success:
            try:
                data = json.loads(stdout)
                service = data['services'][0]
                running_count = service['runningCount']
                desired_count = service['desiredCount']
                
                if running_count == desired_count and running_count > 0:
                    print("OK Deployment completed successfully")
                    return True
                    
                print(f"Deployment in progress... ({running_count}/{desired_count})")
            except:
                pass
        
        time.sleep(30)
    
    print("ERROR Deployment timeout")
    return False

def get_application_url():
    """Get the application URL"""
    success, stdout, _ = run_command("aws elbv2 describe-load-balancers --region eu-north-1")
    if success:
        try:
            data = json.loads(stdout)
            for lb in data['LoadBalancers']:
                if 'edweavepack' in lb['LoadBalancerName']:
                    return f"http://{lb['DNSName']}"
        except:
            pass
    return "Check AWS Console for URL"

def main():
    print("Starting robust AWS deployment...")
    
    # Check prerequisites
    if not check_aws_credentials():
        print("Please configure AWS credentials: aws configure")
        return False
    
    # Build and push images
    if not build_and_push_images():
        print("ERROR Failed to build/push images")
        return False
    
    # Update ECS service
    if not update_ecs_service():
        print("ERROR Failed to update ECS service")
        return False
    
    # Wait for deployment
    if not wait_for_deployment():
        print("ERROR Deployment may have failed")
        return False
    
    # Get URL
    url = get_application_url()
    
    print("\n" + "="*50)
    print("DEPLOYMENT SUCCESSFUL!")
    print("="*50)
    print(f"Application URL: {url}")
    print(f"API Documentation: {url}/docs")
    print("="*50)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)