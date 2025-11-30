#!/usr/bin/env python3
"""
Complete post-deployment validation with smoke tests and monitoring setup
"""

import subprocess
import json
import sys
import os
import time
from typing import Dict, Any

def run_smoke_tests(alb_endpoint: str) -> Dict[str, Any]:
    """Run smoke tests and return results"""
    
    print("🧪 Running smoke tests...")
    
    try:
        # Set environment variable for smoke tests
        env = os.environ.copy()
        env['ALB_ENDPOINT'] = alb_endpoint
        
        # Run smoke tests
        result = subprocess.run(
            [sys.executable, 'smoke-tests.py'],
            env=env,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # Parse JSON output from smoke tests
        output_lines = result.stdout.strip().split('\n')
        json_start = -1
        
        for i, line in enumerate(output_lines):
            if line.strip().startswith('{'):
                json_start = i
                break
        
        if json_start >= 0:
            json_output = '\n'.join(output_lines[json_start:])
            smoke_results = json.loads(json_output)
        else:
            smoke_results = {
                "overall_success": result.returncode == 0,
                "error": "Could not parse smoke test results",
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        
        return smoke_results
        
    except subprocess.TimeoutExpired:
        return {
            "overall_success": False,
            "error": "Smoke tests timed out after 5 minutes"
        }
    except Exception as e:
        return {
            "overall_success": False,
            "error": f"Smoke test execution failed: {str(e)}"
        }

def setup_monitoring(region: str = "us-east-1") -> Dict[str, Any]:
    """Setup CloudWatch monitoring and return results"""
    
    print("📊 Setting up CloudWatch monitoring...")
    
    try:
        # Run monitoring setup
        result = subprocess.run(
            [sys.executable, 'setup-monitoring.py', region],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # Parse JSON output from monitoring setup
        output_lines = result.stdout.strip().split('\n')
        json_start = -1
        
        for i, line in enumerate(output_lines):
            if line.strip().startswith('{'):
                json_start = i
                break
        
        if json_start >= 0:
            json_output = '\n'.join(output_lines[json_start:])
            monitoring_results = json.loads(json_output)
        else:
            monitoring_results = {
                "success": result.returncode == 0,
                "error": "Could not parse monitoring setup results",
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        
        return monitoring_results
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Monitoring setup timed out after 5 minutes"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Monitoring setup failed: {str(e)}"
        }

def main():
    """Main post-deployment validation function"""
    
    print("🚀 EdweavePack Post-Deployment Validation")
    print("=" * 50)
    
    # Get parameters
    alb_endpoint = os.getenv("ALB_ENDPOINT") or (sys.argv[1] if len(sys.argv) > 1 else None)
    region = os.getenv("AWS_REGION", "us-east-1")
    
    if not alb_endpoint:
        print("❌ ALB endpoint required. Set ALB_ENDPOINT env var or pass as argument")
        sys.exit(1)
    
    validation_results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "alb_endpoint": alb_endpoint,
        "region": region,
        "smoke_tests": {},
        "monitoring": {},
        "overall_success": False
    }
    
    # Step 1: Run smoke tests
    print(f"\n🔍 Step 1: Smoke Tests (Endpoint: {alb_endpoint})")
    smoke_results = run_smoke_tests(alb_endpoint)
    validation_results["smoke_tests"] = smoke_results
    
    if smoke_results.get("overall_success"):
        print("✅ Smoke tests passed")
    else:
        print("❌ Smoke tests failed")
        print(f"Error: {smoke_results.get('error', 'Unknown error')}")
    
    # Step 2: Setup monitoring
    print(f"\n📊 Step 2: CloudWatch Monitoring Setup (Region: {region})")
    monitoring_results = setup_monitoring(region)
    validation_results["monitoring"] = monitoring_results
    
    if monitoring_results.get("success"):
        print("✅ Monitoring setup completed")
        if monitoring_results.get("dashboard_url"):
            print(f"📈 Dashboard: {monitoring_results['dashboard_url']}")
    else:
        print("❌ Monitoring setup failed")
        print(f"Error: {monitoring_results.get('error', 'Unknown error')}")
    
    # Overall success
    validation_results["overall_success"] = (
        smoke_results.get("overall_success", False) and 
        monitoring_results.get("success", False)
    )
    
    # Summary
    print(f"\n📋 Validation Summary:")
    print("=" * 30)
    print(f"Smoke Tests: {'✅ PASS' if smoke_results.get('overall_success') else '❌ FAIL'}")
    print(f"Monitoring: {'✅ PASS' if monitoring_results.get('success') else '❌ FAIL'}")
    print(f"Overall: {'✅ SUCCESS' if validation_results['overall_success'] else '❌ FAILURE'}")
    
    # Output detailed results
    print(f"\n📄 Detailed Results:")
    print(json.dumps(validation_results, indent=2))
    
    # Return appropriate exit code
    sys.exit(0 if validation_results["overall_success"] else 1)

if __name__ == "__main__":
    main()