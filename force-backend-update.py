#!/usr/bin/env python3

import boto3
import json

def force_backend_update():
    """Force ECS service to use latest backend with upload endpoints"""
    
    ecs = boto3.client('ecs', region_name='eu-north-1')
    
    print("Creating new task definition with upload endpoints...")
    
    # Create new task definition
    task_def = {
        "family": "edweavepack-upload-ready",
        "networkMode": "awsvpc",
        "requiresCompatibilities": ["FARGATE"],
        "cpu": "512",
        "memory": "1024",
        "executionRoleArn": "arn:aws:iam::084828575963:role/ecsTaskExecutionRole",
        "containerDefinitions": [
            {
                "name": "backend",
                "image": "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-backend:latest",
                "portMappings": [{"containerPort": 8000, "protocol": "tcp"}],
                "essential": True,
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": "/ecs/edweavepack",
                        "awslogs-region": "eu-north-1",
                        "awslogs-stream-prefix": "backend"
                    }
                }
            },
            {
                "name": "frontend",
                "image": "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-frontend:latest",
                "portMappings": [{"containerPort": 80, "protocol": "tcp"}],
                "essential": True,
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": "/ecs/edweavepack",
                        "awslogs-region": "eu-north-1",
                        "awslogs-stream-prefix": "frontend"
                    }
                }
            }
        ]
    }
    
    # Register new task definition
    response = ecs.register_task_definition(**task_def)
    new_task_arn = response['taskDefinition']['taskDefinitionArn']
    print(f"New task definition: {new_task_arn}")
    
    # Update service to use new task definition
    print("Updating service...")
    ecs.update_service(
        cluster='edweavepack-cluster',
        service='edweavepack-service',
        taskDefinition=new_task_arn,
        forceNewDeployment=True
    )
    
    print("Service updated - backend endpoints will be available in 2-3 minutes")

if __name__ == "__main__":
    force_backend_update()