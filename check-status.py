#!/usr/bin/env python3

import boto3
import requests

def check_deployment():
    """Check current deployment status"""
    try:
        ecs = boto3.client('ecs', region_name='eu-north-1')
        
        # Check service status
        service = ecs.describe_services(
            cluster='edweavepack-cluster',
            services=['edweavepack-service']
        )['services'][0]
        
        print(f"Service Status: {service['status']}")
        print(f"Running Tasks: {service['runningCount']}/{service['desiredCount']}")
        print(f"Task Definition: {service['taskDefinition'].split('/')[-1]}")
        
        # Check tasks
        tasks = ecs.list_tasks(
            cluster='edweavepack-cluster',
            serviceName='edweavepack-service'
        )['taskArns']
        
        if tasks:
            task_details = ecs.describe_tasks(
                cluster='edweavepack-cluster',
                tasks=tasks
            )['tasks']
            
            for task in task_details:
                print(f"Task: {task['lastStatus']}")
                for container in task.get('containers', []):
                    print(f"  {container['name']}: {container['lastStatus']}")
        
        # Test endpoints
        base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
        
        endpoints = ["/", "/api/health", "/api/auth/register"]
        for endpoint in endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
                print(f"{endpoint}: {response.status_code}")
            except:
                print(f"{endpoint}: ERROR")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_deployment()