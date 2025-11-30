#!/usr/bin/env python3
"""
Setup CloudWatch monitoring for EdweavePack
"""

import boto3
import json
import sys
from typing import Dict, Any

class CloudWatchMonitoring:
    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.logs = boto3.client('logs', region_name=region)
        self.sns = boto3.client('sns', region_name=region)
        
    def create_metric_filters(self) -> Dict[str, str]:
        """Create CloudWatch metric filters for 5xx errors"""
        
        filters_created = {}
        
        # ALB 5xx errors filter
        try:
            self.logs.put_metric_filter(
                logGroupName='/aws/applicationloadbalancer/edweavepack-alb',
                filterName='ALB-5xx-Errors',
                filterPattern='[timestamp, request_id, client_ip, client_port, target_ip, target_port, request_processing_time, target_processing_time, response_processing_time, elb_status_code=5*, user_agent_status_code, target_status_code, received_bytes, sent_bytes, request, user_agent, ssl_cipher, ssl_protocol, target_group_arn, trace_id, domain_name, chosen_cert_arn, matched_rule_priority, request_creation_time, actions_executed, redirect_url, error_reason]',
                metricTransformations=[
                    {
                        'metricName': 'ALB5xxErrors',
                        'metricNamespace': 'EdweavePack/ALB',
                        'metricValue': '1',
                        'defaultValue': 0
                    }
                ]
            )
            filters_created['alb_5xx'] = 'ALB-5xx-Errors'
        except Exception as e:
            print(f"Warning: ALB metric filter creation failed: {e}")
        
        # Backend 5xx errors filter
        try:
            self.logs.put_metric_filter(
                logGroupName='/ecs/edweavepack-backend',
                filterName='Backend-5xx-Errors',
                filterPattern='[timestamp, level="ERROR", message]',
                metricTransformations=[
                    {
                        'metricName': 'Backend5xxErrors',
                        'metricNamespace': 'EdweavePack/Backend',
                        'metricValue': '1',
                        'defaultValue': 0
                    }
                ]
            )
            filters_created['backend_5xx'] = 'Backend-5xx-Errors'
        except Exception as e:
            print(f"Warning: Backend metric filter creation failed: {e}")
        
        return filters_created
    
    def create_sns_topic(self) -> str:
        """Create SNS topic for alarm notifications"""
        
        try:
            response = self.sns.create_topic(Name='edweavepack-alerts')
            topic_arn = response['TopicArn']
            
            # Add email subscription (replace with actual email)
            self.sns.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint='admin@edweavepack.com'
            )
            
            return topic_arn
        except Exception as e:
            print(f"Warning: SNS topic creation failed: {e}")
            return ""
    
    def create_alarms(self, sns_topic_arn: str) -> Dict[str, str]:
        """Create CloudWatch alarms"""
        
        alarms_created = {}
        
        # ALB 5xx errors alarm
        try:
            self.cloudwatch.put_metric_alarm(
                AlarmName='EdweavePack-ALB-5xx-Errors',
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=2,
                MetricName='ALB5xxErrors',
                Namespace='EdweavePack/ALB',
                Period=300,
                Statistic='Sum',
                Threshold=5.0,
                ActionsEnabled=True,
                AlarmActions=[sns_topic_arn] if sns_topic_arn else [],
                AlarmDescription='ALB 5xx errors exceeded threshold',
                Unit='Count'
            )
            alarms_created['alb_5xx'] = 'EdweavePack-ALB-5xx-Errors'
        except Exception as e:
            print(f"Warning: ALB alarm creation failed: {e}")
        
        # ECS CPU utilization alarm
        try:
            self.cloudwatch.put_metric_alarm(
                AlarmName='EdweavePack-ECS-High-CPU',
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=3,
                MetricName='CPUUtilization',
                Namespace='AWS/ECS',
                Period=300,
                Statistic='Average',
                Threshold=80.0,
                ActionsEnabled=True,
                AlarmActions=[sns_topic_arn] if sns_topic_arn else [],
                AlarmDescription='ECS CPU utilization high',
                Dimensions=[
                    {'Name': 'ServiceName', 'Value': 'edweavepack-service'},
                    {'Name': 'ClusterName', 'Value': 'edweavepack-cluster'}
                ],
                Unit='Percent'
            )
            alarms_created['ecs_cpu'] = 'EdweavePack-ECS-High-CPU'
        except Exception as e:
            print(f"Warning: ECS CPU alarm creation failed: {e}")
        
        return alarms_created
    
    def create_dashboard(self) -> str:
        """Create CloudWatch dashboard"""
        
        dashboard_body = {
            "widgets": [
                {
                    "type": "metric",
                    "x": 0, "y": 0, "width": 12, "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/ECS", "CPUUtilization", "ServiceName", "edweavepack-service", "ClusterName", "edweavepack-cluster"],
                            [".", "MemoryUtilization", ".", ".", ".", "."],
                            [".", "RunningTaskCount", ".", ".", ".", "."]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": self.region,
                        "title": "ECS Service Metrics"
                    }
                },
                {
                    "type": "metric",
                    "x": 12, "y": 0, "width": 12, "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/ApplicationELB", "HTTPCode_ELB_5XX_Count", "LoadBalancer", "app/edweavepack-alb/*"],
                            [".", "TargetResponseTime", ".", "."],
                            [".", "HealthyHostCount", "TargetGroup", "edweavepack-targets"]
                        ],
                        "period": 300,
                        "stat": "Sum",
                        "region": self.region,
                        "title": "ALB Metrics"
                    }
                },
                {
                    "type": "metric",
                    "x": 0, "y": 6, "width": 12, "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/RDS", "CPUUtilization", "DBInstanceIdentifier", "edweavepack-db"],
                            [".", "FreeStorageSpace", ".", "."],
                            [".", "DatabaseConnections", ".", "."]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": self.region,
                        "title": "RDS Metrics"
                    }
                },
                {
                    "type": "log",
                    "x": 12, "y": 6, "width": 12, "height": 6,
                    "properties": {
                        "query": "SOURCE '/ecs/edweavepack-backend'\n| fields @timestamp, @message\n| filter @message like /ERROR/\n| sort @timestamp desc\n| limit 20",
                        "region": self.region,
                        "title": "Recent Errors"
                    }
                }
            ]
        }
        
        try:
            self.cloudwatch.put_dashboard(
                DashboardName='EdweavePack-Monitoring',
                DashboardBody=json.dumps(dashboard_body)
            )
            
            dashboard_url = f"https://{self.region}.console.aws.amazon.com/cloudwatch/home?region={self.region}#dashboards:name=EdweavePack-Monitoring"
            return dashboard_url
        except Exception as e:
            print(f"Warning: Dashboard creation failed: {e}")
            return ""
    
    def setup_monitoring(self) -> Dict[str, Any]:
        """Setup complete monitoring stack"""
        
        print("🔧 Setting up CloudWatch monitoring...")
        
        # Create metric filters
        print("📊 Creating metric filters...")
        filters = self.create_metric_filters()
        
        # Create SNS topic
        print("📧 Creating SNS topic...")
        sns_topic = self.create_sns_topic()
        
        # Create alarms
        print("🚨 Creating CloudWatch alarms...")
        alarms = self.create_alarms(sns_topic)
        
        # Create dashboard
        print("📈 Creating CloudWatch dashboard...")
        dashboard_url = self.create_dashboard()
        
        return {
            "success": True,
            "metric_filters": filters,
            "sns_topic_arn": sns_topic,
            "alarms": alarms,
            "dashboard_url": dashboard_url,
            "region": self.region
        }

def main():
    """Main monitoring setup function"""
    
    region = sys.argv[1] if len(sys.argv) > 1 else "us-east-1"
    
    print("🚀 EdweavePack CloudWatch Monitoring Setup")
    print("=" * 45)
    
    monitoring = CloudWatchMonitoring(region)
    results = monitoring.setup_monitoring()
    
    print(f"\n📋 Setup Results:")
    print(json.dumps(results, indent=2))
    
    if results["dashboard_url"]:
        print(f"\n📈 Dashboard URL: {results['dashboard_url']}")
    
    return results

if __name__ == "__main__":
    main()