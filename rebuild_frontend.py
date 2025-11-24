#!/usr/bin/env python3

import subprocess
import json
import tempfile

def run_command(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result.returncode == 0, result.stdout, result.stderr

def rebuild_frontend():
    """Rebuild frontend with correct API URL and update ECS"""
    
    # Create new Dockerfile with environment variable
    dockerfile_content = '''FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
ENV REACT_APP_API_URL=http://edweavepack-alb-1353441079.eu-north-1.elb.amazonaws.com
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]'''
    
    with open('frontend/Dockerfile.new', 'w') as f:
        f.write(dockerfile_content)
    
    # Get ECR login
    success, token, _ = run_command("aws ecr get-login-password --region eu-north-1")
    if not success:
        print("ERROR: Failed to get ECR token")
        return False
    
    # Login to ECR
    ecr_url = "084828575963.dkr.ecr.eu-north-1.amazonaws.com"
    success, _, _ = run_command(f'echo {token.strip()} | docker login --username AWS --password-stdin {ecr_url}')
    if not success:
        print("ERROR: Failed to login to ECR")
        return False
    
    # Build new frontend image
    success, _, stderr = run_command("docker build -f Dockerfile.new -t edweavepack-frontend-fixed .", cwd="frontend")
    if not success:
        print(f"ERROR: Failed to build frontend: {stderr}")
        return False
    
    # Tag and push
    frontend_repo = f"{ecr_url}/edweavepack-frontend"
    run_command(f"docker tag edweavepack-frontend-fixed:latest {frontend_repo}:latest")
    success, _, _ = run_command(f"docker push {frontend_repo}:latest")
    if not success:
        print("ERROR: Failed to push frontend")
        return False
    
    # Force ECS update
    success, _, _ = run_command("aws ecs update-service --cluster edweavepack-cluster --service edweavepack-service --force-new-deployment --region eu-north-1")
    if success:
        print("SUCCESS: Frontend rebuilt and deployed")
        return True
    else:
        print("ERROR: Failed to update ECS service")
        return False

if __name__ == "__main__":
    rebuild_frontend()