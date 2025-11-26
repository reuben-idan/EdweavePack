#!/usr/bin/env python3
"""Deploy AI updates to live environment"""

import subprocess
import sys
import time
import requests
import json

def deploy_updates():
    """Deploy enhanced AI implementation"""
    
    print("Deploying Enhanced AI Implementation")
    print("=" * 50)
    
    # 1. Commit changes
    try:
        subprocess.run(["git", "add", "."], check=True, cwd=".")
        subprocess.run(["git", "commit", "-m", "Enhanced AI implementation with Amazon Q integration"], check=True, cwd=".")
        subprocess.run(["git", "push", "origin", "main"], check=True, cwd=".")
        print("Code pushed to repository")
    except subprocess.CalledProcessError as e:
        print(f"Git operations: {e}")
    
    # 2. Trigger deployment
    try:
        subprocess.run(["python", "auto_deploy.py"], check=True, cwd=".")
        print("Deployment triggered")
    except subprocess.CalledProcessError:
        print("Using alternative deployment")
        subprocess.run(["deploy-aws.bat"], shell=True, cwd=".")
    
    # 3. Wait for deployment
    print("Waiting for deployment...")
    time.sleep(60)
    
    return True

def test_deployment():
    """Test deployment with expert precision"""
    
    base_url = "http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com"
    
    tests = [
        ("Health Check", f"{base_url}/health"),
        ("API Root", f"{base_url}/api"),
        ("Auth Endpoint", f"{base_url}/api/auth"),
    ]
    
    print("\nTesting Deployment")
    print("=" * 30)
    
    for test_name, url in tests:
        try:
            response = requests.get(url, timeout=10)
            status = "PASS" if response.status_code < 400 else "FAIL"
            print(f"{status} {test_name}: {response.status_code}")
        except Exception as e:
            print(f"FAIL {test_name}: {e}")

def test_ai_functionality():
    """Test AI functionality with precision"""
    
    base_url = "http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com"
    
    # Test user registration and login
    test_user = {
        "email": "ai_test@example.com",
        "password": "TestPass123!",
        "full_name": "AI Test User",
        "role": "teacher"
    }
    
    print("\nTesting AI Functionality")
    print("=" * 35)
    
    session = requests.Session()
    
    # 1. Register test user
    try:
        response = session.post(f"{base_url}/api/auth/register", json=test_user, timeout=15)
        if response.status_code in [200, 201, 400]:  # 400 if user exists
            print("User registration: PASS")
        else:
            print(f"User registration: {response.status_code}")
            return False
    except Exception as e:
        print(f"User registration: {e}")
        return False
    
    # 2. Login
    try:
        login_data = {"username": test_user["email"], "password": test_user["password"]}
        response = session.post(f"{base_url}/api/auth/token", 
                               data=login_data, 
                               headers={"Content-Type": "application/x-www-form-urlencoded"},
                               timeout=15)
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            session.headers.update({"Authorization": f"Bearer {token}"})
            print("User login: PASS")
        else:
            print(f"User login: {response.status_code}")
            return False
    except Exception as e:
        print(f"User login: {e}")
        return False
    
    # 3. Test curriculum generation
    try:
        curriculum_data = {
            "content": "Python programming fundamentals including variables, functions, loops, and data structures. Object-oriented programming concepts with classes and inheritance.",
            "subject": "Computer Science",
            "grade_level": "High School",
            "learning_objectives": ["Understand Python syntax", "Apply programming concepts", "Create original programs"]
        }
        
        response = session.post(f"{base_url}/api/curriculum/", json=curriculum_data, timeout=30)
        
        if response.status_code in [200, 201]:
            curriculum = response.json()
            if "weekly_modules" in curriculum and len(curriculum["weekly_modules"]) >= 4:
                print("AI Curriculum Generation: PASS")
                curriculum_id = curriculum.get("id")
            else:
                print("AI Curriculum Generation: Invalid structure")
                return False
        else:
            print(f"AI Curriculum Generation: {response.status_code}")
            return False
    except Exception as e:
        print(f"AI Curriculum Generation: {e}")
        return False
    
    # 4. Test assessment generation
    try:
        if curriculum_id:
            response = session.post(f"{base_url}/api/assessment/generate", 
                                   json={"curriculum_id": curriculum_id, "assessment_type": "comprehensive"},
                                   timeout=25)
            
            if response.status_code in [200, 201]:
                assessment = response.json()
                if "questions" in assessment or "question_bank" in assessment:
                    print("AI Assessment Generation: PASS")
                else:
                    print("AI Assessment Generation: No questions generated")
            else:
                print(f"AI Assessment Generation: {response.status_code}")
        else:
            print("AI Assessment Generation: Skipped (no curriculum ID)")
    except Exception as e:
        print(f"AI Assessment Generation: {e}")
    
    # 5. Test agent endpoints
    try:
        response = session.get(f"{base_url}/api/agents/kiro/config", timeout=15)
        if response.status_code == 200:
            config = response.json()
            if "agents_available" in config:
                print("Agent Orchestration: PASS")
            else:
                print("Agent Orchestration: Invalid config")
        else:
            print(f"Agent Orchestration: {response.status_code}")
    except Exception as e:
        print(f"Agent Orchestration: {e}")
    
    return True

def test_user_flow():
    """Test complete user flow"""
    
    print("\nTesting Complete User Flow")
    print("=" * 35)
    
    base_url = "http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com"
    
    # Test frontend accessibility
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200 and "EdweavePack" in response.text:
            print("Frontend Loading: PASS")
        else:
            print(f"Frontend Loading: {response.status_code}")
    except Exception as e:
        print(f"Frontend Loading: {e}")
    
    # Test API documentation
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("API Documentation: PASS")
        else:
            print(f"API Documentation: {response.status_code}")
    except Exception as e:
        print(f"API Documentation: {e}")

if __name__ == "__main__":
    print("EdweavePack Enhanced AI Deployment & Testing")
    print("=" * 55)
    
    # Deploy updates
    if deploy_updates():
        # Wait for services to stabilize
        print("\nAllowing services to stabilize...")
        time.sleep(30)
        
        # Run comprehensive tests
        test_deployment()
        test_ai_functionality()
        test_user_flow()
        
        print("\nDeployment and Testing Complete!")
        print(f"Live Application: http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com")
        print("Test with: ai_test@example.com / TestPass123!")
    else:
        print("Deployment failed")
        sys.exit(1)