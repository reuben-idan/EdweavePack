#!/usr/bin/env python3
"""
Deployment validation script for EdweavePack
Tests all critical functionality after deployment
"""

import requests
import time
import json
import sys
from datetime import datetime

class DeploymentValidator:
    def __init__(self, base_url="https://edweavepack.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 30
        self.test_results = []
    
    def log_test(self, test_name, success, message, details=None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        icon = "✅" if success else "❌"
        print(f"{icon} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_ssl_certificate(self):
        """Test SSL certificate validity"""
        try:
            response = self.session.get(self.base_url)
            if response.url.startswith('https://'):
                self.log_test("SSL Certificate", True, "SSL certificate is valid and working")
                return True
            else:
                self.log_test("SSL Certificate", False, "Site is not using HTTPS")
                return False
        except Exception as e:
            self.log_test("SSL Certificate", False, "SSL test failed", str(e))
            return False
    
    def test_frontend_loading(self):
        """Test frontend application loading"""
        try:
            response = self.session.get(self.base_url)
            if response.status_code == 200 and 'EdweavePack' in response.text:
                self.log_test("Frontend Loading", True, "Frontend loads successfully")
                return True
            else:
                self.log_test("Frontend Loading", False, f"Frontend failed to load properly (status: {response.status_code})")
                return False
        except Exception as e:
            self.log_test("Frontend Loading", False, "Frontend loading test failed", str(e))
            return False
    
    def test_api_health(self):
        """Test API health endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                self.log_test("API Health", True, "API health endpoint responding")
                return True
            else:
                self.log_test("API Health", False, f"API health check failed (status: {response.status_code})")
                return False
        except Exception as e:
            self.log_test("API Health", False, "API health test failed", str(e))
            return False
    
    def test_api_documentation(self):
        """Test API documentation accessibility"""
        try:
            response = self.session.get(f"{self.base_url}/docs")
            if response.status_code == 200:
                self.log_test("API Documentation", True, "API documentation is accessible")
                return True
            else:
                self.log_test("API Documentation", False, f"API docs not accessible (status: {response.status_code})")
                return False
        except Exception as e:
            self.log_test("API Documentation", False, "API documentation test failed", str(e))
            return False
    
    def test_user_registration(self):
        """Test user registration functionality"""
        try:
            test_user = {
                "email": f"test_{int(time.time())}@example.com",
                "password": "TestPassword123!",
                "full_name": "Test User",
                "role": "teacher",
                "institution": "Test Institution"
            }
            
            response = self.session.post(f"{self.base_url}/api/auth/register", json=test_user)
            
            if response.status_code in [200, 201]:
                self.log_test("User Registration", True, "User registration working")
                return True
            elif response.status_code == 400:
                # Check if it's a validation error (expected for duplicate emails)
                error_detail = response.json().get('detail', '')
                if 'already registered' in error_detail.lower():
                    self.log_test("User Registration", True, "Registration endpoint working (duplicate email handled)")
                    return True
                else:
                    self.log_test("User Registration", False, f"Registration validation error: {error_detail}")
                    return False
            else:
                self.log_test("User Registration", False, f"Registration failed (status: {response.status_code})")
                return False
        except Exception as e:
            self.log_test("User Registration", False, "Registration test failed", str(e))
            return False
    
    def test_cors_headers(self):
        """Test CORS configuration"""
        try:
            headers = {
                'Origin': 'https://edweavepack.com',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type,Authorization'
            }
            
            response = self.session.options(f"{self.base_url}/api/auth/register", headers=headers)
            
            cors_origin = response.headers.get('Access-Control-Allow-Origin')
            cors_methods = response.headers.get('Access-Control-Allow-Methods')
            
            if cors_origin and cors_methods:
                self.log_test("CORS Configuration", True, "CORS headers properly configured")
                return True
            else:
                self.log_test("CORS Configuration", False, "CORS headers missing or incomplete")
                return False
        except Exception as e:
            self.log_test("CORS Configuration", False, "CORS test failed", str(e))
            return False
    
    def test_response_times(self):
        """Test response times for critical endpoints"""
        endpoints = [
            ('/', 'Homepage'),
            ('/health', 'Health Check'),
            ('/docs', 'API Docs'),
            ('/api/auth/register', 'Registration API')
        ]
        
        all_fast = True
        for endpoint, name in endpoints:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.base_url}{endpoint}")
                response_time = time.time() - start_time
                
                if response_time < 2.0:  # Less than 2 seconds
                    self.log_test(f"Response Time - {name}", True, f"Fast response ({response_time:.2f}s)")
                elif response_time < 5.0:  # Less than 5 seconds
                    self.log_test(f"Response Time - {name}", True, f"Acceptable response ({response_time:.2f}s)")
                else:
                    self.log_test(f"Response Time - {name}", False, f"Slow response ({response_time:.2f}s)")
                    all_fast = False
            except Exception as e:
                self.log_test(f"Response Time - {name}", False, "Response time test failed", str(e))
                all_fast = False
        
        return all_fast
    
    def test_security_headers(self):
        """Test security headers"""
        try:
            response = self.session.get(self.base_url)
            headers = response.headers
            
            security_checks = [
                ('X-Content-Type-Options', 'nosniff'),
                ('X-Frame-Options', ['DENY', 'SAMEORIGIN']),
                ('X-XSS-Protection', '1'),
            ]
            
            all_secure = True
            for header, expected in security_checks:
                if header in headers:
                    if isinstance(expected, list):
                        if any(exp in headers[header] for exp in expected):
                            continue
                    elif expected in headers[header]:
                        continue
                
                self.log_test(f"Security Header - {header}", False, f"Missing or incorrect {header} header")
                all_secure = False
            
            if all_secure:
                self.log_test("Security Headers", True, "Security headers properly configured")
            
            return all_secure
        except Exception as e:
            self.log_test("Security Headers", False, "Security headers test failed", str(e))
            return False
    
    def run_validation(self):
        """Run all validation tests"""
        print("🚀 Starting EdweavePack Deployment Validation")
        print("=" * 60)
        
        tests = [
            ("SSL Certificate", self.test_ssl_certificate),
            ("Frontend Loading", self.test_frontend_loading),
            ("API Health", self.test_api_health),
            ("API Documentation", self.test_api_documentation),
            ("User Registration", self.test_user_registration),
            ("CORS Configuration", self.test_cors_headers),
            ("Response Times", self.test_response_times),
            ("Security Headers", self.test_security_headers),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running {test_name} test...")
            if test_func():
                passed += 1
        
        print("\n" + "=" * 60)
        print(f"📊 Validation Summary: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 Deployment validation successful! All systems operational.")
            return True
        elif passed >= total * 0.8:
            print("⚠️  Deployment mostly successful, but some issues need attention.")
            return False
        else:
            print("🚨 Deployment validation failed! Critical issues detected.")
            return False
    
    def save_report(self, filename="deployment_validation_report.json"):
        """Save validation report"""
        report = {
            "validation_timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "summary": {
                "total_tests": len(self.test_results),
                "passed": len([r for r in self.test_results if r["success"]]),
                "failed": len([r for r in self.test_results if not r["success"]])
            },
            "test_results": self.test_results
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Validation report saved to {filename}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="EdweavePack Deployment Validator")
    parser.add_argument("--url", default="https://edweavepack.com", help="Base URL to validate")
    parser.add_argument("--save-report", action="store_true", help="Save validation report")
    
    args = parser.parse_args()
    
    validator = DeploymentValidator(args.url)
    success = validator.run_validation()
    
    if args.save_report:
        validator.save_report()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()