# Post-Deploy Smoke Tests & CloudWatch Monitoring

This guide covers comprehensive post-deployment validation with smoke tests and CloudWatch monitoring setup for EdweavePack.

## 📁 Created Files

### Smoke Tests & Validation
- `smoke-tests.py` - Comprehensive smoke tests with auth flow
- `setup-monitoring.py` - CloudWatch monitoring setup
- `post-deploy-validation.py` - Complete validation orchestrator
- `test-monitoring.py` - Test validation without AWS credentials

### Updated Workflows
- `.github/workflows/deploy.yml` - Updated with post-deployment validation

## 🧪 Smoke Tests Implementation

### Test Coverage
1. **Frontend Health Check**
   - Tests ALB endpoint `/` returns HTTP 200
   - Validates frontend application is accessible

2. **Backend Health Check**
   - Tests backend `/health` endpoint returns HTTP 200
   - Validates API service is running

3. **Complete Auth Flow Test**
   - Registers test teacher account
   - Confirms Cognito sign-up process
   - Obtains JWT token from login
   - Makes authenticated API call to `/api/curriculum/`
   - Validates end-to-end authentication workflow

### Usage
```bash
# Run smoke tests
export ALB_ENDPOINT="http://your-alb-dns.elb.amazonaws.com"
python smoke-tests.py

# Or pass as argument
python smoke-tests.py "http://your-alb-dns.elb.amazonaws.com"
```

## 📊 CloudWatch Monitoring Setup

### Metric Filters
1. **ALB 5xx Errors**
   - Log Group: `/aws/applicationloadbalancer/edweavepack-alb`
   - Metric: `ALB5xxErrors` in `EdweavePack/ALB` namespace
   - Filters HTTP 5xx status codes from ALB logs

2. **Backend 5xx Errors**
   - Log Group: `/ecs/edweavepack-backend`
   - Metric: `Backend5xxErrors` in `EdweavePack/Backend` namespace
   - Filters ERROR level messages from application logs

### CloudWatch Alarms
1. **ALB 5xx Errors Alarm**
   - Threshold: > 5 errors in 10 minutes (2 evaluation periods)
   - Action: SNS notification to `edweavepack-alerts` topic

2. **ECS High CPU Alarm**
   - Threshold: > 80% CPU utilization for 15 minutes (3 evaluation periods)
   - Action: SNS notification for scaling alerts

### CloudWatch Dashboard
**Dashboard Name**: `EdweavePack-Monitoring`

**Widgets**:
- **ECS Service Metrics**: CPU, Memory, Running Tasks
- **ALB Metrics**: 5xx errors, response time, healthy hosts
- **RDS Metrics**: CPU, storage, connections
- **Recent Errors**: Log insights query for ERROR messages

### Usage
```bash
# Setup monitoring
python setup-monitoring.py us-east-1

# Setup with specific region
python setup-monitoring.py eu-west-1
```

## 🔄 Complete Validation Process

### Orchestrated Validation
```bash
# Run complete post-deployment validation
export ALB_ENDPOINT="http://your-alb-dns.elb.amazonaws.com"
export AWS_REGION="us-east-1"
python post-deploy-validation.py

# Or with arguments
python post-deploy-validation.py "http://your-alb-dns.elb.amazonaws.com"
```

### GitHub Actions Integration
The deployment workflow now includes comprehensive validation:

```yaml
- name: Run comprehensive post-deployment validation
  env:
    ALB_ENDPOINT: ${{ steps.get-alb.outputs.alb_endpoint }}
    AWS_REGION: ${{ env.AWS_REGION }}
  run: |
    pip install requests boto3
    python post-deploy-validation.py
```

## 📊 Expected Results

### Smoke Test Results
```json
{
  "overall_success": true,
  "total_tests": 3,
  "passed_tests": 3,
  "failed_tests": 0,
  "results": [
    {
      "test": "Frontend Health Check",
      "status": "PASS",
      "success": true
    },
    {
      "test": "Backend Health Check", 
      "status": "PASS",
      "success": true
    },
    {
      "test": "Auth Flow Test",
      "status": "PASS", 
      "success": true
    }
  ],
  "endpoint": "http://alb-dns.elb.amazonaws.com"
}
```

