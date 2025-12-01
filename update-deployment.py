#!/usr/bin/env python3
import boto3

AWS_REGION = 'eu-north-1'
AWS_ACCESS_KEY = 'AKIARHQBNLDN6T3PP7IK'
AWS_SECRET_KEY = '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'

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

ecs = session.client('ecs')
account_id = session.client('sts').get_caller_identity()['Account']

# Update task definition with correct ALB URL
task_def = {
    "family": "edweavepack-final",
    "networkMode": "awsvpc",
    "requiresCompatibilities": ["FARGATE"],
    "cpu": "1024",
    "memory": "2048",
    "executionRoleArn": f"arn:aws:iam::{account_id}:role/ecsTaskExecutionRole",
    "taskRoleArn": f"arn:aws:iam::{account_id}:role/ecsTaskRole",
    "containerDefinitions": [
        {
            "name": "backend",
            "image": f"{account_id}.dkr.ecr.{AWS_REGION}.amazonaws.com/edweavepack-backend:latest",
            "portMappings": [{"containerPort": 8000}],
            "essential": True,
            "environment": [
                {"name": "AWS_REGION", "value": AWS_REGION},
                {"name": "ENVIRONMENT", "value": "production"},
                {"name": "BEDROCK_MODEL_ID", "value": "anthropic.claude-3-5-sonnet-20241022-v2:0"},
                {"name": "DATABASE_URL", "value": "sqlite:///./app.db"},
                {"name": "JWT_SECRET", "value": "production-secret-key-2025"}
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/edweavepack-final",
                    "awslogs-region": AWS_REGION,
                    "awslogs-stream-prefix": "backend",
                    "awslogs-create-group": "true"
                }
            }
        },
        {
            "name": "frontend",
            "image": f"{account_id}.dkr.ecr.{AWS_REGION}.amazonaws.com/edweavepack-frontend:latest",
            "portMappings": [{"containerPort": 80}],
            "essential": True,
            "environment": [
                {"name": "REACT_APP_API_URL", "value": "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"},
                {"name": "REACT_APP_VERSION", "value": "3.0.0"},
                {"name": "REACT_APP_AI_ENABLED", "value": "true"}
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/edweavepack-final",
                    "awslogs-region": AWS_REGION,
                    "awslogs-stream-prefix": "frontend",
                    "awslogs-create-group": "true"
                }
            }
        }
    ]
}

response = ecs.register_task_definition(**task_def)
task_arn = response['taskDefinition']['taskDefinitionArn']

# Update service
ecs.update_service(
    cluster='edweavepack-cluster',
    service='edweavepack-service',
    taskDefinition=task_arn,
    forceNewDeployment=True
)

print("Deployment updated with correct ALB URL")
print("URL: http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com")
print("Wait 2-3 minutes for deployment to complete")