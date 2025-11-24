#!/usr/bin/env python3

import subprocess
import time

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0

def complete_rebuild():
    print("TOTAL OVERHAUL REDEPLOYMENT")
    
    # 1. Build frontend with correct API URL
    print("Building frontend...")
    run_cmd("cd frontend && npm run build")
    
    # 2. Get ECR login
    print("ECR login...")
    success, token, _ = subprocess.run("aws ecr get-login-password --region eu-north-1", shell=True, capture_output=True, text=True).returncode == 0, subprocess.run("aws ecr get-login-password --region eu-north-1", shell=True, capture_output=True, text=True).stdout, ""
    
    if success:
        subprocess.run(f'echo {token.strip()} | docker login --username AWS --password-stdin 084828575963.dkr.ecr.eu-north-1.amazonaws.com', shell=True)
    
    # 3. Force rebuild images
    print("Rebuilding Docker images...")
    ecr_url = "084828575963.dkr.ecr.eu-north-1.amazonaws.com"
    
    # Backend
    run_cmd("docker build --no-cache -t edweavepack-backend backend/")
    run_cmd(f"docker tag edweavepack-backend:latest {ecr_url}/edweavepack-backend:latest")
    run_cmd(f"docker push {ecr_url}/edweavepack-backend:latest")
    
    # Frontend
    run_cmd("docker build --no-cache -t edweavepack-frontend frontend/")
    run_cmd(f"docker tag edweavepack-frontend:latest {ecr_url}/edweavepack-frontend:latest")
    run_cmd(f"docker push {ecr_url}/edweavepack-frontend:latest")
    
    # 4. Restart service
    print("Restarting ECS service...")
    run_cmd("aws ecs update-service --cluster edweavepack-cluster --service edweavepack-service --desired-count 2 --force-new-deployment --region eu-north-1")
    
    print("COMPLETE REBUILD INITIATED")

if __name__ == "__main__":
    complete_rebuild()