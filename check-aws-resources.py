#!/usr/bin/env python3
import boto3
import sys

# AWS Configuration
AWS_REGION = 'eu-north-1'
AWS_ACCESS_KEY = 'AKIARHQBNLDN6T3PP7IK'
AWS_SECRET_KEY = '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'

def check_aws_resources():
    try:
        # Initialize AWS clients
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION
        )
        
        ecr = session.client('ecr')
        ecs = session.client('ecs')
        elbv2 = session.client('elbv2')
        
        print(f"Checking AWS resources in {AWS_REGION}...")
        print("=" * 50)
        
        # Check ECR repositories
        print("\nECR Repositories:")
        try:
            repos = ecr.describe_repositories()['repositories']
            backend_exists = any(r['repositoryName'] == 'edweavepack-backend' for r in repos)
            frontend_exists = any(r['repositoryName'] == 'edweavepack-frontend' for r in repos)
            
            print(f"  edweavepack-backend: {'EXISTS' if backend_exists else 'MISSING'}")
            print(f"  edweavepack-frontend: {'EXISTS' if frontend_exists else 'MISSING'}")
        except Exception as e:
            print(f"  Error checking ECR: {e}")
        
        # Check ECS cluster
        print("\nECS Resources:")
        try:
            clusters = ecs.describe_clusters(clusters=['edweavepack-cluster'])['clusters']
            cluster_exists = len(clusters) > 0 and clusters[0]['status'] == 'ACTIVE'
            print(f"  edweavepack-cluster: {'EXISTS' if cluster_exists else 'MISSING'}")
            
            if cluster_exists:
                services = ecs.describe_services(
                    cluster='edweavepack-cluster',
                    services=['edweavepack-service']
                )['services']
                service_exists = len(services) > 0
                print(f"  edweavepack-service: {'EXISTS' if service_exists else 'MISSING'}")
        except Exception as e:
            print(f"  Error checking ECS: {e}")
        
        # Check ALB
        print("\nLoad Balancer:")
        try:
            albs = elbv2.describe_load_balancers()['LoadBalancers']
            alb_exists = any(alb['LoadBalancerName'] == 'edweavepack-alb' for alb in albs)
            print(f"  edweavepack-alb: {'EXISTS' if alb_exists else 'MISSING'}")
        except Exception as e:
            print(f"  Error checking ALB: {e}")
        
        print("\n" + "=" * 50)
        print("Resource check completed")
        
    except Exception as e:
        print(f"Failed to connect to AWS: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_aws_resources()