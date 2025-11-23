# AWS Deployment Guide

## Prerequisites
- AWS CLI configured with appropriate permissions
- Docker installed
- Terraform installed

## Quick Deploy
```bash
# Set up AWS credentials
aws configure

# Deploy infrastructure and application
./deploy.sh
```

## Manual Deployment Steps

### 1. Infrastructure Setup
```bash
cd infrastructure
terraform init
terraform apply -var="db_password=YourSecurePassword123!"
```

### 2. Build and Push Images
```bash
# Get ECR login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(terraform output -raw ecr_backend_url)

# Build and push
docker build -t $(terraform output -raw ecr_backend_url):latest backend/
docker push $(terraform output -raw ecr_backend_url):latest

docker build -t $(terraform output -raw ecr_frontend_url):latest frontend/
docker push $(terraform output -raw ecr_frontend_url):latest
```

### 3. Deploy Service
```bash
aws ecs update-service --cluster edweavepack-cluster --service edweavepack-service --force-new-deployment
```

## Architecture
- **ECS Fargate**: Container orchestration
- **ALB**: Load balancing and routing
- **RDS PostgreSQL**: Database
- **ElastiCache Redis**: Caching
- **ECR**: Container registry
- **VPC**: Network isolation

## Monitoring
- CloudWatch logs: `/ecs/edweavepack`
- Health checks: `/health` endpoints
- Auto-scaling based on CPU/memory

## Security Features
- VPC with private subnets
- Security groups with minimal access
- Encrypted storage (RDS, ElastiCache)
- Non-root container users
- Image vulnerability scanning