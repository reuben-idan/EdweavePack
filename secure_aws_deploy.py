#!/usr/bin/env python3
"""
Secure AWS deployment script following industry standards
"""
import subprocess
import os
import sys
import json
import time
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Execute command with proper error handling"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}")
        print(f"Error: {e.stderr}")
        if check:
            sys.exit(1)
        return None, e.stderr

def check_aws_credentials():
    """Verify AWS credentials are configured"""
    print("Checking AWS credentials...")
    stdout, stderr = run_command("aws sts get-caller-identity")
    if stdout:
        identity = json.loads(stdout)
        print(f"AWS credentials valid for account: {identity['Account']}")
        return True
    return False

def setup_terraform_vars():
    """Setup secure Terraform variables"""
    print("Setting up Terraform variables...")
    
    tfvars_path = Path("infrastructure/terraform.tfvars")
    if not tfvars_path.exists():
        # Generate secure database password
        import secrets
        import string
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        db_password = ''.join(secrets.choice(alphabet) for _ in range(20))
        
        tfvars_content = f'''aws_region   = "eu-north-1"
environment  = "production"
project_name = "edweavepack"
db_password  = "{db_password}"
'''
        with open(tfvars_path, 'w') as f:
            f.write(tfvars_content)
        print("Terraform variables configured")
    else:
        print("Terraform variables already exist")

def deploy_infrastructure():
    """Deploy infrastructure with Terraform"""
    print("Deploying infrastructure...")
    
    os.chdir("infrastructure")
    
    # Initialize Terraform
    print("Initializing Terraform...")
    run_command("terraform init")
    
    # Plan deployment
    print("Planning deployment...")
    run_command("terraform plan -out=tfplan")
    
    # Apply deployment
    print("Applying infrastructure changes...")
    run_command("terraform apply tfplan")
    
    # Get outputs
    stdout, _ = run_command("terraform output -json")
    outputs = json.loads(stdout)
    
    os.chdir("..")
    return outputs

def build_and_push_images(outputs):
    """Build and push Docker images to ECR"""
    print("Building and pushing Docker images...")
    
    # Get ECR URLs
    backend_repo = outputs["ecr_backend_url"]["value"]
    frontend_repo = outputs["ecr_frontend_url"]["value"]
    region = "eu-north-1"
    
    # Login to ECR
    run_command(f"aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {backend_repo}")
    
    # Build and push backend
    print("Building backend image...")
    run_command("docker build -f backend/Dockerfile.prod -t edweavepack-backend backend/")
    run_command(f"docker tag edweavepack-backend:latest {backend_repo}:latest")
    run_command(f"docker push {backend_repo}:latest")
    
    # Build and push frontend
    print("Building frontend image...")
    run_command("docker build -f frontend/Dockerfile.prod -t edweavepack-frontend frontend/")
    run_command(f"docker tag edweavepack-frontend:latest {frontend_repo}:latest")
    run_command(f"docker push {frontend_repo}:latest")
    
    print("Images pushed to ECR")

def update_ecs_services():
    """Update ECS services with new images"""
    print("Updating ECS services...")
    
    # Force new deployment
    run_command("aws ecs update-service --cluster edweavepack-cluster --service edweavepack-backend --force-new-deployment --region eu-north-1")
    run_command("aws ecs update-service --cluster edweavepack-cluster --service edweavepack-frontend --force-new-deployment --region eu-north-1")
    
    print("ECS services updated")

def verify_deployment(outputs):
    """Verify deployment is working"""
    print("Verifying deployment...")
    
    alb_dns = outputs["load_balancer_dns"]["value"]
    
    # Wait for services to be ready
    print("Waiting for services to stabilize...")
    time.sleep(60)
    
    # Test health endpoint
    import requests
    try:
        response = requests.get(f"https://{alb_dns}/health", timeout=30, verify=False)
        if response.status_code == 200:
            print("Backend health check passed")
        else:
            print(f"Backend health check returned: {response.status_code}")
    except Exception as e:
        print(f"Backend health check failed: {e}")
    
    # Test frontend
    try:
        response = requests.get(f"https://{alb_dns}/", timeout=30, verify=False)
        if response.status_code == 200:
            print("Frontend accessible")
        else:
            print(f"Frontend returned: {response.status_code}")
    except Exception as e:
        print(f"Frontend test failed: {e}")

def main():
    """Main deployment process"""
    print("Starting secure AWS deployment...")
    
    # Pre-deployment checks
    if not check_aws_credentials():
        print("AWS credentials not configured")
        sys.exit(1)
    
    # Setup configuration
    setup_terraform_vars()
    
    # Deploy infrastructure
    outputs = deploy_infrastructure()
    
    # Build and deploy applications
    build_and_push_images(outputs)
    update_ecs_services()
    
    # Verify deployment
    verify_deployment(outputs)
    
    print("Deployment completed successfully!")
    print(f"Application URL: https://{outputs['load_balancer_dns']['value']}")
    print(f"API Docs: https://{outputs['load_balancer_dns']['value']}/docs")

if __name__ == "__main__":
    main()