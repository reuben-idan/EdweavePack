# Get AWS Access Keys

## Steps to Get AWS Credentials

1. **Login to AWS Console**
   - URL: https://084828575963.signin.aws.amazon.com/console
   - Username: nobleadonis2@gmail.com
   - Password: NtoI8]Z'

2. **Navigate to IAM**
   - Search for "IAM" in AWS Console
   - Click on "IAM" service

3. **Create Access Key**
   - Click "Users" in left sidebar
   - Click on your username
   - Click "Security credentials" tab
   - Click "Create access key"
   - Choose "Command Line Interface (CLI)"
   - Click "Next" → "Create access key"

4. **Copy Credentials**
   - Copy "Access key ID"
   - Copy "Secret access key"

5. **Configure AWS CLI**
   ```cmd
   cd "C:\Program Files\Amazon\AWSCLIV2"
   aws.exe configure
   ```
   
   Enter:
   - AWS Access Key ID: [paste access key]
   - AWS Secret Access Key: [paste secret key]
   - Default region: us-east-1
   - Default output format: json

6. **Deploy Application**
   ```cmd
   cd c:\Users\reube\EdweavePack
   deploy-aws.bat
   ```

## Alternative: Manual Configuration

Edit file: `%USERPROFILE%\.aws\credentials`
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY_HERE
aws_secret_access_key = YOUR_SECRET_KEY_HERE
```

Then run: `deploy-aws.bat`

## What Happens Next

1. ✅ Creates S3 bucket for Terraform state
2. ✅ Deploys AWS infrastructure (VPC, ECS, RDS, etc.)
3. ✅ Pushes Docker images to ECR
4. ✅ Starts ECS service
5. ✅ Provides application URL

**Estimated deployment time: 10-15 minutes**