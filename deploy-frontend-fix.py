#!/usr/bin/env python3

import subprocess
import boto3

def deploy_frontend():
    """Deploy frontend with upload page fixes"""
    
    print("Deploying Frontend Fix")
    print("=" * 22)
    
    # Build frontend
    result = subprocess.run([
        "docker", "build", "-t", "edweavepack-frontend:latest", "."
    ], cwd="frontend", capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Build failed: {result.stderr}")
        return False
    
    print("Frontend built")
    
    # Tag and push
    subprocess.run([
        "docker", "tag", "edweavepack-frontend:latest", 
        "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-frontend:latest"
    ])
    
    subprocess.run([
        "docker", "push", 
        "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-frontend:latest"
    ])
    
    print("Frontend pushed")
    
    # Update ECS
    ecs = boto3.client('ecs', region_name='eu-north-1')
    ecs.update_service(
        cluster='edweavepack-cluster',
        service='edweavepack-service',
        forceNewDeployment=True
    )
    
    print("Service updated")
    return True

if __name__ == "__main__":
    deploy_frontend()