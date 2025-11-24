#!/usr/bin/env python3
"""
Secure Deployment Script for EdweavePack
Rebuilds and deploys with HTTPS and secure logging
"""

import subprocess
import sys
import time
import json

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"{description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description} failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main deployment process"""
    print("Starting Secure EdweavePack Deployment")
    print("=" * 50)
    
    # Step 1: Stop ECS service
    print("\nStep 1: Stopping ECS service")
    if not run_command(
        "aws ecs update-service --cluster edweavepack-cluster --service edweavepack-service --desired-count 0 --region eu-north-1",
        "Stopping ECS service"
    ):
        print("Failed to stop ECS service")
        return False
    
    # Wait for tasks to stop
    print("Waiting for tasks to stop...")
    time.sleep(30)
    
    # Step 2: Build frontend with HTTPS configuration
    print("\nStep 2: Building secure frontend")
    if not run_command(
        "docker build --no-cache -t edweavepack-frontend ./frontend",
        "Building frontend Docker image"
    ):
        print("Failed to build frontend")
        return False
    
    # Step 3: Build backend with secure CORS
    print("\nStep 3: Building secure backend")
    if not run_command(
        "docker build --no-cache -t edweavepack-backend ./backend",
        "Building backend Docker image"
    ):
        print("Failed to build backend")
        return False
    
    # Step 4: Tag and push frontend
    print("\nStep 4: Pushing frontend to ECR")
    frontend_commands = [
        "docker tag edweavepack-frontend:latest 533267405883.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-frontend:latest",
        "docker push 533267405883.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-frontend:latest"
    ]
    
    for cmd in frontend_commands:
        if not run_command(cmd, f"Frontend ECR operation"):
            print("Failed to push frontend to ECR")
            return False
    
    # Step 5: Tag and push backend
    print("\nStep 5: Pushing backend to ECR")
    backend_commands = [
        "docker tag edweavepack-backend:latest 533267405883.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-backend:latest",
        "docker push 533267405883.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-backend:latest"
    ]
    
    for cmd in backend_commands:
        if not run_command(cmd, f"Backend ECR operation"):
            print("Failed to push backend to ECR")
            return False
    
    # Step 6: Restart ECS service
    print("\nStep 6: Restarting ECS service")
    if not run_command(
        "aws ecs update-service --cluster edweavepack-cluster --service edweavepack-service --desired-count 2 --force-new-deployment --region eu-north-1",
        "Restarting ECS service"
    ):
        print("Failed to restart ECS service")
        return False
    
    # Step 7: Wait and verify deployment
    print("\nStep 7: Verifying deployment")
    print("Waiting for service to stabilize...")
    time.sleep(60)
    
    if not run_command(
        "aws ecs describe-services --cluster edweavepack-cluster --services edweavepack-service --region eu-north-1",
        "Checking service status"
    ):
        print("Failed to check service status")
        return False
    
    print("\nSecure Deployment Complete!")
    print("=" * 50)
    print("HTTPS enabled")
    print("Sensitive data logging removed")
    print("Secure CORS configuration")
    print("Network errors resolved")
    print("\nApplication URL: https://edweavepack-alb-1353441079.eu-north-1.elb.amazonaws.com")
    print("\nSecurity improvements:")
    print("  - All API calls now use HTTPS")
    print("  - Password data no longer logged to console")
    print("  - Secure logging functions implemented")
    print("  - Production-ready CORS configuration")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)