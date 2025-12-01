#!/usr/bin/env python3
import boto3

AWS_REGION = 'eu-north-1'
AWS_ACCESS_KEY = 'AKIARHQBNLDN6T3PP7IK'
AWS_SECRET_KEY = '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'

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

elbv2 = session.client('elbv2')
ecs = session.client('ecs')
ec2 = session.client('ec2')

# Get all ALBs
albs = elbv2.describe_load_balancers()
print("Available ALBs:")
for alb in albs['LoadBalancers']:
    print(f"- {alb['LoadBalancerName']}: {alb['DNSName']}")

# Get VPC and subnets
vpcs = ec2.describe_vpcs()
default_vpc = next((vpc for vpc in vpcs['Vpcs'] if vpc.get('IsDefault')), vpcs['Vpcs'][0])
vpc_id = default_vpc['VpcId']

subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
subnet_ids = [subnet['SubnetId'] for subnet in subnets['Subnets']]

print(f"\nVPC: {vpc_id}")
print(f"Subnets: {subnet_ids}")

# Create ALB if none exists
if not any('edweavepack' in alb['LoadBalancerName'] for alb in albs['LoadBalancers']):
    print("\nCreating new ALB...")
    
    # Create security group
    try:
        sg = ec2.create_security_group(
            GroupName='edweavepack-alb-sg',
            Description='EdweavePack ALB Security Group',
            VpcId=vpc_id
        )
        sg_id = sg['GroupId']
        
        # Add rules
        ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ]
        )
    except:
        # Use existing security group
        sgs = ec2.describe_security_groups(Filters=[{'Name': 'group-name', 'Values': ['default']}])
        sg_id = sgs['SecurityGroups'][0]['GroupId']
    
    # Create ALB
    alb = elbv2.create_load_balancer(
        Name='edweavepack-alb',
        Subnets=subnet_ids[:2],
        SecurityGroups=[sg_id],
        Scheme='internet-facing',
        Type='application'
    )
    
    alb_arn = alb['LoadBalancers'][0]['LoadBalancerArn']
    dns_name = alb['LoadBalancers'][0]['DNSName']
    
    # Create target group
    tg = elbv2.create_target_group(
        Name='edweavepack-tg',
        Protocol='HTTP',
        Port=80,
        VpcId=vpc_id,
        TargetType='ip'
    )
    tg_arn = tg['TargetGroups'][0]['TargetGroupArn']
    
    # Create listener
    elbv2.create_listener(
        LoadBalancerArn=alb_arn,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[{
            'Type': 'forward',
            'TargetGroupArn': tg_arn
        }]
    )
    
    print(f"ALB created: {dns_name}")
    print(f"Target Group: {tg_arn}")
    
    # Update ECS service with ALB
    try:
        ecs.update_service(
            cluster='edweavepack-cluster',
            service='edweavepack-service',
            loadBalancers=[{
                'targetGroupArn': tg_arn,
                'containerName': 'frontend',
                'containerPort': 80
            }]
        )
        print("ECS service updated with ALB")
    except Exception as e:
        print(f"ECS update error: {e}")
    
    print(f"\nNew URL: http://{dns_name}")
else:
    working_alb = next(alb for alb in albs['LoadBalancers'] if 'edweavepack' in alb['LoadBalancerName'])
    print(f"\nExisting ALB: http://{working_alb['DNSName']}")