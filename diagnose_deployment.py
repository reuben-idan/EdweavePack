#!/usr/bin/env python3
"""Diagnose existing AWS deployment and AI implementation"""

import requests
import json
import time

def check_deployment_status():
    """Check current deployment status"""
    base_url = "http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com"
    
    print("DEPLOYMENT DIAGNOSIS")
    print("=" * 30)
    
    # Test 1: Basic connectivity
    try:
        response = requests.get(base_url, timeout=10)
        print(f"Frontend Status: {response.status_code}")
        if response.status_code == 200:
            print("  Frontend: WORKING")
        else:
            print(f"  Frontend: ERROR - {response.status_code}")
    except Exception as e:
        print(f"  Frontend: FAILED - {e}")
    
    # Test 2: API root
    try:
        response = requests.get(f"{base_url}/api", timeout=10)
        print(f"API Root Status: {response.status_code}")
        if response.status_code in [200, 404, 422]:
            print("  API: RESPONDING")
        else:
            print(f"  API: ERROR - {response.status_code}")
    except Exception as e:
        print(f"  API: FAILED - {e}")
    
    # Test 3: Health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Health Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("  Health Response:")
            print(f"    Status: {data.get('status')}")
            print(f"    Database: {data.get('database')}")
            print(f"    AI Service: {data.get('ai_service')}")
        else:
            print(f"  Health: ERROR - {response.status_code}")
            if response.text:
                print(f"    Error: {response.text[:200]}")
    except Exception as e:
        print(f"  Health: FAILED - {e}")
    
    # Test 4: Curriculum endpoints
    endpoints = [
        "/api/curriculum/",
        "/api/curriculum/test/1",
        "/api/agents/kiro/config"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            print(f"{endpoint}: {response.status_code}")
            
            if response.status_code == 500:
                print(f"  500 ERROR DETECTED: {endpoint}")
                if response.text:
                    error_text = response.text[:300]
                    print(f"    Error details: {error_text}")
            elif response.status_code in [200, 401]:
                print(f"  {endpoint}: WORKING")
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'ai' in str(data).lower():
                            print(f"    AI features detected")
                    except:
                        pass
        except Exception as e:
            print(f"  {endpoint}: FAILED - {e}")

def check_backend_logs():
    """Check for backend issues"""
    print("\nBACKEND ANALYSIS")
    print("=" * 20)
    
    base_url = "http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com"
    
    # Test specific AI endpoints that might be causing 500 errors
    ai_endpoints = [
        ("/api/curriculum/", "POST", {"title": "Test", "subject": "Math", "grade_level": "High School", "source_content": "Test content"}),
        ("/api/assessment/generate", "POST", {"curriculum_id": 1, "assessment_type": "test"}),
        ("/api/agents/curriculum/generate", "POST", {"content": "test", "subject": "Math", "level": "High School"})
    ]
    
    for endpoint, method, data in ai_endpoints:
        try:
            if method == "POST":
                response = requests.post(f"{base_url}{endpoint}", json=data, timeout=15)
            else:
                response = requests.get(f"{base_url}{endpoint}", timeout=15)
            
            print(f"{method} {endpoint}: {response.status_code}")
            
            if response.status_code == 500:
                print(f"  CRITICAL: 500 error in {endpoint}")
                try:
                    error_data = response.json()
                    print(f"    Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"    Raw error: {response.text[:200]}")
            elif response.status_code in [200, 201]:
                print(f"  SUCCESS: {endpoint} working")
            elif response.status_code == 401:
                print(f"  AUTH REQUIRED: {endpoint} (endpoint exists)")
            else:
                print(f"  STATUS: {endpoint} returned {response.status_code}")
                
        except Exception as e:
            print(f"  ERROR: {endpoint} - {e}")

def check_ai_services():
    """Check AI service implementation"""
    print("\nAI SERVICES CHECK")
    print("=" * 20)
    
    # Check if AI services are properly imported and working
    base_url = "http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com"
    
    try:
        # Test the health endpoint for AI service status
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            ai_service = data.get('ai_service', {})
            
            print("AI Service Status:")
            for key, value in ai_service.items():
                print(f"  {key}: {value}")
            
            if ai_service:
                print("AI services are configured")
            else:
                print("AI services not detected in health check")
        else:
            print("Cannot check AI services - health endpoint unavailable")
    except Exception as e:
        print(f"AI service check failed: {e}")

def identify_500_errors():
    """Identify specific endpoints causing 500 errors"""
    print("\n500 ERROR ANALYSIS")
    print("=" * 25)
    
    base_url = "http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com"
    
    # Test all major endpoints
    test_endpoints = [
        "/",
        "/api",
        "/health", 
        "/api/auth/register",
        "/api/curriculum/",
        "/api/curriculum/test/1",
        "/api/assessment/",
        "/api/analytics/dashboard",
        "/api/agents/kiro/config"
    ]
    
    error_endpoints = []
    working_endpoints = []
    
    for endpoint in test_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 500:
                error_endpoints.append(endpoint)
                print(f"500 ERROR: {endpoint}")
                # Try to get error details
                try:
                    error_data = response.json()
                    print(f"  Details: {error_data.get('detail', 'No details')}")
                except:
                    print(f"  Raw: {response.text[:100]}")
            elif response.status_code in [200, 401, 404]:
                working_endpoints.append(endpoint)
                print(f"WORKING: {endpoint} ({response.status_code})")
            else:
                print(f"OTHER: {endpoint} ({response.status_code})")
                
        except Exception as e:
            print(f"FAILED: {endpoint} - {e}")
    
    print(f"\nSUMMARY:")
    print(f"  Working endpoints: {len(working_endpoints)}")
    print(f"  500 error endpoints: {len(error_endpoints)}")
    
    if error_endpoints:
        print(f"  CRITICAL: These endpoints have 500 errors:")
        for endpoint in error_endpoints:
            print(f"    - {endpoint}")
    
    return len(error_endpoints) == 0

def main():
    """Main diagnosis function"""
    print("AWS DEPLOYMENT & AI IMPLEMENTATION DIAGNOSIS")
    print("=" * 50)
    
    # Run all diagnostic checks
    check_deployment_status()
    check_backend_logs()
    check_ai_services()
    no_500_errors = identify_500_errors()
    
    print(f"\nDIAGNOSIS COMPLETE")
    print("=" * 20)
    
    if no_500_errors:
        print("STATUS: HEALTHY - No 500 errors detected")
        print("AI implementation appears to be working")
    else:
        print("STATUS: ISSUES DETECTED - 500 errors found")
        print("Backend AI implementation needs attention")
        print("\nRECOMMENDATIONS:")
        print("1. Check backend logs for Python import errors")
        print("2. Verify AI service dependencies are installed")
        print("3. Check database connectivity")
        print("4. Validate environment variables")

if __name__ == "__main__":
    main()