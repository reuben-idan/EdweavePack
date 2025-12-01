#!/usr/bin/env python3

import boto3
import json

def create_new_task_definition():
    """Create new task definition with updated backend"""
    try:
        ecs = boto3.client('ecs', region_name='eu-north-1')
        
        # Create new task definition
        task_definition = {
            "family": "edweavepack-auth-ready",
            "networkMode": "awsvpc",
            "requiresCompatibilities": ["FARGATE"],
            "cpu": "512",
            "memory": "1024",
            "executionRoleArn": "arn:aws:iam::084828575963:role/ecsTaskExecutionRole",
            "containerDefinitions": [
                {
                    "name": "backend",
                    "image": "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-backend:latest",
                    "portMappings": [
                        {
                            "containerPort": 8000,
                            "protocol": "tcp"
                        }
                    ],
                    "essential": True,
                    "logConfiguration": {
                        "logDriver": "awslogs",
                        "options": {
                            "awslogs-group": "/ecs/edweavepack",
                            "awslogs-region": "eu-north-1",
                            "awslogs-stream-prefix": "backend"
                        }
                    },
                    "environment": [
                        {"name": "PORT", "value": "8000"},
                        {"name": "NODE_ENV", "value": "production"}
                    ]
                },
                {
                    "name": "frontend", 
                    "image": "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-frontend:latest",
                    "portMappings": [
                        {
                            "containerPort": 80,
                            "protocol": "tcp"
                        }
                    ],
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
        
        response = ecs.register_task_definition(**task_definition)
        
        task_def_arn = response['taskDefinition']['taskDefinitionArn']
        print(f"Created task definition: {task_def_arn}")
        
        return task_def_arn
        
    except Exception as e:
        print(f"Error creating task definition: {e}")
        return None

def update_service_with_new_task_def(task_def_arn):
    """Update service to use new task definition"""
    try:
        ecs = boto3.client('ecs', region_name='eu-north-1')
        
        cluster_name = 'edweavepack-cluster'
        service_name = 'edweavepack-service'
        
        response = ecs.update_service(
            cluster=cluster_name,
            service=service_name,
            taskDefinition=task_def_arn,
            forceNewDeployment=True
        )
        
        print(f"Service updated with new task definition")
        return True
        
    except Exception as e:
        print(f"Error updating service: {e}")
        return False

def main():
    print("Updating Task Definition with Auth Backend")
    print("=" * 45)
    
    # Create new task definition
    task_def_arn = create_new_task_definition()
    if not task_def_arn:
        print("Failed to create task definition")
        return
    
    # Update service
    if not update_service_with_new_task_def(task_def_arn):
        print("Failed to update service")
        return
    
    print("\nTask definition updated successfully!")
    print("Service will redeploy with auth endpoints in ~2-3 minutes")

if __name__ == "__main__":
    main()