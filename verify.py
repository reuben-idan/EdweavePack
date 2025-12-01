#!/usr/bin/env python3
import requests
import time
import boto3

AWS_REGION = 'eu-north-1'
AWS_ACCESS_KEY = 'AKIARHQBNLDN6T3PP7IK'
AWS_SECRET_KEY = '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'

def verify_deployment():
    url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    print("=== DEPLOYMENT VERIFICATION ===")
    
    # Check ECS service
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )
    
    ecs = session.client('ecs')
    services = ecs.describe_services(
        cluster='edweavepack-cluster',
        services=['edweavepack-service']
    )
    
    service = services['services'][0]
    print(f"Service: {service['status']}")
    print(f"Tasks: {service['runningCount']}/{service['desiredCount']}")
    
    # Test URL multiple times
    print(f"\nTesting URL: {url}")
    
    for i in range(5):
        try:
            response = requests.get(url, timeout=15)
            print(f"Attempt {i+1}: Status {response.status_code}")
            
            if response.status_code == 200:
                print("SUCCESS: Application is live!")
                print(f"Response: {response.text[:200]}")
                return True
            elif response.status_code == 503:
                print("Service unavailable - containers still starting")
            else:
                print(f"Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"Attempt {i+1}: Error - {str(e)[:50]}")
        
        if i < 4:
            print("Waiting 30 seconds...")
            time.sleep(30)
    
    return False

if __name__ == "__main__":
    success = verify_deployment()
    if success:
        print("\n✅ DEPLOYMENT SUCCESSFUL!")
        print("URL: http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com")
    else:
        print("\n⏳ Deployment still in progress - check again in 5 minutes")