@echo off
echo Starting secure AWS deployment for EdweavePack...

REM Generate secure passwords
set DB_PASSWORD=%RANDOM%%RANDOM%%RANDOM%SecureDB!
set JWT_SECRET=%RANDOM%%RANDOM%%RANDOM%SecureJWT!

REM Set Terraform variables
set TF_VAR_db_password=%DB_PASSWORD%
set TF_VAR_jwt_secret_key=%JWT_SECRET%

echo Deploying with secure configuration...
python secure_aws_deploy.py

if %ERRORLEVEL% EQU 0 (
    echo ✅ Secure deployment completed successfully!
    echo 📋 Access your application at the ALB endpoint
) else (
    echo ❌ Deployment failed!
    exit /b 1
)

pause