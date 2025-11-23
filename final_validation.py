#!/usr/bin/env python3
"""
Final validation script for EdweavePack deployment readiness
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if Path(file_path).exists():
        print(f"SUCCESS: {description}")
        return True
    else:
        print(f"MISSING: {description} - {file_path}")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists"""
    if Path(dir_path).exists() and Path(dir_path).is_dir():
        print(f"SUCCESS: {description}")
        return True
    else:
        print(f"MISSING: {description} - {dir_path}")
        return False

def run_command(cmd, cwd=None, description=""):
    """Run a command and check if it succeeds"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"SUCCESS: {description}")
            return True
        else:
            print(f"FAILED: {description} - {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT: {description}")
        return False
    except Exception as e:
        print(f"ERROR: {description} - {e}")
        return False

def main():
    """Run final validation checks"""
    print("EdweavePack Final Validation")
    print("=" * 50)
    
    os.chdir(Path(__file__).parent)
    
    checks = []
    
    # File structure validation
    print("\n1. File Structure Validation")
    print("-" * 30)
    checks.append(check_file_exists("backend/main.py", "Backend main application"))
    checks.append(check_file_exists("backend/requirements.txt", "Backend dependencies"))
    checks.append(check_file_exists("frontend/package.json", "Frontend dependencies"))
    checks.append(check_file_exists("frontend/src/App.js", "Frontend main component"))
    checks.append(check_file_exists("docker-compose.yml", "Docker compose configuration"))
    checks.append(check_directory_exists("backend/app/api", "Backend API directory"))
    checks.append(check_directory_exists("backend/app/models", "Backend models directory"))
    checks.append(check_directory_exists("frontend/src/pages", "Frontend pages directory"))
    
    # Backend validation
    print("\n2. Backend Validation")
    print("-" * 30)
    checks.append(run_command("python basic_test.py", cwd="backend", description="Backend functionality test"))
    
    # Frontend validation
    print("\n3. Frontend Validation")
    print("-" * 30)
    checks.append(run_command("npm run build", cwd="frontend", description="Frontend build test"))
    
    # Docker validation
    print("\n4. Docker Configuration")
    print("-" * 30)
    checks.append(check_file_exists("backend/Dockerfile", "Backend Dockerfile"))
    checks.append(check_file_exists("frontend/Dockerfile", "Frontend Dockerfile"))
    
    # Test files validation
    print("\n5. Test Suite Validation")
    print("-" * 30)
    checks.append(check_directory_exists("backend/tests", "Backend tests directory"))
    checks.append(check_file_exists("backend/tests/conftest.py", "Test configuration"))
    checks.append(check_file_exists("backend/tests/test_auth.py", "Authentication tests"))
    checks.append(check_file_exists("backend/tests/test_curriculum.py", "Curriculum tests"))
    
    # Documentation validation
    print("\n6. Documentation Validation")
    print("-" * 30)
    checks.append(check_file_exists("README.md", "Main documentation"))
    checks.append(check_file_exists("DEPLOYMENT_SUMMARY.md", "Deployment guide"))
    
    # Calculate results
    passed = sum(checks)
    total = len(checks)
    success_rate = (passed / total) * 100
    
    print("\n" + "=" * 50)
    print("FINAL VALIDATION RESULTS")
    print("=" * 50)
    print(f"Passed: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("\nSTATUS: READY FOR DEPLOYMENT!")
        print("All critical components are in place and functional.")
        print("\nNext steps:")
        print("1. Configure production environment variables")
        print("2. Set up production database")
        print("3. Deploy using: docker-compose up -d")
        print("4. Access application at http://localhost:3000")
        return True
    elif success_rate >= 75:
        print("\nSTATUS: MOSTLY READY - Minor issues detected")
        print("Address the failed checks above before deployment.")
        return False
    else:
        print("\nSTATUS: NOT READY - Critical issues detected")
        print("Fix the failed checks before attempting deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)