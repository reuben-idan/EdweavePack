#!/bin/bash

# ECS RunTask for Seeding Test Data
# This script seeds the database with test data using ECS RunTask

set -e

# Configuration
CLUSTER_NAME="edweavepack-cluster"
TASK_DEFINITION="edweavepack-backend"
SUBNET_ID="subnet-0123456789abcdef0"  # Replace with actual subnet
SECURITY_GROUP="sg-0123456789abcdef0"  # Replace with actual security group
REGION="us-east-1"

echo "🌱 Seeding database with test data via ECS RunTask..."

# Run seed data task
TASK_ARN=$(aws ecs run-task \
  --cluster "$CLUSTER_NAME" \
  --task-definition "$TASK_DEFINITION" \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_ID],securityGroups=[$SECURITY_GROUP],assignPublicIp=ENABLED}" \
  --overrides '{
    "containerOverrides": [
      {
        "name": "backend",
        "command": ["python", "seed_data.py"]
      }
    ]
  }' \
  --region "$REGION" \
  --query 'tasks[0].taskArn' \
  --output text)

echo "✅ Seed data task started: $TASK_ARN"

# Wait for task completion
echo "⏳ Waiting for seed data task to complete..."
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
echo "📋 Seed data logs:"
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
  echo "✅ Database seeding completed successfully"
else
  echo "❌ Database seeding failed with exit code: $EXIT_CODE"
  exit 1
fi