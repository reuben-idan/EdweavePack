@echo off
echo Starting AWS deployment...

REM Set AWS CLI path
set AWS_CLI="C:\Program Files\Amazon\AWSCLIV2\aws.exe"

REM Check AWS credentials
echo Checking AWS credentials...
%AWS_CLI% sts get-caller-identity
if errorlevel 1 (
    echo ERROR: AWS credentials not configured or invalid
    echo Please run: aws configure
    echo Or set credentials in %USERPROFILE%\.aws\credentials
    pause
    exit /b 1
)

REM Create S3 bucket for Terraform state
echo Creating S3 bucket for Terraform state...
%AWS_CLI% s3 mb s3://edweavepack-terraform-state-084828575963 --region us-east-1 2>nul

REM Initialize and apply Terraform
echo Deploying infrastructure...
cd infrastructure
terraform init
if errorlevel 1 (
    echo ERROR: Terraform init failed
    pause
    exit /b 1
)

terraform plan -var="db_password=EdweavePack2024!"
if errorlevel 1 (
    echo ERROR: Terraform plan failed
    pause
    exit /b 1
)

terraform apply -auto-approve -var="db_password=EdweavePack2024!"
if errorlevel 1 (
    echo ERROR: Terraform apply failed
    pause
    exit /b 1
)

REM Get outputs
for /f "tokens=*" %%i in ('terraform output -raw ecr_backend_url') do set BACKEND_ECR=%%i
for /f "tokens=*" %%i in ('terraform output -raw ecr_frontend_url') do set FRONTEND_ECR=%%i
for /f "tokens=*" %%i in ('terraform output -raw load_balancer_dns') do set ALB_DNS=%%i

cd ..

REM Login to ECR
echo Logging into ECR...
for /f "tokens=*" %%i in ('%AWS_CLI% ecr get-login-password --region us-east-1') do docker login --username AWS --password-stdin %BACKEND_ECR% <<<"%%i"

REM Tag and push images
echo Pushing images to ECR...
docker tag edweavepack-backend:latest %BACKEND_ECR%:latest
docker push %BACKEND_ECR%:latest

docker tag edweavepack-frontend:latest %FRONTEND_ECR%:latest
docker push %FRONTEND_ECR%:latest

REM Update ECS service
echo Updating ECS service...
%AWS_CLI% ecs update-service --cluster edweavepack-cluster --service edweavepack-service --force-new-deployment --region us-east-1

echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo Application URL: http://%ALB_DNS%
echo.
echo Services:
echo - Frontend: http://%ALB_DNS%
echo - Backend API: http://%ALB_DNS%/api
echo - API Docs: http://%ALB_DNS%/docs
echo.
pause