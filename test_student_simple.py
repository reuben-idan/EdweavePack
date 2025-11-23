#!/usr/bin/env python3
"""
Simple Student Functionality Test
"""

import os
import sys
from pathlib import Path

def test_student_files():
    """Test that student files exist"""
    print("Testing Student Files...")
    
    required_files = [
        "frontend/src/pages/StudentLogin.js",
        "frontend/src/pages/StudentSignup.js", 
        "frontend/src/pages/StudentDashboardEnhanced.js",
        "frontend/src/pages/StudentProfileEnhanced.js",
        "frontend/src/pages/StudentLearningPathEnhanced.js",
        "frontend/src/hooks/useStudentAuth.js"
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
    
    if missing:
        print(f"MISSING FILES: {missing}")
        return False
    
    print("SUCCESS: All student files exist")
    return True

def test_app_routes():
    """Test App.js has student routes"""
    print("Testing App.js Routes...")
    
    try:
        with open("frontend/src/App.js", "r") as f:
            content = f.read()
        
        routes = ["/student/login", "/student/signup", "/student/dashboard"]
        missing = [r for r in routes if r not in content]
        
        if missing:
            print(f"MISSING ROUTES: {missing}")
            return False
        
        if "StudentAuthProvider" not in content:
            print("MISSING: StudentAuthProvider")
            return False
        
        print("SUCCESS: App.js routes configured")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_backend_api():
    """Test backend API exists"""
    print("Testing Backend API...")
    
    try:
        with open("backend/app/api/learning_paths.py", "r") as f:
            content = f.read()
        
        endpoints = ["create_student", "get_students", "update_student"]
        missing = [e for e in endpoints if f"def {e}" not in content]
        
        if missing:
            print(f"MISSING ENDPOINTS: {missing}")
            return False
        
        print("SUCCESS: Backend API configured")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Run tests"""
    print("EdweavePack Student Functionality Test")
    print("=" * 40)
    
    os.chdir(Path(__file__).parent)
    
    tests = [
        test_student_files,
        test_app_routes,
        test_backend_api
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("SUCCESS: Student functionality ready!")
        return True
    else:
        print("FAILED: Some issues need fixing")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)