### Monitoring Setup Results
```json
{
  "success": true,
  "metric_filters": {
    "alb_5xx": "ALB-5xx-Errors",
    "backend_5xx": "Backend-5xx-Errors"
  },
  "sns_topic_arn": "arn:aws:sns:us-east-1:123456789012:edweavepack-alerts",
  "alarms": {
    "alb_5xx": "EdweavePack-ALB-5xx-Errors",
    "ecs_cpu": "EdweavePack-ECS-High-CPU"
  },
  "dashboard_url": "https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=EdweavePack-Monitoring",
  "region": "us-east-1"
}
```

## 🔗 Dashboard & Monitoring URLs

### CloudWatch Dashboard
```
https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=EdweavePack-Monitoring
```

### CloudWatch Alarms
```
https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#alarmsV2:
```

### SNS Topic ARN
```
arn:aws:sns:us-east-1:ACCOUNT_ID:edweavepack-alerts
```

## 🚨 Monitoring Alerts

### Email Notifications
SNS topic `edweavepack-alerts` sends notifications for:
- ALB 5xx errors exceeding threshold
- ECS CPU utilization above 80%
- Custom application errors

### Alert Configuration
```bash
# Subscribe email to SNS topic
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:ACCOUNT_ID:edweavepack-alerts \
  --protocol email \
  --notification-endpoint admin@edweavepack.com
```

## 🔧 Troubleshooting

### Common Issues

1. **Smoke Tests Failing**
   - Check ALB endpoint accessibility
   - Verify security group rules
   - Ensure ECS tasks are running
   - Check application logs in CloudWatch

2. **Auth Flow Test Failing**
   - Verify Cognito User Pool configuration
   - Check JWT token validation
   - Ensure backend API endpoints are accessible
   - Validate database connectivity

3. **Monitoring Setup Issues**
   - Check IAM permissions for CloudWatch
   - Verify log group names exist
   - Ensure SNS topic permissions
   - Check AWS region configuration

### Debug Commands
```bash
# Check ECS service status
aws ecs describe-services \
  --cluster edweavepack-cluster \
  --services edweavepack-service

# Check ALB target health
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:region:account:targetgroup/edweavepack-targets/*

# Test endpoints manually
curl -v http://your-alb-dns.elb.amazonaws.com/health
curl -v http://your-alb-dns.elb.amazonaws.com/

# Check CloudWatch logs
aws logs describe-log-groups --log-group-name-prefix "/ecs/edweavepack"
```

## 📈 Performance Metrics

### Key Metrics to Monitor
- **Response Time**: ALB target response time < 2 seconds
- **Error Rate**: 5xx errors < 1% of total requests
- **CPU Utilization**: ECS tasks < 70% average
- **Memory Utilization**: ECS tasks < 80% average
- **Database Connections**: RDS connections < 80% of max

### Scaling Triggers
- CPU > 80% for 15 minutes → Scale out ECS tasks
- 5xx errors > 5 in 10 minutes → Investigation alert
- Response time > 5 seconds → Performance alert

## ✅ Validation Checklist

- [x] Frontend health check implemented
- [x] Backend health check implemented  
- [x] Complete auth flow test implemented
- [x] CloudWatch metric filters created
- [x] CloudWatch alarms configured
- [x] SNS notifications setup
- [x] CloudWatch dashboard created
- [x] GitHub Actions integration updated
- [x] Comprehensive validation orchestrator
- [x] Error handling and rollback integration

## 🎯 Success Criteria

### Pass/Fail Conditions
- **PASS**: All smoke tests return HTTP 200, auth flow completes successfully
- **FAIL**: Any smoke test fails, monitoring setup errors, validation timeout

### Expected Logs
```
EdweavePack Post-Deployment Validation
==================================================

Step 1: Smoke Tests (Endpoint: http://alb-dns.elb.amazonaws.com)
✅ Smoke tests passed

Step 2: CloudWatch Monitoring Setup (Region: us-east-1)  
✅ Monitoring setup completed
📈 Dashboard: https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=EdweavePack-Monitoring

Validation Summary:
==============================
Smoke Tests: ✅ PASS
Monitoring: ✅ PASS
Overall: ✅ SUCCESS
```

The post-deployment validation system provides comprehensive testing and monitoring setup with automatic rollback on failure, ensuring reliable deployments with proper observability.