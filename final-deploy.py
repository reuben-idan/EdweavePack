#!/usr/bin/env python3
import boto3
import subprocess
import sys
import time

AWS_REGION = 'eu-north-1'
AWS_ACCESS_KEY = 'AKIARHQBNLDN6T3PP7IK'
AWS_SECRET_KEY = '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'

def run_cmd(cmd, cwd=None, timeout=300):
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def deploy():
    print("=== EdweavePack AWS AI Deployment ===")
    
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )
    
    ecr = session.client('ecr')
    ecs = session.client('ecs')
    account_id = session.client('sts').get_caller_identity()['Account']
    
    # ECR setup
    token = ecr.get_authorization_token()
    registry = token['authorizationData'][0]['proxyEndpoint'].replace('https://', '')
    
    print("1. ECR Authentication...")
    success, _, _ = run_cmd(f"aws ecr get-login-password --region {AWS_REGION} | docker login --username AWS --password-stdin {registry}")
    if not success:
        print("ECR auth failed")
        return False
    
    print("2. Pushing existing backend image...")
    run_cmd(f"docker tag edweavepack-backend:latest {registry}/edweavepack-backend:latest")
    success, _, _ = run_cmd(f"docker push {registry}/edweavepack-backend:latest", timeout=600)
    if not success:
        print("Backend push failed")
        return False
    
    print("3. Building and pushing frontend...")
    success, _, _ = run_cmd("docker build -t edweavepack-frontend .", cwd="frontend", timeout=600)
    if not success:
        print("Frontend build failed")
        return False
    
    run_cmd(f"docker tag edweavepack-frontend:latest {registry}/edweavepack-frontend:latest")
    success, _, _ = run_cmd(f"docker push {registry}/edweavepack-frontend:latest", timeout=600)
    if not success:
        print("Frontend push failed")
        return False
    
    print("4. Creating ECS task definition...")
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
                "image": f"{registry}/edweavepack-backend:latest",
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
                "image": f"{registry}/edweavepack-frontend:latest",
                "portMappings": [{"containerPort": 80}],
                "essential": True,
                "environment": [
                    {"name": "REACT_APP_API_URL", "value": "http://edweavepack-alb-420811343.eu-north-1.elb.amazonaws.com"},
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
    print(f"Task definition: {task_arn}")
    
    print("5. Updating ECS service...")
    try:
        ecs.update_service(
            cluster='edweavepack-cluster',
            service='edweavepack-service',
            taskDefinition=task_arn,
            forceNewDeployment=True
        )
        print("Service updated")
    except:
        try:
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
            print("Service created")
        except Exception as e:
            print(f"Service error: {e}")
            return False
    
    print("\n=== DEPLOYMENT COMPLETE ===")
    print("URL: http://edweavepack-alb-420811343.eu-north-1.elb.amazonaws.com")
    print("Features:")
    print("- FastAPI Backend with AWS AI Services")
    print("- React Frontend with Glassmorphism UI")
    print("- Bedrock (Claude 3.5 Sonnet) Integration")
    print("- Textract Document Analysis")
    print("- Comprehend Text Analysis")
    print("- Polly Text-to-Speech")
    print("- Translate Multi-language Support")
    print("- Comprehensive Authentication")
    print("- Database Integration")
    print("- Production-ready Deployment")
    return True

if __name__ == "__main__":
    success = deploy()
    sys.exit(0 if success else 1)