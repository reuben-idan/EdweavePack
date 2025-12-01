#!/usr/bin/env python3

import boto3
import subprocess
import json
import time
import sys

def rebuild_frontend():
    """Rebuild frontend with correct ALB URL"""
    
    print("=== Rebuilding Frontend ===")
    
    # Build frontend image
    print("Building frontend image...")
    result = subprocess.run([
        "docker", "build", "-t", "edweavepack-frontend:latest", "."
    ], cwd="frontend", capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Build failed: {result.stderr}")
        return False
    
    print("Frontend built successfully")
    
    # Tag image
    print("Tagging image...")
    result = subprocess.run([
        "docker", "tag", "edweavepack-frontend:latest", 
        "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-frontend:latest"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Tag failed: {result.stderr}")
        return False
    
    print("Image tagged successfully")
    
    # Push image
    print("Pushing to ECR...")
    result = subprocess.run([
        "docker", "push", 
        "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-frontend:latest"
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

def main():
    print("EdweavePack Frontend Fix")
    print("=" * 40)
    
    # Rebuild frontend
    if not rebuild_frontend():
        print("Failed to rebuild frontend")
        sys.exit(1)
    
    # Update service
    if not update_service():
        print("Failed to update service")
        sys.exit(1)
    
    print("\nDeployment completed!")
    print("URL: http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com")

if __name__ == "__main__":
    main()