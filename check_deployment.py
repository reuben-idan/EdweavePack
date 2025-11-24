#!/usr/bin/env python3

import subprocess
import json
import time

def check_ecs_status():
    """Check ECS deployment status"""
    try:
        result = subprocess.run([
            "aws", "ecs", "describe-services", 
            "--cluster", "edweavepack-cluster",
            "--services", "edweavepack-service",
            "--region", "eu-north-1"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data['services']:
                service = data['services'][0]
                print(f"Service Status: {service['status']}")
                print(f"Running Tasks: {service['runningCount']}/{service['desiredCount']}")
                print(f"Pending Tasks: {service['pendingCount']}")
                return True
        return False
    except Exception as e:
        print(f"Error checking ECS: {e}")
        return False

def get_load_balancer_url():
    """Get application URL"""
    try:
        result = subprocess.run([
            "aws", "elbv2", "describe-load-balancers",
            "--region", "eu-north-1"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            for lb in data['LoadBalancers']:
                if 'edweavepack' in lb.get('LoadBalancerName', ''):
                    url = f"http://{lb['DNSName']}"
                    print(f"Application URL: {url}")
                    return url
        return None
    except Exception as e:
        print(f"Error getting URL: {e}")
        return None

if __name__ == "__main__":
    print("Checking AWS deployment status...")
    
    if check_ecs_status():
        print("ECS service found")
        url = get_load_balancer_url()
        if url:
            print(f"\nAccess your application at: {url}")
            print(f"API Documentation: {url}/docs")
    else:
        print("ECS service not found or not accessible")
        print("Deployment may still be in progress via GitHub Actions")