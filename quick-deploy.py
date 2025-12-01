#!/usr/bin/env python3

import subprocess
import boto3

def quick_deploy():
    """Quick deployment of auth fix"""
    
    print("Quick Auth Fix Deployment")
    print("=" * 25)
    
    # Build and push
    subprocess.run(["docker", "build", "-t", "edweavepack-backend:latest", "."], cwd="backend")
    subprocess.run(["docker", "tag", "edweavepack-backend:latest", 
                   "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-backend:latest"])
    subprocess.run(["docker", "push", 
                   "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-backend:latest"])
    
    # Update service
    ecs = boto3.client('ecs', region_name='eu-north-1')
    ecs.update_service(
        cluster='edweavepack-cluster',
        service='edweavepack-service',
        forceNewDeployment=True
    )
    
    print("Deployment initiated")

if __name__ == "__main__":
    quick_deploy()