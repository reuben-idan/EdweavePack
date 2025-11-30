#!/usr/bin/env python3
"""
Post-deployment smoke tests for EdweavePack
"""

import requests
import json
import time
import os
import sys
from typing import Dict, Any

class SmokeTests:
    def __init__(self, alb_endpoint: str):
        self.alb_endpoint = alb_endpoint.rstrip('/')
        self.results = []
        
    def run_test(self, test_name: str, test_func) -> bool:
        """Run individual test and record result"""
        print(f"🧪 Running {test_name}...")
        try:
            result = test_func()
            self.results.append({
                "test": test_name,
                "status": "PASS" if result else "FAIL",
                "success": result
            })
            print(f"✅ {test_name}: {'PASS' if result else 'FAIL'}")
            return result
        except Exception as e:
            self.results.append({
                "test": test_name,
                "status": "ERROR",
                "error": str(e),
                "success": False
            })
            print(f"❌ {test_name}: ERROR - {e}")
            return False
    
    def test_frontend_health(self) -> bool:
        """Test ALB endpoint returns 200"""
        response = requests.get(f"{self.alb_endpoint}/", timeout=10)
        return response.status_code == 200
    
    def test_backend_health(self) -> bool:
        """Test backend health endpoint returns 200"""
        response = requests.get(f"{self.alb_endpoint}/health", timeout=10)
        return response.status_code == 200
    
    def test_auth_flow(self) -> bool:
        """Test complete auth flow with Cognito"""
        # Step 1: Register test teacher
        register_payload = {
            "email": f"test-{int(time.time())}@edweavepack.com",
            "name": "Test Teacher",
            "password": "TestPass123!",
            "institution": "Test School"
        }
        
        register_response = requests.post(
            f"{self.alb_endpoint}/api/auth/register",
            json=register_payload,
            timeout=10
        )
        
        if register_response.status_code not in [200, 201]:
            print(f"Registration failed: {register_response.status_code}")
            return False
        
        # Step 2: Login to get token
        login_payload = {
            "email": register_payload["email"],
            "password": register_payload["password"]
        }
        
        login_response = requests.post(
            f"{self.alb_endpoint}/api/auth/token",
            json=login_payload,
            timeout=10
        )
        
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code}")
            return False
        
        token_data = login_response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            print("No access token received")
            return False
        
        # Step 3: Test authenticated API call
        curriculum_payload = {
            "title": "Smoke Test Curriculum",
            "description": "Test curriculum for smoke testing",
            "subject": "Testing",
            "grade_level": "Test Level"
        }
        
        headers = {"Authorization": f"Bearer {access_token}"}
        curriculum_response = requests.post(
            f"{self.alb_endpoint}/api/curriculum/",
            json=curriculum_payload,
            headers=headers,
            timeout=10
        )
        
        return curriculum_response.status_code in [200, 201]
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all smoke tests"""
        print("🚀 Starting EdweavePack Smoke Tests")
        print("=" * 40)
        
        # Run tests
        test1 = self.run_test("Frontend Health Check", self.test_frontend_health)
        test2 = self.run_test("Backend Health Check", self.test_backend_health)
        test3 = self.run_test("Auth Flow Test", self.test_auth_flow)
        
        # Summary
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        
        print(f"\n📊 Test Summary:")
        print(f"Total: {total_tests}, Passed: {passed_tests}, Failed: {total_tests - passed_tests}")
        
        overall_success = all(r["success"] for r in self.results)
        
        return {
            "overall_success": overall_success,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "results": self.results,
            "endpoint": self.alb_endpoint
        }

def main():
    """Main smoke test function"""
    
    # Get ALB endpoint from environment or argument
    alb_endpoint = os.getenv("ALB_ENDPOINT") or sys.argv[1] if len(sys.argv) > 1 else None
    
    if not alb_endpoint:
        print("❌ ALB endpoint required. Set ALB_ENDPOINT env var or pass as argument")
        sys.exit(1)
    
    # Run smoke tests
    smoke_tests = SmokeTests(alb_endpoint)
    results = smoke_tests.run_all_tests()
    
    # Output results as JSON for CI/CD
    print(f"\n📋 Results JSON:")
    print(json.dumps(results, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if results["overall_success"] else 1)

if __name__ == "__main__":
    main()