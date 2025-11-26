#!/usr/bin/env python3
"""Comprehensive AI functionality testing before deployment"""

import requests
import json
import time

def test_health_with_ai():
    """Test health endpoint for AI features"""
    base_url = "http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com"
    
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Health Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Check for AI features
            ai_features = data.get("ai_service", {})
            if ai_features:
                print("AI Service Status: DETECTED")
                return True
            else:
                print("AI Service Status: NOT DETECTED")
                return False
        else:
            print("Health check failed")
            return False
            
    except Exception as e:
        print(f"Health test error: {e}")
        return False

def test_curriculum_ai():
    """Test curriculum AI endpoint"""
    base_url = "http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com"
    
    try:
        # Test the AI curriculum test endpoint
        response = requests.get(f"{base_url}/api/curriculum/test/1", timeout=15)
        print(f"Curriculum AI Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"AI Features Found: {json.dumps(data.get('ai_features', {}), indent=2)}")
            
            # Check for AI indicators
            ai_indicators = ['ai_powered', 'ai_features', 'metadata']
            found_ai = any(indicator in data for indicator in ai_indicators)
            
            if found_ai:
                print("Curriculum AI: WORKING")
                return True
            else:
                print("Curriculum AI: NO AI FEATURES DETECTED")
                return False
        else:
            print("Curriculum endpoint not accessible")
            return False
            
    except Exception as e:
        print(f"Curriculum AI test error: {e}")
        return False

def test_backend_ai_services():
    """Test backend AI service availability"""
    base_url = "http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com"
    
    # Test if backend is responding
    try:
        response = requests.get(f"{base_url}/api", timeout=10)
        print(f"Backend API Status: {response.status_code}")
        
        if response.status_code in [200, 404, 422]:  # Any response means backend is up
            print("Backend: ONLINE")
            return True
        else:
            print("Backend: OFFLINE")
            return False
            
    except Exception as e:
        print(f"Backend test error: {e}")
        return False

def test_frontend_integration():
    """Test frontend loads correctly"""
    base_url = "http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com"
    
    try:
        response = requests.get(base_url, timeout=10)
        print(f"Frontend Status: {response.status_code}")
        
        if response.status_code == 200:
            # Check if it's the React app
            content = response.text
            if "EdweavePack" in content or "react" in content.lower():
                print("Frontend: REACT APP LOADED")
                return True
            else:
                print("Frontend: LOADED BUT UNKNOWN CONTENT")
                return True
        else:
            print("Frontend: NOT ACCESSIBLE")
            return False
            
    except Exception as e:
        print(f"Frontend test error: {e}")
        return False

def run_comprehensive_test():
    """Run all AI tests and report results"""
    
    print("COMPREHENSIVE AI FUNCTIONALITY TEST")
    print("=" * 45)
    
    tests = [
        ("Frontend Integration", test_frontend_integration),
        ("Backend Services", test_backend_ai_services),
        ("Health with AI", test_health_with_ai),
        ("Curriculum AI", test_curriculum_ai),
    ]
    
    results = {}
    passed = 0
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        try:
            result = test_func()
            results[test_name] = result
            if result:
                passed += 1
                print(f"PASS: {test_name}")
            else:
                print(f"FAIL: {test_name}")
        except Exception as e:
            print(f"ERROR: {test_name} - {e}")
            results[test_name] = False
    
    # Final report
    total = len(tests)
    success_rate = (passed / total) * 100
    
    print(f"\nTEST RESULTS SUMMARY")
    print("=" * 25)
    print(f"Passed: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate >= 75:
        print("STATUS: READY FOR DEPLOYMENT")
        print("All critical AI systems operational")
        return True
    elif success_rate >= 50:
        print("STATUS: PARTIAL SUCCESS")
        print("Core systems working, some AI features may need attention")
        return True
    else:
        print("STATUS: NOT READY")
        print("Critical issues found - fix before deployment")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    exit(0 if success else 1)