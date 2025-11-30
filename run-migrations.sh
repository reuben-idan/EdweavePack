#!/bin/bash

# ECS RunTask for Database Migrations
# This script runs database migrations using ECS RunTask

set -e

# Configuration
CLUSTER_NAME="edweavepack-cluster"
TASK_DEFINITION="edweavepack-backend"
SUBNET_ID="subnet-0123456789abcdef0"  # Replace with actual subnet
SECURITY_GROUP="sg-0123456789abcdef0"  # Replace with actual security group
REGION="us-east-1"

echo "🚀 Running database migrations via ECS RunTask..."

# Run migration task
TASK_ARN=$(aws ecs run-task \
  --cluster "$CLUSTER_NAME" \
  --task-definition "$TASK_DEFINITION" \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_ID],securityGroups=[$SECURITY_GROUP],assignPublicIp=ENABLED}" \
  --overrides '{
    "containerOverrides": [
      {
        "name": "backend",
        "command": ["python", "migrate.py"]
      }
    ]
  }' \
  --region "$REGION" \
  --query 'tasks[0].taskArn' \
  --output text)

echo "✅ Migration task started: $TASK_ARN"

# Wait for task completion
echo "⏳ Waiting for migration task to complete..."
aws ecs wait tasks-stopped \
  --cluster "$CLUSTER_NAME" \
  --tasks "$TASK_ARN" \
  --region "$REGION"

# Get task exit code
EXIT_CODE=$(aws ecs describe-tasks \
  --cluster "$CLUSTER_NAME" \
  --tasks "$TASK_ARN" \
  --region "$REGION" \
  --query 'tasks[0].containers[0].exitCode' \
  --output text)

# Get logs
echo "📋 Migration logs:"
LOG_GROUP="/ecs/edweavepack-backend"
LOG_STREAM=$(aws logs describe-log-streams \
  --log-group-name "$LOG_GROUP" \
  --order-by LastEventTime \
  --descending \
  --max-items 1 \
  --query 'logStreams[0].logStreamName' \
  --output text)

if [ "$LOG_STREAM" != "None" ]; then
  aws logs get-log-events \
    --log-group-name "$LOG_GROUP" \
    --log-stream-name "$LOG_STREAM" \
    --query 'events[*].message' \
    --output text
fi

if [ "$EXIT_CODE" = "0" ]; then
  echo "✅ Database migrations completed successfully"
else
  echo "❌ Database migrations failed with exit code: $EXIT_CODE"
  exit 1
fi