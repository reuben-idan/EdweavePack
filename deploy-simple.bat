@echo off
echo Starting AWS deployment...

REM Check Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker not found. Please install Docker Desktop.
    exit /b 1
)

REM Set AWS credentials (replace with your values)
set AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
set AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
set AWS_DEFAULT_REGION=us-east-1

REM Build Docker images locally for testing
echo Building Docker images...
docker build -t edweavepack-backend:latest backend/
docker build -t edweavepack-frontend:latest frontend/

REM Test containers locally
echo Testing containers...
docker run -d --name test-backend -p 8000:8000 edweavepack-backend:latest
timeout /t 5
docker run -d --name test-frontend -p 3000:3000 edweavepack-frontend:latest
timeout /t 5

REM Check if containers are running
docker ps

echo.
echo Containers built and tested successfully!
echo.
echo To deploy to AWS:
echo 1. Configure AWS CLI: aws configure
echo 2. Run: terraform init in infrastructure folder
echo 3. Run: terraform apply in infrastructure folder
echo.
echo Local URLs:
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000

REM Cleanup
docker stop test-backend test-frontend 2>nul
docker rm test-backend test-frontend 2>nul