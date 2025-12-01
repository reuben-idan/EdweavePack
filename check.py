#!/usr/bin/env python3
import boto3
import requests

AWS_REGION = 'eu-north-1'
AWS_ACCESS_KEY = 'AKIARHQBNLDN6T3PP7IK'
AWS_SECRET_KEY = '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'

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

ecs = session.client('ecs')

# Check service
services = ecs.describe_services(
    cluster='edweavepack-cluster',
    services=['edweavepack-service']
)

service = services['services'][0]
print(f"Service: {service['status']}")
print(f"Tasks: {service['runningCount']}/{service['desiredCount']}")

# Test URL
url = "http://edweavepack-alb-420811343.eu-north-1.elb.amazonaws.com"
try:
    response = requests.get(url, timeout=10)
    print(f"URL Status: {response.status_code}")
    if response.status_code == 200:
        print("SUCCESS: Application accessible")
    else:
        print("Application starting...")
except:
    print("Application not ready yet")

print(f"\nURL: {url}")