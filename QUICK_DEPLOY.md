# Quick AWS Deployment

## Step 1: Get AWS Keys (2 minutes)
1. Login: https://084828575963.signin.aws.amazon.com/console
2. Search "IAM" → Users → Security credentials
3. Create access key → CLI → Create
4. Copy Access Key ID and Secret Key

## Step 2: Configure CLI (1 minute)
```cmd
cd "C:\Program Files\Amazon\AWSCLIV2"
aws.exe configure
```
Enter your keys, region: us-east-1, format: json

## Step 3: Deploy (10 minutes)
```cmd
cd c:\Users\reube\EdweavePack
deploy-aws.bat
```

## Result
- Application URL provided at end
- Full production AWS deployment
- Auto-scaling, load balancing, database

**Total time: ~13 minutes**