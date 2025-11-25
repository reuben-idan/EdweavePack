#!/usr/bin/env python3
"""
Network issues fix script for EdweavePack
Applies network configuration fixes and validates deployment
"""

import subprocess
import sys
import time
import os

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"OK {cmd}")
            return True
        else:
            print(f"ERROR {cmd}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"ERROR Failed to run {cmd}: {e}")
        return False

def apply_terraform_changes():
    """Apply Terraform infrastructure changes"""
    print("Applying Terraform changes...")
    
    terraform_dir = "infrastructure"
    commands = [
        "terraform init",
        "terraform plan -out=tfplan",
        "terraform apply tfplan"
    ]
    
    for cmd in commands:
        if not run_command(cmd, cwd=terraform_dir):
            return False
    
    return True

def rebuild_containers():
    """Rebuild and push container images"""
    print("Rebuilding containers...")
    
    commands = [
        "docker-compose build --no-cache",
        "docker-compose up -d"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            return False
    
    return True

def wait_for_services():
    """Wait for services to become healthy"""
    print("Waiting for services to start...")
    time.sleep(30)
    
    # Test local services
    import requests
    
    services = [
        ("Backend", "http://localhost:8000/health"),
        ("Frontend", "http://localhost:3000")
    ]
    
    for name, url in services:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"OK {name} is healthy")
            else:
                print(f"WARN {name} returned status {response.status_code}")
        except Exception as e:
            print(f"ERROR {name} is not responding: {e}")

def main():
    """Main fix process"""
    print("EdweavePack Network Fix")
    print("=" * 30)
    
    # Check if we're in the right directory
    if not os.path.exists("docker-compose.yml"):
        print("ERROR Please run this script from the EdweavePack root directory")
        sys.exit(1)
    
    # Apply fixes step by step
    steps = [
        ("Rebuilding containers", rebuild_containers),
        ("Waiting for services", wait_for_services)
    ]
    
    # Only apply Terraform if in production
    if os.getenv("APPLY_TERRAFORM", "false").lower() == "true":
        steps.insert(0, ("Applying Terraform changes", apply_terraform_changes))
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"ERROR {step_name} failed!")
            sys.exit(1)
    
    print("\nNetwork fixes applied successfully!")
    print("\nNext steps:")
    print("1. Test local endpoints: http://localhost:3000 and http://localhost:8000")
    print("2. Run validation: python validate_network.py")
    print("3. For production: set APPLY_TERRAFORM=true and re-run")

if __name__ == "__main__":
    main()