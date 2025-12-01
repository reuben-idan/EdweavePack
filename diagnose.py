#!/usr/bin/env python3
import boto3
import requests
import json

AWS_REGION = 'eu-north-1'
AWS_ACCESS_KEY = 'AKIARHQBNLDN6T3PP7IK'
AWS_SECRET_KEY = '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'

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def check_all():
    ecs = session.client('ecs')
    elbv2 = session.client('elbv2')
    logs = session.client('logs')
    
    print("=== COMPREHENSIVE DEPLOYMENT DIAGNOSIS ===")
    
    # 1. Check ECS Service
    print("\n1. ECS SERVICE STATUS:")
    try:
        services = ecs.describe_services(
            cluster='edweavepack-cluster',
            services=['edweavepack-service']
        )
        
        if services['services']:
            service = services['services'][0]
            print(f"   Status: {service['status']}")
            print(f"   Running: {service['runningCount']}/{service['desiredCount']}")
            print(f"   Pending: {service['pendingCount']}")
            
            # Check tasks
            tasks = ecs.list_tasks(
                cluster='edweavepack-cluster',
                serviceName='edweavepack-service'
            )
            
            if tasks['taskArns']:
                task_details = ecs.describe_tasks(
                    cluster='edweavepack-cluster',
                    tasks=tasks['taskArns']
                )
                
                for task in task_details['tasks']:
                    print(f"   Task: {task['lastStatus']}")
                    if task['lastStatus'] == 'STOPPED':
                        print(f"   Stop Reason: {task.get('stoppedReason', 'Unknown')}")
                        for container in task['containers']:
                            if 'reason' in container:
                                print(f"   Container {container['name']}: {container['reason']}")
            else:
                print("   No tasks found")
        else:
            print("   Service not found")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 2. Check ALB
    print("\n2. LOAD BALANCER STATUS:")
    try:
        albs = elbv2.describe_load_balancers()
        edweave_albs = [alb for alb in albs['LoadBalancers'] if 'edweavepack' in alb['LoadBalancerName']]
        
        if edweave_albs:
            alb = edweave_albs[0]
            print(f"   ALB: {alb['LoadBalancerName']}")
            print(f"   DNS: {alb['DNSName']}")
            print(f"   State: {alb['State']['Code']}")
            
            # Check target groups
            tgs = elbv2.describe_target_groups(LoadBalancerArn=alb['LoadBalancerArn'])
            for tg in tgs['TargetGroups']:
                print(f"   Target Group: {tg['TargetGroupName']}")
                
                # Check target health
                health = elbv2.describe_target_health(TargetGroupArn=tg['TargetGroupArn'])
                for target in health['TargetHealthDescriptions']:
                    print(f"   Target {target['Target']['Id']}: {target['TargetHealth']['State']}")
                    if target['TargetHealth']['State'] != 'healthy':
                        print(f"   Reason: {target['TargetHealth'].get('Description', 'Unknown')}")
        else:
            print("   No ALB found")
    except Exception as e:
        print(f"   Error: {e}")
    
    # 3. Test URL
    print("\n3. URL ACCESSIBILITY:")
    url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    try:
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   SUCCESS: Application accessible")
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Error: {str(e)[:100]}")
    
    # 4. Check logs
    print("\n4. RECENT LOGS:")
    try:
        log_groups = logs.describe_log_groups(logGroupNamePrefix='/ecs/edweavepack')
        if log_groups['logGroups']:
            for lg in log_groups['logGroups']:
                print(f"   Log Group: {lg['logGroupName']}")
                
                streams = logs.describe_log_streams(
                    logGroupName=lg['logGroupName'],
                    orderBy='LastEventTime',
                    descending=True,
                    limit=2
                )
                
                for stream in streams['logStreams']:
                    events = logs.get_log_events(
                        logGroupName=lg['logGroupName'],
                        logStreamName=stream['logStreamName'],
                        limit=3
                    )
                    
                    for event in events['events'][-3:]:
                        print(f"   {event['message'][:100]}")
    except Exception as e:
        print(f"   Log error: {e}")
    
    return url

if __name__ == "__main__":
    url = check_all()
    print(f"\n=== SUMMARY ===")
    print(f"URL: {url}")
    print("If issues found, running fix script...")