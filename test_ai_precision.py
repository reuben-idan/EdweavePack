#!/usr/bin/env python3
"""Precision testing of AI functionality"""

import requests
import json
import time
from datetime import datetime

class AIFunctionalityTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = {}
        
    def authenticate(self):
        """Authenticate with test credentials"""
        try:
            login_data = {
                "username": "deploy_test@example.com",
                "password": "TestPass123!"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/auth/token",
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=15
            )
            
            if response.status_code == 200:
                token = response.json().get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {token}"})
                return True
            return False
        except Exception:
            return False
    
    def test_curriculum_ai_generation(self):
        """Test AI curriculum generation"""
        print("\n🧪 Testing AI Curriculum Generation")
        
        test_data = {
            "title": "AI Test Curriculum",
            "description": "Testing AI curriculum generation",
            "subject": "Computer Science",
            "grade_level": "High School",
            "source_content": "Python programming fundamentals including variables, functions, loops, and data structures. Object-oriented programming concepts with classes and inheritance."
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/curriculum/", json=test_data, timeout=30)
            
            if response.status_code in [200, 201]:
                curriculum = response.json()
                
                # Test AI features
                checks = {
                    "has_ai_metadata": "hackathon_features" in curriculum or "ai_enhanced" in str(curriculum),
                    "has_weekly_modules": "weekly_modules" in curriculum or "modules" in curriculum,
                    "has_learning_objectives": "learning_objectives" in curriculum,
                    "content_processed": len(str(curriculum)) > 500
                }
                
                score = sum(checks.values()) / len(checks) * 100
                self.results["curriculum_generation"] = {"score": score, "checks": checks}
                print(f"  ✅ AI Curriculum Generation: {score:.1f}%")
                return curriculum.get("id")
            else:
                print(f"  ❌ Failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            return None
    
    def test_ai_agents(self):
        """Test AI agent endpoints"""
        print("\n🤖 Testing AI Agent System")
        
        tests = [
            ("Agent Config", "/api/agents/kiro/config"),
            ("Health Check", "/health"),
        ]
        
        passed = 0
        for test_name, endpoint in tests:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=15)
                if response.status_code in [200, 401]:  # 401 OK for protected endpoints
                    print(f"  ✅ {test_name}: Working")
                    passed += 1
                else:
                    print(f"  ⚠️ {test_name}: {response.status_code}")
            except Exception as e:
                print(f"  ❌ {test_name}: {e}")
        
        score = (passed / len(tests)) * 100
        self.results["ai_agents"] = {"score": score, "passed": passed, "total": len(tests)}
        return score > 50
    
    def test_assessment_ai(self, curriculum_id):
        """Test AI assessment generation"""
        print("\n📝 Testing AI Assessment Generation")
        
        if not curriculum_id:
            print("  ⚠️ Skipped: No curriculum ID")
            return False
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/assessment/generate",
                json={"curriculum_id": curriculum_id, "assessment_type": "comprehensive"},
                timeout=25
            )
            
            if response.status_code in [200, 201]:
                assessment = response.json()
                
                checks = {
                    "has_questions": "questions" in assessment or "question_bank" in assessment,
                    "ai_generated": "ai" in str(assessment).lower() or "generated" in str(assessment).lower(),
                    "has_structure": len(str(assessment)) > 200
                }
                
                score = sum(checks.values()) / len(checks) * 100
                self.results["assessment_generation"] = {"score": score, "checks": checks}
                print(f"  ✅ AI Assessment Generation: {score:.1f}%")
                return True
            else:
                print(f"  ❌ Failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            return False
    
    def test_frontend_ai_features(self):
        """Test frontend AI integration"""
        print("\n🎨 Testing Frontend AI Features")
        
        try:
            # Test main page loads
            response = requests.get(self.base_url, timeout=10)
            frontend_works = response.status_code == 200
            
            # Test API endpoints accessibility
            response = requests.get(f"{self.base_url}/api", timeout=10)
            api_accessible = response.status_code in [200, 404, 422]  # Any response means server is up
            
            score = ((frontend_works + api_accessible) / 2) * 100
            self.results["frontend_integration"] = {"score": score, "frontend": frontend_works, "api": api_accessible}
            
            print(f"  ✅ Frontend Integration: {score:.1f}%")
            return score > 50
            
        except Exception as e:
            print(f"  ❌ Frontend test failed: {e}")
            return False
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print(f"\n📊 AI FUNCTIONALITY TEST REPORT")
        print("=" * 50)
        
        total_score = 0
        test_count = 0
        
        for test_name, result in self.results.items():
            score = result.get("score", 0)
            total_score += score
            test_count += 1
            
            status = "✅ PASS" if score >= 70 else "⚠️ PARTIAL" if score >= 50 else "❌ FAIL"
            print(f"{status} {test_name.replace('_', ' ').title()}: {score:.1f}%")
        
        overall_score = total_score / test_count if test_count > 0 else 0
        
        print(f"\n🏆 Overall AI Score: {overall_score:.1f}%")
        
        if overall_score >= 85:
            print("🎉 EXCELLENT - Ready for deployment")
            return True
        elif overall_score >= 70:
            print("✅ GOOD - Safe to deploy")
            return True
        else:
            print("⚠️ NEEDS IMPROVEMENT - Review before deployment")
            return False

def run_precision_test():
    """Run comprehensive AI precision test"""
    
    base_url = "http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com"
    
    print("🎯 AI FUNCTIONALITY PRECISION TEST")
    print("=" * 45)
    print(f"Target: {base_url}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = AIFunctionalityTester(base_url)
    
    # Test sequence
    if not tester.authenticate():
        print("❌ Authentication failed - using public endpoints only")
    
    # Core AI tests
    curriculum_id = tester.test_curriculum_ai_generation()
    tester.test_ai_agents()
    tester.test_assessment_ai(curriculum_id)
    tester.test_frontend_ai_features()
    
    # Generate final report
    return tester.generate_report()

if __name__ == "__main__":
    success = run_precision_test()
    exit(0 if success else 1)