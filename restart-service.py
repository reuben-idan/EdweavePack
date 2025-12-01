#!/usr/bin/env python3

import boto3
import time

def restart_service():
    """Restart ECS service completely"""
    
    ecs = boto3.client('ecs', region_name='eu-north-1')
    
    print("Restarting ECS service...")
    
    # Stop all tasks
    print("Stopping current tasks...")
    tasks = ecs.list_tasks(
        cluster='edweavepack-cluster',
        serviceName='edweavepack-service'
    )['taskArns']
    
    for task in tasks:
        ecs.stop_task(
            cluster='edweavepack-cluster',
            task=task,
            reason='Force restart for upload endpoints'
        )
    
    # Wait for tasks to stop
    print("Waiting for tasks to stop...")
    time.sleep(30)
    
    # Force new deployment
    print("Starting new deployment...")
    ecs.update_service(
        cluster='edweavepack-cluster',
        service='edweavepack-service',
        forceNewDeployment=True
    )
    
    print("Service restart initiated")
    print("Upload endpoints should be available in 3-4 minutes")

if __name__ == "__main__":
    restart_service()