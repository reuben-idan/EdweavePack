#!/usr/bin/env python3

import boto3
import requests

def check_running_services():
    """Check which services are actually running"""
    try:
        ecs = boto3.client('ecs', region_name='eu-north-1')
        
        # Check the main service
        cluster_name = 'edweavepack-cluster'
        service_name = 'edweavepack-service'
        
        service_details = ecs.describe_services(
            cluster=cluster_name,
            services=[service_name]
        )['services'][0]
        
        print(f"Service: {service_name}")
        print(f"Status: {service_details['status']}")
        print(f"Running: {service_details['runningCount']}")
        print(f"Task Definition: {service_details['taskDefinition']}")
        
        # Get task definition details
        task_def_arn = service_details['taskDefinition']
        task_def = ecs.describe_task_definition(taskDefinition=task_def_arn)
        
        print("\nContainer Definitions:")
        for container in task_def['taskDefinition']['containerDefinitions']:
            print(f"- {container['name']}: {container['image']}")
            if 'portMappings' in container:
                for port in container['portMappings']:
                    print(f"  Port: {port['containerPort']}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_direct_endpoints():
    """Test endpoints directly"""
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    endpoints = [
        "/",
        "/health", 
        "/api/health",
        "/api/auth/register",
        "/docs"
    ]
    
    print("\n=== Testing Endpoints ===")
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"{endpoint}: {response.status_code}")
        except Exception as e:
            print(f"{endpoint}: Error - {e}")

def main():
    print("Service Status Check")
    print("=" * 30)
    
    check_running_services()
    test_direct_endpoints()

if __name__ == "__main__":
    main()