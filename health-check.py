#!/usr/bin/env python3
"""
Comprehensive health check script for EdweavePack deployment
"""

import requests
import time
import sys
import json
from datetime import datetime

class HealthChecker:
    def __init__(self, base_url="http://localhost"):
        self.base_url = base_url
        self.backend_url = f"{base_url}:8000"
        self.frontend_url = f"{base_url}:3000"
        self.results = []
    
    def log_result(self, test_name, status, message, response_time=None):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "response_time": response_time
        }
        self.results.append(result)
        
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        time_str = f" ({response_time:.2f}s)" if response_time else ""
        print(f"{status_icon} {test_name}: {message}{time_str}")
    
    def test_backend_health(self):
        """Test backend health endpoint"""
        try:
            start_time = time.time()
            response = requests.get(f"{self.backend_url}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_result("Backend Health", "PASS", "Backend is healthy", response_time)
                return True
            else:
                self.log_result("Backend Health", "FAIL", f"Backend returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_result("Backend Health", "FAIL", f"Backend connection failed: {str(e)}")
            return False
    
    def test_frontend_health(self):
        """Test frontend availability"""
        try:
            start_time = time.time()
            response = requests.get(self.frontend_url, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.log_result("Frontend Health", "PASS", "Frontend is accessible", response_time)
                return True
            else:
                self.log_result("Frontend Health", "FAIL", f"Frontend returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_result("Frontend Health", "FAIL", f"Frontend connection failed: {str(e)}")
            return False
    
    def test_api_endpoints(self):
        """Test critical API endpoints"""
        endpoints = [
            ("/", "Root endpoint"),
            ("/docs", "API documentation"),
            ("/api/auth/register", "Registration endpoint", "POST"),
            ("/api/auth/token", "Login endpoint", "POST"),
        ]
        
        all_passed = True
        for endpoint_data in endpoints:
            endpoint = endpoint_data[0]
            description = endpoint_data[1]
            method = endpoint_data[2] if len(endpoint_data) > 2 else "GET"
            
            try:
                start_time = time.time()
                if method == "GET":
                    response = requests.get(f"{self.backend_url}{endpoint}", timeout=5)
                else:
                    # For POST endpoints, just check if they're reachable (will return 422 for missing data)
                    response = requests.post(f"{self.backend_url}{endpoint}", timeout=5)
                
                response_time = time.time() - start_time
                
                # Accept 200, 422 (validation error), and 405 (method not allowed) as "healthy"
                if response.status_code in [200, 422, 405]:
                    self.log_result(f"API {description}", "PASS", f"Endpoint reachable", response_time)
                else:
                    self.log_result(f"API {description}", "WARN", f"Unexpected status {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                self.log_result(f"API {description}", "FAIL", f"Endpoint failed: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_database_connection(self):
        """Test database connectivity through API"""
        try:
            # Try to register a test user (will fail but shows DB is connected)
            test_data = {
                "email": "healthcheck@test.com",
                "password": "testpass123",
                "full_name": "Health Check",
                "role": "teacher",
                "institution": "Test"
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.backend_url}/api/auth/register", 
                json=test_data,
                timeout=10
            )
            response_time = time.time() - start_time
            
            # We expect this to fail with 400 (user exists) or succeed with 200
            if response.status_code in [200, 400]:
                self.log_result("Database Connection", "PASS", "Database is accessible", response_time)
                return True
            else:
                self.log_result("Database Connection", "WARN", f"Unexpected response: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_result("Database Connection", "FAIL", f"Database test failed: {str(e)}")
            return False
    
    def test_cors_configuration(self):
        """Test CORS configuration"""
        try:
            headers = {
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            
            start_time = time.time()
            response = requests.options(f"{self.backend_url}/api/auth/register", headers=headers, timeout=5)
            response_time = time.time() - start_time
            
            cors_headers = response.headers.get('Access-Control-Allow-Origin')
            if cors_headers:
                self.log_result("CORS Configuration", "PASS", "CORS headers present", response_time)
                return True
            else:
                self.log_result("CORS Configuration", "FAIL", "CORS headers missing")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_result("CORS Configuration", "FAIL", f"CORS test failed: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all health checks"""
        print("🏥 Starting EdweavePack Health Check...")
        print("=" * 50)
        
        tests = [
            self.test_backend_health,
            self.test_frontend_health,
            self.test_api_endpoints,
            self.test_database_connection,
            self.test_cors_configuration
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            print()  # Add spacing between tests
        
        print("=" * 50)
        print(f"📊 Health Check Summary: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All systems are healthy!")
            return True
        elif passed >= total * 0.8:
            print("⚠️  Most systems are healthy, but some issues detected")
            return False
        else:
            print("🚨 Critical issues detected!")
            return False
    
    def save_results(self, filename="health_check_results.json"):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_tests": len(self.results),
                    "passed": len([r for r in self.results if r["status"] == "PASS"]),
                    "failed": len([r for r in self.results if r["status"] == "FAIL"]),
                    "warnings": len([r for r in self.results if r["status"] == "WARN"])
                },
                "results": self.results
            }, indent=2)
        print(f"📄 Results saved to {filename}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="EdweavePack Health Check")
    parser.add_argument("--url", default="http://localhost", help="Base URL for health check")
    parser.add_argument("--save", action="store_true", help="Save results to JSON file")
    
    args = parser.parse_args()
    
    checker = HealthChecker(args.url)
    success = checker.run_all_tests()
    
    if args.save:
        checker.save_results()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()