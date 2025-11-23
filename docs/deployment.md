# Deployment Guide

## Prerequisites

- AWS CLI configured with appropriate permissions
- Docker and Docker Compose installed
- Terraform >= 1.0
- Node.js 18+ and Python 3.11+

## Quick Deployment

### 1. Infrastructure Setup

```bash
# Clone repository
git clone https://github.com/your-org/EdweavePack.git
cd EdweavePack

# Configure Terraform variables
cp infrastructure/terraform.tfvars.example infrastructure/terraform.tfvars
# Edit terraform.tfvars with your values

# Deploy infrastructure
make deploy-infra
```

### 2. Application Deployment

```bash
# Build and deploy
./deploy.sh all

# Or step by step
./deploy.sh infra    # Deploy infrastructure
./deploy.sh images   # Build and push images
./deploy.sh service  # Update ECS service
```

## Manual Deployment

### Infrastructure

```bash
cd infrastructure
terraform init
terraform plan
terraform apply
```

### Docker Images

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
cd backend
docker build -t edweavepack-backend .
docker tag edweavepack-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/edweavepack-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/edweavepack-backend:latest

# Build and push frontend
cd ../frontend
docker build -t edweavepack-frontend .
docker tag edweavepack-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/edweavepack-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/edweavepack-frontend:latest
```

### ECS Service Update

```bash
aws ecs update-service --cluster edweavepack-cluster --service edweavepack-service --force-new-deployment
```

## CI/CD Pipeline

The GitHub Actions workflow automatically:

1. **Test Phase**: Runs backend and frontend tests
2. **Lint Phase**: Checks code quality
3. **Build Phase**: Creates Docker images
4. **Deploy Phase**: Pushes to ECR and updates ECS

### Required Secrets

Add these secrets to your GitHub repository:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

## Monitoring

### CloudWatch Dashboards

Access monitoring at: AWS Console → CloudWatch → Dashboards → edweavepack-dashboard

### OpenSearch Logs

Access logs at: AWS Console → OpenSearch → edweavepack-logs

### Alarms

- High CPU utilization (>80%)
- High memory utilization (>80%)
- High response time (>5s)

## Environment Variables

### Backend

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `AWS_REGION`: AWS region
- `S3_BUCKET`: S3 bucket name
- `JWT_SECRET`: JWT signing secret

### Frontend

- `REACT_APP_API_URL`: Backend API URL

## Scaling

### Auto Scaling

ECS service is configured with:
- Min capacity: 1
- Max capacity: 10
- Target CPU: 70%

### Manual Scaling

```bash
aws ecs update-service --cluster edweavepack-cluster --service edweavepack-service --desired-count 3
```

## Troubleshooting

### Common Issues

1. **ECS Tasks Failing**
   - Check CloudWatch logs
   - Verify environment variables
   - Check security group rules

2. **Database Connection Issues**
   - Verify RDS security group
   - Check database credentials
   - Ensure VPC configuration

3. **Load Balancer Health Checks Failing**
   - Check target group health
   - Verify container port mapping
   - Review application logs

### Useful Commands

```bash
# Check ECS service status
aws ecs describe-services --cluster edweavepack-cluster --services edweavepack-service

# View task logs
aws logs tail /ecs/edweavepack-backend --follow

# Check ALB target health
aws elbv2 describe-target-health --target-group-arn <target-group-arn>
```

## Rollback

### Quick Rollback

```bash
# Rollback to previous task definition
aws ecs update-service --cluster edweavepack-cluster --service edweavepack-service --task-definition edweavepack-app:<previous-revision>
```

### Infrastructure Rollback

```bash
cd infrastructure
terraform plan -destroy
terraform destroy  # Only if necessary
```

## Security

- All traffic encrypted in transit (HTTPS/TLS)
- Database encryption at rest
- VPC with private subnets
- Security groups with minimal access
- IAM roles with least privilege
- Container image scanning enabled

## Cost Optimization

- Use Fargate Spot for non-production
- Enable RDS automated backups
- Configure S3 lifecycle policies
- Monitor CloudWatch costs
- Use reserved instances for predictable workloads