#!/usr/bin/env python3
"""
Comprehensive test runner for EdweavePack
Tests backend API, frontend components, and integration
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=check
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"Error: {result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return e

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    backend_dir = Path("backend")
    if backend_dir.exists():
        result = run_command("pip install -r requirements.txt", cwd=backend_dir, check=False)
        if result.returncode != 0:
            print("❌ Failed to install Python dependencies")
            return False
    
    # Check Node dependencies
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        result = run_command("npm install", cwd=frontend_dir, check=False)
        if result.returncode != 0:
            print("❌ Failed to install Node dependencies")
            return False
    
    print("✅ Dependencies checked")
    return True

def run_backend_tests():
    """Run backend API tests"""
    print("\n🧪 Running Backend Tests...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Run pytest with coverage
    result = run_command(
        "python -m pytest tests/ -v --tb=short --cov=app --cov-report=term-missing",
        cwd=backend_dir,
        check=False
    )
    
    if result.returncode == 0:
        print("✅ Backend tests passed")
        return True
    else:
        print("❌ Backend tests failed")
        return False

def run_frontend_tests():
    """Run frontend component tests"""
    print("\n🧪 Running Frontend Tests...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Run React tests
    result = run_command(
        "npm test -- --coverage --watchAll=false",
        cwd=frontend_dir,
        check=False
    )
    
    if result.returncode == 0:
        print("✅ Frontend tests passed")
        return True
    else:
        print("❌ Frontend tests failed")
        return False

def run_integration_tests():
    """Run integration tests with Docker"""
    print("\n🧪 Running Integration Tests...")
    
    # Start services
    print("Starting Docker services...")
    result = run_command("docker-compose up -d postgres redis", check=False)
    
    if result.returncode != 0:
        print("❌ Failed to start Docker services")
        return False
    
    # Wait for services to be ready
    print("Waiting for services to be ready...")
    time.sleep(10)
    
    # Run integration tests
    result = run_command(
        "python -m pytest tests/ -v -k integration",
        cwd=Path("backend"),
        check=False
    )
    
    # Cleanup
    run_command("docker-compose down", check=False)
    
    if result.returncode == 0:
        print("✅ Integration tests passed")
        return True
    else:
        print("❌ Integration tests failed")
        return False

def lint_code():
    """Run code linting"""
    print("\n🔍 Running Code Linting...")
    
    # Backend linting
    backend_dir = Path("backend")
    if backend_dir.exists():
        print("Linting Python code...")
        run_command("python -m flake8 app/ --max-line-length=100 --ignore=E203,W503", 
                   cwd=backend_dir, check=False)
    
    # Frontend linting
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        print("Linting JavaScript code...")
        run_command("npm run lint", cwd=frontend_dir, check=False)
    
    print("✅ Code linting completed")

def security_scan():
    """Run security scans"""
    print("\n🔒 Running Security Scans...")
    
    # Python security scan
    backend_dir = Path("backend")
    if backend_dir.exists():
        print("Scanning Python dependencies...")
        run_command("pip install safety", check=False)
        run_command("safety check", cwd=backend_dir, check=False)
    
    # Node security scan
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        print("Scanning Node dependencies...")
        run_command("npm audit", cwd=frontend_dir, check=False)
    
    print("✅ Security scans completed")

def main():
    """Main test runner"""
    print("🚀 EdweavePack Test Suite")
    print("=" * 50)
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    results = []
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        sys.exit(1)
    
    # Run tests
    results.append(("Backend Tests", run_backend_tests()))
    results.append(("Frontend Tests", run_frontend_tests()))
    
    # Optional: Integration tests (requires Docker)
    if "--integration" in sys.argv:
        results.append(("Integration Tests", run_integration_tests()))
    
    # Code quality checks
    if "--lint" in sys.argv:
        lint_code()
    
    if "--security" in sys.argv:
        security_scan()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Ready for deployment.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Please fix issues before deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()