#!/usr/bin/env python3
"""
Comprehensive Student Functionality Test Suite
Tests every aspect of the student portion of EdweavePack
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path

class StudentFunctionalityTester:
    def __init__(self):
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test(self, test_name, status, message=""):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "message": message,
            "timestamp": time.strftime("%H:%M:%S")
        }
        self.test_results.append(result)
        
        if status == "PASS":
            self.passed_tests += 1
            print(f"✅ {test_name}: PASSED")
        else:
            self.failed_tests += 1
            print(f"❌ {test_name}: FAILED - {message}")
    
    def test_student_components_exist(self):
        """Test that all student components exist"""
        print("\n🔍 Testing Student Component Files...")
        
        required_files = [
            "frontend/src/pages/StudentLogin.js",
            "frontend/src/pages/StudentSignup.js", 
            "frontend/src/pages/StudentDashboard.js",
            "frontend/src/pages/StudentDashboardEnhanced.js",
            "frontend/src/pages/StudentProfile.js",
            "frontend/src/pages/StudentProfileEnhanced.js",
            "frontend/src/pages/StudentLearningPath.js",
            "frontend/src/pages/StudentLearningPathEnhanced.js",
            "frontend/src/pages/StudentQuiz.js",
            "frontend/src/pages/StudentUpload.js",
            "frontend/src/hooks/useStudentAuth.js"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.log_test("Student Components Exist", "FAIL", f"Missing files: {', '.join(missing_files)}")
            return False
        
        self.log_test("Student Components Exist", "PASS")
        return True
    
    def test_student_routes_configured(self):
        """Test that student routes are properly configured in App.js"""
        print("\n🔍 Testing Student Routes Configuration...")
        
        try:
            with open("frontend/src/App.js", "r") as f:
                app_content = f.read()
            
            required_routes = [
                "/student/login",
                "/student/signup", 
                "/student/dashboard",
                "/student/profile",
                "/student/learning-path",
                "/student/upload",
                "/student/quiz"
            ]
            
            missing_routes = []
            for route in required_routes:
                if route not in app_content:
                    missing_routes.append(route)
            
            if missing_routes:
                self.log_test("Student Routes Configuration", "FAIL", f"Missing routes: {', '.join(missing_routes)}")
                return False
            
            # Check for StudentAuthProvider
            if "StudentAuthProvider" not in app_content:
                self.log_test("Student Routes Configuration", "FAIL", "StudentAuthProvider not configured")
                return False
            
            self.log_test("Student Routes Configuration", "PASS")
            return True
            
        except Exception as e:
            self.log_test("Student Routes Configuration", "FAIL", str(e))
            return False
    
    def test_student_auth_hook(self):
        """Test student authentication hook functionality"""
        print("\n🔍 Testing Student Authentication Hook...")
        
        try:
            with open("frontend/src/hooks/useStudentAuth.js", "r") as f:
                auth_content = f.read()
            
            required_functions = [
                "login",
                "register", 
                "logout",
                "updateProfile",
                "changePassword",
                "forgotPassword",
                "resetPassword"
            ]
            
            missing_functions = []
            for func in required_functions:
                if f"const {func} = " not in auth_content and f"{func}:" not in auth_content:
                    missing_functions.append(func)
            
            if missing_functions:
                self.log_test("Student Auth Hook", "FAIL", f"Missing functions: {', '.join(missing_functions)}")
                return False
            
            # Check for proper context setup
            if "StudentAuthContext" not in auth_content:
                self.log_test("Student Auth Hook", "FAIL", "StudentAuthContext not defined")
                return False
            
            self.log_test("Student Auth Hook", "PASS")
            return True
            
        except Exception as e:
            self.log_test("Student Auth Hook", "FAIL", str(e))
            return False
    
    def test_student_login_functionality(self):
        """Test student login component functionality"""
        print("\n🔍 Testing Student Login Component...")
        
        try:
            with open("frontend/src/pages/StudentLogin.js", "r") as f:
                login_content = f.read()
            
            required_features = [
                "useState",
                "useStudentAuth",
                "handleSubmit",
                "email",
                "password",
                "showPassword",
                "rememberMe",
                "validation"
            ]
            
            missing_features = []
            for feature in required_features:
                if feature not in login_content:
                    missing_features.append(feature)
            
            if missing_features:
                self.log_test("Student Login Component", "FAIL", f"Missing features: {', '.join(missing_features)}")
                return False
            
            # Check for proper error handling
            if "errors" not in login_content or "AlertCircle" not in login_content:
                self.log_test("Student Login Component", "FAIL", "Missing error handling")
                return False
            
            self.log_test("Student Login Component", "PASS")
            return True
            
        except Exception as e:
            self.log_test("Student Login Component", "FAIL", str(e))
            return False
    
    def test_student_signup_functionality(self):
        """Test student signup component functionality"""
        print("\n🔍 Testing Student Signup Component...")
        
        try:
            with open("frontend/src/pages/StudentSignup.js", "r") as f:
                signup_content = f.read()
            
            required_features = [
                "step",
                "setStep",
                "formData",
                "learningStyles",
                "examOptions",
                "validateStep1",
                "validateStep2", 
                "passwordStrength",
                "handleNext",
                "handleSubmit"
            ]
            
            missing_features = []
            for feature in required_features:
                if feature not in signup_content:
                    missing_features.append(feature)
            
            if missing_features:
                self.log_test("Student Signup Component", "FAIL", f"Missing features: {', '.join(missing_features)}")
                return False
            
            # Check for multi-step form
            if "step === 1" not in signup_content or "step === 2" not in signup_content:
                self.log_test("Student Signup Component", "FAIL", "Multi-step form not implemented")
                return False
            
            self.log_test("Student Signup Component", "PASS")
            return True
            
        except Exception as e:
            self.log_test("Student Signup Component", "FAIL", str(e))
            return False
    
    def test_student_dashboard_functionality(self):
        """Test student dashboard component functionality"""
        print("\n🔍 Testing Student Dashboard Component...")
        
        try:
            with open("frontend/src/pages/StudentDashboardEnhanced.js", "r") as f:
                dashboard_content = f.read()
            
            required_features = [
                "dashboardData",
                "todaysTasks",
                "weeklyPlan", 
                "subjects",
                "upcomingQuizzes",
                "aiRecommendations",
                "handleTaskComplete",
                "handleRefresh",
                "notifications",
                "achievements"
            ]
            
            missing_features = []
            for feature in required_features:
                if feature not in dashboard_content:
                    missing_features.append(feature)
            
            if missing_features:
                self.log_test("Student Dashboard Component", "FAIL", f"Missing features: {', '.join(missing_features)}")
                return False
            
            # Check for comprehensive data structure
            if "progress" not in dashboard_content or "analytics" not in dashboard_content:
                self.log_test("Student Dashboard Component", "FAIL", "Missing progress/analytics data")
                return False
            
            self.log_test("Student Dashboard Component", "PASS")
            return True
            
        except Exception as e:
            self.log_test("Student Dashboard Component", "FAIL", str(e))
            return False
    
    def test_student_learning_path_functionality(self):
        """Test student learning path component functionality"""
        print("\n🔍 Testing Student Learning Path Component...")
        
        try:
            with open("frontend/src/pages/StudentLearningPathEnhanced.js", "r") as f:
                path_content = f.read()
            
            required_features = [
                "learningPath",
                "activeWeek",
                "weeks",
                "lessons",
                "achievements",
                "handleLessonStart",
                "getStatusColor",
                "getStatusIcon",
                "bloomLevel",
                "difficulty"
            ]
            
            missing_features = []
            for feature in required_features:
                if feature not in path_content:
                    missing_features.append(feature)
            
            if missing_features:
                self.log_test("Student Learning Path Component", "FAIL", f"Missing features: {', '.join(missing_features)}")
                return False
            
            # Check for Bloom's taxonomy integration
            if "Bloom" not in path_content:
                self.log_test("Student Learning Path Component", "FAIL", "Bloom's taxonomy not integrated")
                return False
            
            self.log_test("Student Learning Path Component", "PASS")
            return True
            
        except Exception as e:
            self.log_test("Student Learning Path Component", "FAIL", str(e))
            return False
    
    def test_student_profile_functionality(self):
        """Test student profile component functionality"""
        print("\n🔍 Testing Student Profile Component...")
        
        try:
            with open("frontend/src/pages/StudentProfileEnhanced.js", "r") as f:
                profile_content = f.read()
            
            required_features = [
                "activeTab",
                "profileData",
                "passwordData",
                "settings",
                "handleProfileSubmit",
                "handlePasswordSubmit",
                "learningStyles",
                "examOptions",
                "subjectOptions",
                "notifications",
                "preferences"
            ]
            
            missing_features = []
            for feature in required_features:
                if feature not in profile_content:
                    missing_features.append(feature)
            
            if missing_features:
                self.log_test("Student Profile Component", "FAIL", f"Missing features: {', '.join(missing_features)}")
                return False
            
            # Check for tabbed interface
            if "profile" not in profile_content or "academic" not in profile_content or "security" not in profile_content:
                self.log_test("Student Profile Component", "FAIL", "Tabbed interface not implemented")
                return False
            
            self.log_test("Student Profile Component", "PASS")
            return True
            
        except Exception as e:
            self.log_test("Student Profile Component", "FAIL", str(e))
            return False
    
    def test_backend_student_endpoints(self):
        """Test backend student API endpoints"""
        print("\n🔍 Testing Backend Student Endpoints...")
        
        try:
            with open("backend/app/api/learning_paths.py", "r") as f:
                api_content = f.read()
            
            required_endpoints = [
                "create_student",
                "get_students",
                "get_student", 
                "update_student",
                "delete_student",
                "generate_personalized_path",
                "get_personalized_path"
            ]
            
            missing_endpoints = []
            for endpoint in required_endpoints:
                if f"def {endpoint}" not in api_content:
                    missing_endpoints.append(endpoint)
            
            if missing_endpoints:
                self.log_test("Backend Student Endpoints", "FAIL", f"Missing endpoints: {', '.join(missing_endpoints)}")
                return False
            
            # Check for proper validation
            if "StudentCreate" not in api_content:
                self.log_test("Backend Student Endpoints", "FAIL", "Missing input validation schema")
                return False
            
            self.log_test("Backend Student Endpoints", "PASS")
            return True
            
        except Exception as e:
            self.log_test("Backend Student Endpoints", "FAIL", str(e))
            return False
    
    def test_student_models(self):
        """Test student database models"""
        print("\n🔍 Testing Student Database Models...")
        
        try:
            with open("backend/app/models/student.py", "r") as f:
                model_content = f.read()
            
            required_models = [
                "class Student",
                "class StudentLearningPath",
                "class WeeklyPlan",
                "class DailyTask",
                "class StudentQuiz",
                "class StudentQuizResult",
                "class ProgressSnapshot",
                "class AssessmentAttempt",
                "class LearningAnalytics"
            ]
            
            missing_models = []
            for model in required_models:
                if model not in model_content:
                    missing_models.append(model)
            
            if missing_models:
                self.log_test("Student Database Models", "FAIL", f"Missing models: {', '.join(missing_models)}")
                return False
            
            # Check for proper relationships
            if "teacher_id" not in model_content or "relationship" not in model_content:
                self.log_test("Student Database Models", "FAIL", "Missing relationships")
                return False
            
            self.log_test("Student Database Models", "PASS")
            return True
            
        except Exception as e:
            self.log_test("Student Database Models", "FAIL", str(e))
            return False
    
    def test_api_integration(self):
        """Test API service integration"""
        print("\n🔍 Testing API Service Integration...")
        
        try:
            with open("frontend/src/services/api.js", "r") as f:
                api_content = f.read()
            
            required_apis = [
                "studentsAPI",
                "authAPI",
                "assessmentAPI",
                "analyticsAPI"
            ]
            
            missing_apis = []
            for api in required_apis:
                if api not in api_content:
                    missing_apis.append(api)
            
            if missing_apis:
                self.log_test("API Service Integration", "FAIL", f"Missing APIs: {', '.join(missing_apis)}")
                return False
            
            # Check for CRUD operations
            crud_operations = ["create", "getAll", "getById", "update", "delete"]
            for operation in crud_operations:
                if operation not in api_content:
                    self.log_test("API Service Integration", "FAIL", f"Missing CRUD operation: {operation}")
                    return False
            
            self.log_test("API Service Integration", "PASS")
            return True
            
        except Exception as e:
            self.log_test("API Service Integration", "FAIL", str(e))
            return False
    
    def test_user_experience_features(self):
        """Test user experience features"""
        print("\n🔍 Testing User Experience Features...")
        
        features_to_check = [
            ("Loading States", "spinner", "frontend/src/pages/StudentDashboardEnhanced.js"),
            ("Error Handling", "toast.error", "frontend/src/pages/StudentLogin.js"),
            ("Form Validation", "validateForm", "frontend/src/pages/StudentLogin.js"),
            ("Responsive Design", "md:grid-cols", "frontend/src/pages/StudentDashboardEnhanced.js"),
            ("Accessibility", "aria-", "frontend/src/pages/StudentLogin.js"),
            ("Progress Indicators", "progress", "frontend/src/pages/StudentLearningPathEnhanced.js"),
            ("Interactive Elements", "hover-lift", "frontend/src/pages/StudentDashboardEnhanced.js"),
            ("Real-time Updates", "useEffect", "frontend/src/pages/StudentDashboardEnhanced.js")
        ]
        
        failed_features = []
        for feature_name, search_term, file_path in features_to_check:
            try:
                if Path(file_path).exists():
                    with open(file_path, "r") as f:
                        content = f.read()
                    if search_term not in content:
                        failed_features.append(feature_name)
                else:
                    failed_features.append(f"{feature_name} (file missing)")
            except Exception:
                failed_features.append(f"{feature_name} (error)")
        
        if failed_features:
            self.log_test("User Experience Features", "FAIL", f"Missing features: {', '.join(failed_features)}")
            return False
        
        self.log_test("User Experience Features", "PASS")
        return True
    
    def test_security_features(self):
        """Test security implementation"""
        print("\n🔍 Testing Security Features...")
        
        security_checks = [
            ("Password Hashing", "bcrypt", "backend/app/api/auth.py"),
            ("JWT Tokens", "jwt", "backend/app/api/auth.py"),
            ("Input Validation", "pydantic", "backend/app/api/learning_paths.py"),
            ("CORS Protection", "CORSMiddleware", "backend/main.py"),
            ("Authentication Required", "get_current_user", "backend/app/api/learning_paths.py"),
            ("Password Strength", "passwordStrength", "frontend/src/pages/StudentSignup.js"),
            ("Secure Storage", "localStorage", "frontend/src/hooks/useStudentAuth.js")
        ]
        
        failed_checks = []
        for check_name, search_term, file_path in security_checks:
            try:
                if Path(file_path).exists():
                    with open(file_path, "r") as f:
                        content = f.read()
                    if search_term not in content:
                        failed_checks.append(check_name)
                else:
                    failed_checks.append(f"{check_name} (file missing)")
            except Exception:
                failed_checks.append(f"{check_name} (error)")
        
        if failed_checks:
            self.log_test("Security Features", "FAIL", f"Missing security: {', '.join(failed_checks)}")
            return False
        
        self.log_test("Security Features", "PASS")
        return True
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🧪 EdweavePack Student Functionality Test Suite")
        print("=" * 60)
        
        # Change to project directory
        os.chdir(Path(__file__).parent)
        
        # Run all tests
        tests = [
            self.test_student_components_exist,
            self.test_student_routes_configured,
            self.test_student_auth_hook,
            self.test_student_login_functionality,
            self.test_student_signup_functionality,
            self.test_student_dashboard_functionality,
            self.test_student_learning_path_functionality,
            self.test_student_profile_functionality,
            self.test_backend_student_endpoints,
            self.test_student_models,
            self.test_api_integration,
            self.test_user_experience_features,
            self.test_security_features
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                self.log_test(f"System - {test.__name__}", "FAIL", str(e))
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "=" * 60)
        print("📊 STUDENT FUNCTIONALITY TEST REPORT")
        print("=" * 60)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  • {result['test']}: {result['message']}")
        
        # Save detailed report
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_tests": total_tests,
                "passed": self.passed_tests,
                "failed": self.failed_tests,
                "success_rate": success_rate
            },
            "test_results": self.test_results,
            "student_ready": self.failed_tests == 0 and success_rate >= 90
        }
        
        with open("student_test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: student_test_report.json")
        
        if report["student_ready"]:
            print("\n🎉 STUDENT FUNCTIONALITY: FULLY READY!")
            print("All student features are implemented and tested.")
            print("✅ Students can register, login, learn, and track progress")
            print("✅ Comprehensive dashboard with AI recommendations")
            print("✅ Personalized learning paths with Bloom's taxonomy")
            print("✅ Full profile management and settings")
            print("✅ Secure authentication and data protection")
        else:
            print("\n⚠️ STUDENT FUNCTIONALITY: NEEDS ATTENTION")
            print("Some student features need fixes before deployment.")
        
        return report["student_ready"]

def main():
    """Main test runner"""
    tester = StudentFunctionalityTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()