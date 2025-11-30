# GitHub Actions CI/CD Setup Guide

This guide covers setting up GitHub Actions workflows for EdweavePack with automated testing and AWS deployment.

## 📁 Workflow Files Created

### 1. Build and Test Workflow
**File**: `.github/workflows/build-and-test.yml`
**Trigger**: Pull requests to `main` and `develop` branches
**Purpose**: Run tests and linting on code changes

### 2. Deployment Workflow  
**File**: `.github/workflows/deploy.yml`
**Trigger**: Push to `main` branch
**Purpose**: Deploy to AWS ECS with smoke tests and rollback

## 🔐 Required GitHub Secrets

Add these secrets to your GitHub repository settings:

### AWS Credentials
```
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

### ECR Repository URLs
```
ECR_BACKEND_REPO=123456789012.dkr.ecr.us-east-1.amazonaws.com/edweavepack-backend
ECR_FRONTEND_REPO=123456789012.dkr.ecr.us-east-1.amazonaws.com/edweavepack-frontend
```

## 🔧 Setup Instructions

### 1. Create ECR Repositories
```bash
# Create backend repository
aws ecr create-repository \
  --repository-name edweavepack-backend \
  --region us-east-1

# Create frontend repository  
aws ecr create-repository \
  --repository-name edweavepack-frontend \
  --region us-east-1
```

### 2. Create IAM User for GitHub Actions
```bash
# Create IAM user
aws iam create-user --user-name github-actions-edweavepack

# Attach policies
aws iam attach-user-policy \
  --user-name github-actions-edweavepack \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser

aws iam attach-user-policy \
  --user-name github-actions-edweavepack \
  --policy-arn arn:aws:iam::aws:policy/AmazonECS_FullAccess

aws iam attach-user-policy \
  --user-name github-actions-edweavepack \
  --policy-arn arn:aws:iam::aws:policy/ElasticLoadBalancingReadOnly

# Create access keys
aws iam create-access-key --user-name github-actions-edweavepack
```

### 3. Add Secrets to GitHub
1. Go to your repository on GitHub
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each required secret:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `AWS_ACCESS_KEY_ID` | IAM user access key | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key | `wJalrXUt...` |
| `AWS_REGION` | AWS region | `us-east-1` |
| `ECR_BACKEND_REPO` | Backend ECR repository | `123456789012.dkr.ecr.us-east-1.amazonaws.com/edweavepack-backend` |
| `ECR_FRONTEND_REPO` | Frontend ECR repository | `123456789012.dkr.ecr.us-east-1.amazonaws.com/edweavepack-frontend` |

## 🔄 Workflow Details

### Build and Test Workflow (`build-and-test.yml`)

**Triggers**:
- Pull requests to `main` or `develop`
- Push to `develop` branch

**Jobs**:
1. **Backend Tests**
   - Sets up Python 3.11
   - Starts PostgreSQL and Redis services
   - Installs dependencies with pip caching
   - Runs pytest with coverage
   - Uploads coverage to Codecov

2. **Frontend Tests**
   - Sets up Node.js 18
   - Installs dependencies with npm caching
   - Runs Jest tests with coverage
   - Uploads coverage to Codecov

3. **Lint and Format**
   - Checks Python code with Black, isort, flake8
   - Checks frontend code with ESLint

### Deployment Workflow (`deploy.yml`)

**Trigger**: Push to `main` branch

**Steps**:
1. **Build Images**
   - Builds Docker images for backend and frontend
   - Tags with `GITHUB_SHA`
   - Pushes to ECR repositories

2. **Update Task Definition**
   - Downloads current ECS task definition
   - Updates with new image URIs
   - Registers new task definition revision

3. **Deploy to ECS**
   - Updates ECS service with new task definition
   - Waits for service stability

4. **Smoke Tests**
   - Tests backend health endpoint: `GET /health`
   - Tests frontend health endpoint: `GET /`
   - Validates HTTP 200 responses

5. **Rollback on Failure**
   - Automatically rolls back to previous task definition
   - Waits for rollback completion
   - Notifies of rollback status

## 🧪 Testing the Workflows

### Test Build Workflow
1. Create a feature branch
2. Make a small change
3. Open a pull request to `main`
4. Verify all checks pass

### Test Deployment Workflow
1. Merge PR to `main` branch
2. Monitor workflow execution
3. Verify deployment completes
4. Check smoke test results

## 📊 Monitoring and Notifications

### Workflow Status
- View workflow runs in GitHub Actions tab
- Monitor deployment progress in real-time
- Check logs for debugging failures

### AWS Resources
- Monitor ECS service in AWS Console
- Check CloudWatch logs for application logs
- Verify ALB health checks

## 🚨 Troubleshooting

### Common Issues

1. **ECR Authentication Failed**
   - Verify AWS credentials are correct
   - Check IAM permissions for ECR access
   - Ensure ECR repositories exist

2. **ECS Deployment Timeout**
   - Check ECS service configuration
   - Verify task definition is valid
   - Monitor CloudWatch logs for errors

3. **Smoke Tests Failing**
   - Verify ALB configuration
   - Check security group rules
   - Ensure health endpoints are accessible

4. **Rollback Issues**
   - Verify previous task definition exists
   - Check ECS service permissions
   - Monitor rollback progress in AWS Console

### Debug Commands
```bash
# Check ECR repositories
aws ecr describe-repositories --region us-east-1

# Check ECS service status
aws ecs describe-services \
  --cluster edweavepack-cluster \
  --services edweavepack-service

# Check task definition revisions
aws ecs list-task-definitions \
  --family-prefix edweavepack-task-def \
  --status ACTIVE

# Test health endpoints manually
curl http://your-alb-dns/health
curl http://your-alb-dns/
```

## 🔒 Security Best Practices

### IAM Permissions
- Use least privilege principle
- Create dedicated IAM user for GitHub Actions
- Regularly rotate access keys
- Monitor CloudTrail for API usage

### Secrets Management
- Never commit secrets to repository
- Use GitHub encrypted secrets
- Consider AWS Secrets Manager for production
- Audit secret access regularly

### Container Security
- Scan Docker images for vulnerabilities
- Use minimal base images
- Keep dependencies updated
- Implement security policies

## 📈 Performance Optimization

### Build Speed
- Use dependency caching
- Optimize Docker layer caching
- Parallelize independent jobs
- Use appropriate runner sizes

### Deployment Speed
- Optimize Docker image sizes
- Use multi-stage builds
- Implement health check timeouts
- Configure appropriate service scaling

## ✅ Validation Checklist

- [x] Build and test workflow created
- [x] Deployment workflow created
- [x] Required secrets documented
- [x] ECR integration configured
- [x] ECS deployment automated
- [x] Smoke tests implemented
- [x] Rollback mechanism included
- [x] Error handling implemented

The GitHub Actions workflows are now ready for automated CI/CD with comprehensive testing, deployment, and rollback capabilities.