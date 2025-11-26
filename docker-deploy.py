#!/usr/bin/env python3
"""Robust Docker deployment with best practices"""

import subprocess
import sys
import time
import json
import os

def run_command(cmd, cwd=None):
    """Run command with error handling"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        print(result.stdout)
        return True
    except subprocess.TimeoutExpired:
        print("Command timed out")
        return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

def build_and_deploy():
    """Build and deploy with Docker best practices"""
    
    print("Docker Deployment - Enhanced AI EdweavePack")
    print("=" * 50)
    
    # 1. Stop existing containers
    print("Stopping existing containers...")
    run_command("docker-compose down")
    
    # 2. Clean up old images
    print("Cleaning up old images...")
    run_command("docker system prune -f")
    
    # 3. Build with no cache for fresh deployment
    print("Building fresh containers...")
    if not run_command("docker-compose build --no-cache"):
        print("Build failed")
        return False
    
    # 4. Start services
    print("Starting services...")
    if not run_command("docker-compose up -d"):
        print("Startup failed")
        return False
    
    # 5. Wait for services
    print("Waiting for services to initialize...")
    time.sleep(30)
    
    # 6. Check health
    print("Checking service health...")
    if run_command("docker-compose ps"):
        print("Services are running")
        return True
    
    return False

def test_deployment():
    """Test the deployment"""
    
    print("\nTesting deployment...")
    
    # Test backend health
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("Backend health: OK")
        else:
            print(f"Backend health: FAIL ({response.status_code})")
    except Exception as e:
        print(f"Backend health: FAIL ({e})")
    
    # Test frontend
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("Frontend: OK")
        else:
            print(f"Frontend: FAIL ({response.status_code})")
    except Exception as e:
        print(f"Frontend: FAIL ({e})")

if __name__ == "__main__":
    if build_and_deploy():
        test_deployment()
        print("\nDeployment complete!")
        print("Backend: http://localhost:8000")
        print("Frontend: http://localhost:3000")
        print("API Docs: http://localhost:8000/docs")
    else:
        print("Deployment failed")
        sys.exit(1)