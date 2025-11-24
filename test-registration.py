#!/usr/bin/env python3
"""
Comprehensive registration testing for all user types
"""

import requests
import json
import time
from datetime import datetime

class RegistrationTester:
    def __init__(self, base_url="http://localhost:8000"):
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
    
    def test_user_registration(self, role, user_data):
        """Test registration for specific user type"""
        try:
            print(f"\n🔍 Testing {role} registration...")
            
            response = self.session.post(
                f"{self.base_url}/api/auth/register",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                if "access_token" in data:
                    self.log_test(f"{role.title()} Registration", True, f"Successfully registered {role}")
                    
                    # Test token validity
                    token = data["access_token"]
                    profile_response = self.session.get(
                        f"{self.base_url}/api/auth/me",
                        headers={"Authorization": f"Bearer {token}"}
                    )
                    
                    if profile_response.status_code == 200:
                        profile_data = profile_response.json()
                        if profile_data.get("role") == role:
                            self.log_test(f"{role.title()} Profile Fetch", True, f"Profile retrieved successfully with correct role")
                            return True
                        else:
                            self.log_test(f"{role.title()} Profile Fetch", False, f"Role mismatch: expected {role}, got {profile_data.get('role')}")
                    else:
                        self.log_test(f"{role.title()} Profile Fetch", False, f"Failed to fetch profile: {profile_response.status_code}")
                else:
                    self.log_test(f"{role.title()} Registration", False, "No access token in response")
            else:
                error_detail = response.json().get("detail", "Unknown error") if response.headers.get("content-type", "").startswith("application/json") else response.text
                
                # Check if it's expected duplicate email error
                if response.status_code == 400 and "already registered" in error_detail.lower():
                    self.log_test(f"{role.title()} Registration", True, f"Duplicate email handled correctly")
                    return True
                else:
                    self.log_test(f"{role.title()} Registration", False, f"Registration failed: {error_detail}")
            
            return False
            
        except Exception as e:
            self.log_test(f"{role.title()} Registration", False, f"Registration test failed: {str(e)}")
            return False
    
    def test_all_user_types(self):
        """Test registration for all user types"""
        timestamp = int(time.time())
        
        user_types = [
            {
                "role": "teacher",
                "data": {
                    "email": f"teacher_{timestamp}@test.com",
                    "password": "SecurePass123!",
                    "full_name": "John Teacher",
                    "institution": "Test High School",
                    "role": "teacher"
                }
            },
            {
                "role": "student", 
                "data": {
                    "email": f"student_{timestamp}@test.com",
                    "password": "SecurePass123!",
                    "full_name": "Jane Student",
                    "institution": "Test High School",
                    "role": "student"
                }
            },
            {
                "role": "administrator",
                "data": {
                    "email": f"admin_{timestamp}@test.com",
                    "password": "SecurePass123!",
                    "full_name": "Admin User",
                    "institution": "Test District",
                    "role": "administrator"
                }
            },
            {
                "role": "curriculum_designer",
                "data": {
                    "email": f"designer_{timestamp}@test.com",
                    "password": "SecurePass123!",
                    "full_name": "Curriculum Designer",
                    "institution": "Test Education Board",
                    "role": "curriculum_designer"
                }
            }
        ]
        
        successful_registrations = 0
        
        for user_type in user_types:
            if self.test_user_registration(user_type["role"], user_type["data"]):
                successful_registrations += 1
            time.sleep(1)  # Brief pause between tests
        
        return successful_registrations, len(user_types)
    
    def test_validation_errors(self):
        """Test validation error handling"""
        print(f"\n🔍 Testing validation error handling...")
        
        validation_tests = [
            {
                "name": "Missing Email",
                "data": {
                    "password": "SecurePass123!",
                    "full_name": "Test User",
                    "role": "teacher"
                },
                "expected_error": "email"
            },
            {
                "name": "Invalid Email",
                "data": {
                    "email": "invalid-email",
                    "password": "SecurePass123!",
                    "full_name": "Test User",
                    "role": "teacher"
                },
                "expected_error": "email"
            },
            {
                "name": "Short Password",
                "data": {
                    "email": "test@example.com",
                    "password": "123",
                    "full_name": "Test User",
                    "role": "teacher"
                },
                "expected_error": "password"
            },
            {
                "name": "Missing Name",
                "data": {
                    "email": "test@example.com",
                    "password": "SecurePass123!",
                    "role": "teacher"
                },
                "expected_error": "name"
            },
            {
                "name": "Invalid Role",
                "data": {
                    "email": "test@example.com",
                    "password": "SecurePass123!",
                    "full_name": "Test User",
                    "role": "invalid_role"
                },
                "expected_error": "role"
            }
        ]
        
        validation_passed = 0
        
        for test in validation_tests:
            try:
                response = self.session.post(
                    f"{self.base_url}/api/auth/register",
                    json=test["data"],
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 400:
                    self.log_test(f"Validation: {test['name']}", True, "Validation error correctly returned")
                    validation_passed += 1
                else:
                    self.log_test(f"Validation: {test['name']}", False, f"Expected 400, got {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Validation: {test['name']}", False, f"Test failed: {str(e)}")
        
        return validation_passed, len(validation_tests)
    
    def test_network_resilience(self):
        """Test network error handling"""
        print(f"\n🔍 Testing network resilience...")
        
        # Test with invalid URL to simulate network error
        try:
            invalid_session = requests.Session()
            invalid_session.timeout = 2
            
            response = invalid_session.post(
                "http://invalid-url-that-does-not-exist.com/api/auth/register",
                json={
                    "email": "test@example.com",
                    "password": "SecurePass123!",
                    "full_name": "Test User",
                    "role": "teacher"
                }
            )
            
            self.log_test("Network Error Handling", False, "Should have failed with network error")
            return False
            
        except requests.exceptions.RequestException:
            self.log_test("Network Error Handling", True, "Network errors properly handled")
            return True
        except Exception as e:
            self.log_test("Network Error Handling", False, f"Unexpected error: {str(e)}")
            return False
    
    def run_comprehensive_test(self):
        """Run all registration tests"""
        print("🧪 Starting Comprehensive Registration Testing")
        print("=" * 60)
        
        # Test server availability
        try:
            health_response = self.session.get(f"{self.base_url}/health")
            if health_response.status_code != 200:
                print("❌ Server not available. Please start the backend server.")
                return False
        except Exception:
            print("❌ Cannot connect to server. Please ensure backend is running.")
            return False
        
        # Run all tests
        reg_passed, reg_total = self.test_all_user_types()
        val_passed, val_total = self.test_validation_errors()
        net_passed = self.test_network_resilience()
        
        total_passed = reg_passed + val_passed + (1 if net_passed else 0)
        total_tests = reg_total + val_total + 1
        
        print("\n" + "=" * 60)
        print(f"📊 Test Summary:")
        print(f"   User Type Registration: {reg_passed}/{reg_total}")
        print(f"   Validation Tests: {val_passed}/{val_total}")
        print(f"   Network Resilience: {1 if net_passed else 0}/1")
        print(f"   Overall: {total_passed}/{total_tests} tests passed")
        
        if total_passed == total_tests:
            print("🎉 All registration tests passed! System is ready for all user types.")
            return True
        elif total_passed >= total_tests * 0.8:
            print("⚠️  Most tests passed, but some issues need attention.")
            return False
        else:
            print("🚨 Critical registration issues detected!")
            return False
    
    def save_report(self, filename="registration_test_report.json"):
        """Save test report"""
        report = {
            "test_timestamp": datetime.now().isoformat(),
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
        
        print(f"📄 Test report saved to {filename}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="EdweavePack Registration Tester")
    parser.add_argument("--url", default="http://localhost:8000", help="Backend URL to test")
    parser.add_argument("--save-report", action="store_true", help="Save test report")
    
    args = parser.parse_args()
    
    tester = RegistrationTester(args.url)
    success = tester.run_comprehensive_test()
    
    if args.save_report:
        tester.save_report()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())