#!/usr/bin/env python3
import boto3
import subprocess
import sys

AWS_REGION = 'eu-north-1'
AWS_ACCESS_KEY = 'AKIARHQBNLDN6T3PP7IK'
AWS_SECRET_KEY = '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'

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def deploy():
    print("Deploying EdweavePack with AWS AI services...")
    
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )
    
    ecr = session.client('ecr')
    ecs = session.client('ecs')
    account_id = session.client('sts').get_caller_identity()['Account']
    
    # ECR login
    token = ecr.get_authorization_token()
    registry = token['authorizationData'][0]['proxyEndpoint'].replace('https://', '')
    
    print("ECR authentication...")
    success, _, _ = run_cmd(f"aws ecr get-login-password --region {AWS_REGION} | docker login --username AWS --password-stdin {registry}")
    if not success:
        return False
    
    # Build backend
    print("Building backend...")
    success, _, _ = run_cmd("docker build -t edweavepack-backend .", cwd="backend")
    if not success:
        return False
    
    run_cmd(f"docker tag edweavepack-backend:latest {registry}/edweavepack-backend:latest")
    success, _, _ = run_cmd(f"docker push {registry}/edweavepack-backend:latest")
    if not success:
        return False
    
    # Build frontend
    print("Building frontend...")
    success, _, _ = run_cmd("docker build -t edweavepack-frontend .", cwd="frontend")
    if not success:
        return False
    
    run_cmd(f"docker tag edweavepack-frontend:latest {registry}/edweavepack-frontend:latest")
    success, _, _ = run_cmd(f"docker push {registry}/edweavepack-frontend:latest")
    if not success:
        return False
    
    # Create task definition
    task_def = {
        "family": "edweavepack-ai-production",
        "networkMode": "awsvpc",
        "requiresCompatibilities": ["FARGATE"],
        "cpu": "1024",
        "memory": "2048",
        "executionRoleArn": f"arn:aws:iam::{account_id}:role/ecsTaskExecutionRole",
        "taskRoleArn": f"arn:aws:iam::{account_id}:role/ecsTaskRole",
        "containerDefinitions": [
            {
                "name": "backend",
                "image": f"{registry}/edweavepack-backend:latest",
                "portMappings": [{"containerPort": 8000}],
                "essential": True,
                "environment": [
                    {"name": "AWS_REGION", "value": AWS_REGION},
                    {"name": "ENVIRONMENT", "value": "production"},
                    {"name": "BEDROCK_MODEL_ID", "value": "anthropic.claude-3-5-sonnet-20241022-v2:0"},
                    {"name": "DATABASE_URL", "value": "sqlite:///./edweavepack.db"}
                ],
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": "/ecs/edweavepack-ai",
                        "awslogs-region": AWS_REGION,
                        "awslogs-stream-prefix": "backend",
                        "awslogs-create-group": "true"
                    }
                }
            },
            {
                "name": "frontend",
                "image": f"{registry}/edweavepack-frontend:latest",
                "portMappings": [{"containerPort": 80}],
                "essential": True,
                "environment": [
                    {"name": "REACT_APP_API_URL", "value": "http://edweavepack-alb-420811343.eu-north-1.elb.amazonaws.com"},
                    {"name": "REACT_APP_AI_ENABLED", "value": "true"}
                ],
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": "/ecs/edweavepack-ai",
                        "awslogs-region": AWS_REGION,
                        "awslogs-stream-prefix": "frontend",
                        "awslogs-create-group": "true"
                    }
                }
            }
        ]
    }
    
    # Register and deploy
    response = ecs.register_task_definition(**task_def)
    task_arn = response['taskDefinition']['taskDefinitionArn']
    
    try:
        ecs.update_service(
            cluster='edweavepack-cluster',
            service='edweavepack-service',
            taskDefinition=task_arn,
            forceNewDeployment=True
        )
    except:
        ecs.create_service(
            cluster='edweavepack-cluster',
            serviceName='edweavepack-service',
            taskDefinition=task_arn,
            desiredCount=1,
            launchType='FARGATE',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': ['subnet-009bad7f046d644b4', 'subnet-08e77dcadd69e0b7e'],
                    'securityGroups': ['sg-0b1185b83388e7d68'],
                    'assignPublicIp': 'ENABLED'
                }
            }
        )
    
    print("Deployment completed!")
    print("URL: http://edweavepack-alb-420811343.eu-north-1.elb.amazonaws.com")
    print("AI Services: Bedrock, Textract, Comprehend, Polly, Translate")
    return True

if __name__ == "__main__":
    success = deploy()
    sys.exit(0 if success else 1)