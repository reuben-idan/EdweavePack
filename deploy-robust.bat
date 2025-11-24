@echo off
echo ========================================
echo EdweavePack Robust AWS Deployment Script
echo ========================================

:: Check if AWS CLI is installed
aws --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: AWS CLI is not installed or not in PATH
    echo Please install AWS CLI and configure credentials
    pause
    exit /b 1
)

:: Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running
    echo Please start Docker Desktop
    pause
    exit /b 1
)

:: Set variables
set AWS_REGION=eu-north-1
set AWS_ACCOUNT_ID=084828575963
set PROJECT_NAME=edweavepack

echo.
echo Step 1: Building and pushing Docker images...
echo.

:: Build backend image
echo Building backend image...
cd backend
docker build -t %PROJECT_NAME%-backend:latest -f Dockerfile.prod .
if %errorlevel% neq 0 (
    echo ERROR: Failed to build backend image
    pause
    exit /b 1
)

:: Tag and push backend
docker tag %PROJECT_NAME%-backend:latest %AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com/%PROJECT_NAME%-backend:latest
aws ecr get-login-password --region %AWS_REGION% | docker login --username AWS --password-stdin %AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com
docker push %AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com/%PROJECT_NAME%-backend:latest

cd ..

:: Build frontend image
echo Building frontend image...
cd frontend
docker build -t %PROJECT_NAME%-frontend:latest -f Dockerfile.prod .
if %errorlevel% neq 0 (
    echo ERROR: Failed to build frontend image
    pause
    exit /b 1
)

:: Tag and push frontend
docker tag %PROJECT_NAME%-frontend:latest %AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com/%PROJECT_NAME%-frontend:latest
docker push %AWS_ACCOUNT_ID%.dkr.ecr.%AWS_REGION%.amazonaws.com/%PROJECT_NAME%-frontend:latest

cd ..

echo.
echo Step 2: Deploying infrastructure with Terraform...
echo.

cd infrastructure

:: Initialize Terraform
terraform init
if %errorlevel% neq 0 (
    echo ERROR: Terraform initialization failed
    pause
    exit /b 1
)

:: Plan deployment
terraform plan
if %errorlevel% neq 0 (
    echo ERROR: Terraform planning failed
    pause
    exit /b 1
)

:: Apply deployment
terraform apply -auto-approve
if %errorlevel% neq 0 (
    echo ERROR: Terraform deployment failed
    pause
    exit /b 1
)

cd ..

echo.
echo Step 3: Updating ECS service...
echo.

:: Force new deployment
aws ecs update-service --cluster %PROJECT_NAME%-cluster --service %PROJECT_NAME%-service --force-new-deployment --region %AWS_REGION%

echo.
echo Step 4: Waiting for deployment to complete...
echo.

:: Wait for service to be stable
aws ecs wait services-stable --cluster %PROJECT_NAME%-cluster --services %PROJECT_NAME%-service --region %AWS_REGION%

echo.
echo ========================================
echo Deployment completed successfully!
echo ========================================
echo.
echo Your application is now available at:
echo https://edweavepack.com
echo.
echo To check deployment status:
echo aws ecs describe-services --cluster %PROJECT_NAME%-cluster --services %PROJECT_NAME%-service --region %AWS_REGION%
echo.
pause