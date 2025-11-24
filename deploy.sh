#!/bin/bash

# EdweavePack AWS Deployment Script

set -e

echo "🚀 Starting EdweavePack deployment to AWS..."

# Check if environment is provided
if [ -z "$1" ]; then
    echo "Usage: ./deploy.sh [environment]"
    echo "Example: ./deploy.sh production"
    exit 1
fi

ENVIRONMENT=$1
ENV_FILE=".env.${ENVIRONMENT}"

# Check if environment file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Environment file $ENV_FILE not found!"
    echo "Please create $ENV_FILE with your configuration."
    exit 1
fi

# Load environment variables
source $ENV_FILE

echo "📦 Building Docker images for $ENVIRONMENT..."

# Build backend image
docker build -f backend/Dockerfile.prod -t edweave-backend:$ENVIRONMENT ./backend

# Build frontend image with API URL
docker build -f frontend/Dockerfile.prod \
    --build-arg REACT_APP_API_URL=$REACT_APP_API_URL \
    -t edweave-frontend:$ENVIRONMENT ./frontend

echo "🏷️ Tagging images for ECR..."

# Tag images for ECR (replace with your ECR repository URIs)
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

docker tag edweave-backend:$ENVIRONMENT $ECR_REGISTRY/edweave-backend:$ENVIRONMENT
docker tag edweave-frontend:$ENVIRONMENT $ECR_REGISTRY/edweave-frontend:$ENVIRONMENT

echo "🔐 Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

echo "📤 Pushing images to ECR..."
docker push $ECR_REGISTRY/edweave-backend:$ENVIRONMENT
docker push $ECR_REGISTRY/edweave-frontend:$ENVIRONMENT

echo "🔄 Updating ECS services..."
aws ecs update-service \
    --cluster edweave-cluster \
    --service edweave-backend-service \
    --force-new-deployment \
    --region $AWS_REGION

aws ecs update-service \
    --cluster edweave-cluster \
    --service edweave-frontend-service \
    --force-new-deployment \
    --region $AWS_REGION

echo "✅ Deployment completed successfully!"
echo "🌐 Frontend: Check your load balancer URL"
echo "🔧 Backend: Check your API load balancer URL"
echo "📊 Monitor: Check ECS console for deployment status"