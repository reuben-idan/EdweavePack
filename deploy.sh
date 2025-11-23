#!/bin/bash
set -e

echo "🚀 Starting AWS deployment..."

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS CLI not configured. Please run 'aws configure'"
    exit 1
fi

# Set variables
REGION="us-east-1"
PROJECT="edweavepack"

# Create S3 bucket for Terraform state if it doesn't exist
aws s3api head-bucket --bucket "${PROJECT}-terraform-state" --region $REGION 2>/dev/null || \
aws s3 mb s3://${PROJECT}-terraform-state --region $REGION

# Deploy infrastructure
echo "📦 Deploying infrastructure..."
cd infrastructure
terraform init
terraform plan -var="db_password=$(openssl rand -base64 32)"
terraform apply -auto-approve -var="db_password=$(openssl rand -base64 32)"

# Get ECR URLs
BACKEND_ECR=$(terraform output -raw ecr_backend_url)
FRONTEND_ECR=$(terraform output -raw ecr_frontend_url)
ALB_DNS=$(terraform output -raw load_balancer_dns)

cd ..

# Login to ECR
echo "🔐 Logging into ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $BACKEND_ECR

# Build and push images
echo "🏗️ Building and pushing images..."
docker build -t $BACKEND_ECR:latest backend/
docker push $BACKEND_ECR:latest

docker build -t $FRONTEND_ECR:latest frontend/
docker push $FRONTEND_ECR:latest

# Update ECS service
echo "🔄 Updating ECS service..."
aws ecs update-service --cluster ${PROJECT}-cluster --service ${PROJECT}-service --force-new-deployment --region $REGION

echo "✅ Deployment complete!"
echo "🌐 Application URL: http://$ALB_DNS"