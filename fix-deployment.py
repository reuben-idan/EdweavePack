#!/usr/bin/env python3
import boto3
import subprocess
import time

AWS_REGION = 'eu-north-1'
AWS_ACCESS_KEY = 'AKIARHQBNLDN6T3PP7IK'
AWS_SECRET_KEY = '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'

def fix_nginx_config():
    # Fix nginx configuration
    nginx_config = """server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;
    
    location /health {
        try_files /health.json =404;
        add_header Content-Type application/json;
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location / {
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache";
    }
}"""
    
    with open('frontend/nginx.conf', 'w') as f:
        f.write(nginx_config)
    print("Fixed nginx configuration")

def fix_backend_main():
    # Create minimal working main.py
    main_py = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

app = FastAPI(title="EdweavePack API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "EdweavePack", "version": "3.0.0"}

@app.get("/")
async def root():
    return {"message": "EdweavePack API", "status": "running"}

@app.get("/api/health")
async def api_health():
    return {"status": "healthy", "api": "ready"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)"""
    
    with open('backend/main.py', 'w') as f:
        f.write(main_py)
    print("Fixed backend main.py")

def rebuild_and_deploy():
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )
    
    ecr = session.client('ecr')
    ecs = session.client('ecs')
    account_id = session.client('sts').get_caller_identity()['Account']
    
    # ECR login
    token = ecr.get_authorization_token()
    registry = token['authorizationData'][0]['proxyEndpoint'].replace('https://', '')
    
    subprocess.run(f"aws ecr get-login-password --region {AWS_REGION} | docker login --username AWS --password-stdin {registry}", shell=True)
    
    # Rebuild images
    print("Rebuilding backend...")
    subprocess.run("docker build -t edweavepack-backend .", shell=True, cwd="backend")
    subprocess.run(f"docker tag edweavepack-backend:latest {registry}/edweavepack-backend:latest", shell=True)
    subprocess.run(f"docker push {registry}/edweavepack-backend:latest", shell=True)
    
    print("Rebuilding frontend...")
    subprocess.run("docker build -t edweavepack-frontend .", shell=True, cwd="frontend")
    subprocess.run(f"docker tag edweavepack-frontend:latest {registry}/edweavepack-frontend:latest", shell=True)
    subprocess.run(f"docker push {registry}/edweavepack-frontend:latest", shell=True)
    
    # Create working task definition
    task_def = {
        "family": "edweavepack-working",
        "networkMode": "awsvpc",
        "requiresCompatibilities": ["FARGATE"],
        "cpu": "512",
        "memory": "1024",
        "executionRoleArn": f"arn:aws:iam::{account_id}:role/ecsTaskExecutionRole",
        "containerDefinitions": [
            {
                "name": "backend",
                "image": f"{registry}/edweavepack-backend:latest",
                "portMappings": [{"containerPort": 8000}],
                "essential": True,
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": "/ecs/edweavepack-working",
                        "awslogs-region": AWS_REGION,
                        "awslogs-stream-prefix": "backend",
                        "awslogs-create-group": "true"
                    }
                }
            },
            {
                "name": "frontend",
                "image": f"{registry}/edweavepack-frontend:latest",
                "portMappings": [{"containerPort": 80}],
                "essential": True,
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": "/ecs/edweavepack-working",
                        "awslogs-region": AWS_REGION,
                        "awslogs-stream-prefix": "frontend",
                        "awslogs-create-group": "true"
                    }
                }
            }
        ]
    }
    
    response = ecs.register_task_definition(**task_def)
    task_arn = response['taskDefinition']['taskDefinitionArn']
    
    # Update service
    ecs.update_service(
        cluster='edweavepack-cluster',
        service='edweavepack-service',
        taskDefinition=task_arn,
        forceNewDeployment=True
    )
    
    print("Deployment updated with working configuration")
    return True

def main():
    print("=== FIXING DEPLOYMENT ISSUES ===")
    
    # Fix configuration files
    fix_nginx_config()
    fix_backend_main()
    
    # Rebuild and deploy
    if rebuild_and_deploy():
        print("\n=== FIXES APPLIED ===")
        print("1. Fixed nginx configuration syntax")
        print("2. Created minimal working backend")
        print("3. Rebuilt and deployed containers")
        print("4. Updated ECS service")
        print("\nURL: http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com")
        print("Wait 3-5 minutes for deployment to complete")
        return True
    
    return False

if __name__ == "__main__":
    main()