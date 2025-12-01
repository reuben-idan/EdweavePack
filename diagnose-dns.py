#!/usr/bin/env python3

import boto3
import json
import subprocess
import sys

def check_alb_status():
    """Check ALB status and get correct DNS name"""
    try:
        elbv2 = boto3.client('elbv2', region_name='eu-north-1')
        
        # List all load balancers
        response = elbv2.describe_load_balancers()
        
        print("=== Load Balancers ===")
        for lb in response['LoadBalancers']:
            print(f"Name: {lb['LoadBalancerName']}")
            print(f"DNS: {lb['DNSName']}")
            print(f"State: {lb['State']['Code']}")
            print(f"Scheme: {lb['Scheme']}")
            print(f"Type: {lb['Type']}")
            print("---")
            
            # Check target groups for this ALB
            tg_response = elbv2.describe_target_groups(LoadBalancerArn=lb['LoadBalancerArn'])
            for tg in tg_response['TargetGroups']:
                print(f"Target Group: {tg['TargetGroupName']}")
                print(f"Health Check Path: {tg.get('HealthCheckPath', 'N/A')}")
                
                # Check target health
                health_response = elbv2.describe_target_health(TargetGroupArn=tg['TargetGroupArn'])
                for target in health_response['TargetHealthDescriptions']:
                    print(f"Target: {target['Target']['Id']} - {target['TargetHealth']['State']}")
            print("=" * 50)
        
        return response['LoadBalancers']
        
    except Exception as e:
        print(f"Error checking ALB: {e}")
        return []

def check_ecs_services():
    """Check ECS service status"""
    try:
        ecs = boto3.client('ecs', region_name='eu-north-1')
        
        # List clusters
        clusters = ecs.list_clusters()['clusterArns']
        
        for cluster_arn in clusters:
            cluster_name = cluster_arn.split('/')[-1]
            print(f"\n=== Cluster: {cluster_name} ===")
            
            # List services
            services = ecs.list_services(cluster=cluster_arn)['serviceArns']
            
            for service_arn in services:
                service_name = service_arn.split('/')[-1]
                
                # Get service details
                service_details = ecs.describe_services(
                    cluster=cluster_arn,
                    services=[service_arn]
                )['services'][0]
                
                print(f"Service: {service_name}")
                print(f"Status: {service_details['status']}")
                print(f"Running: {service_details['runningCount']}")
                print(f"Desired: {service_details['desiredCount']}")
                print(f"Task Definition: {service_details['taskDefinition']}")
                
                # Get task details
                tasks = ecs.list_tasks(cluster=cluster_arn, serviceName=service_name)['taskArns']
                if tasks:
                    task_details = ecs.describe_tasks(cluster=cluster_arn, tasks=tasks)['tasks']
                    for task in task_details:
                        print(f"Task: {task['taskArn'].split('/')[-1]} - {task['lastStatus']}")
                        if 'containers' in task:
                            for container in task['containers']:
                                print(f"  Container: {container['name']} - {container['lastStatus']}")
                print("---")
                
    except Exception as e:
        print(f"Error checking ECS: {e}")

def test_dns_resolution(dns_name):
    """Test DNS resolution"""
    try:
        result = subprocess.run(['nslookup', dns_name], capture_output=True, text=True)
        print(f"\n=== DNS Resolution for {dns_name} ===")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
    except Exception as e:
        print(f"Error testing DNS: {e}")

def main():
    print("EdweavePack DNS Diagnostic Tool")
    print("=" * 50)
    
    # Check ALB status
    load_balancers = check_alb_status()
    
    # Check ECS services
    check_ecs_services()
    
    # Test DNS resolution for each ALB
    for lb in load_balancers:
        test_dns_resolution(lb['DNSName'])
    
    # Check specific DNS name from error
    error_dns = "edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com"
    print(f"\n=== Testing Error DNS: {error_dns} ===")
    test_dns_resolution(error_dns)

if __name__ == "__main__":
    main()