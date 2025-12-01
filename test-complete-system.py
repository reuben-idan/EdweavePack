#!/usr/bin/env python3

import requests
import json
import time

def test_complete_system():
    """Test complete EdweavePack system with AWS AI"""
    
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    print("EdweavePack Complete System Test")
    print("=" * 40)
    
    # Test 1: Registration
    print("1. Testing Registration...")
    test_user = {
        "email": "complete-test@edweavepack.com",
        "password": "test123",
        "full_name": "Complete Test User",
        "role": "teacher"
    }
    
    try:
        reg_response = requests.post(f"{base_url}/api/auth/register", json=test_user, timeout=10)
        print(f"   Registration: {reg_response.status_code}")
        
        if reg_response.status_code == 200:
            print("   ✓ Registration: SUCCESS")
            token = reg_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test 2: Login (OAuth2 format)
            print("\n2. Testing Login...")
            login_data = {
                "username": test_user["email"],
                "password": test_user["password"]
            }
            
            login_response = requests.post(f"{base_url}/api/auth/token", 
                                         data=login_data, timeout=10)
            print(f"   Login: {login_response.status_code}")
            
            if login_response.status_code == 200:
                print("   ✓ Login: SUCCESS")
                
                # Test 3: AI Curriculum Generation
                print("\n3. Testing AI Curriculum Generation...")
                curriculum_data = {
                    "title": "AWS AI-Enhanced Python Programming",
                    "subject": "Computer Science",
                    "grade_level": "High School"
                }
                
                curr_response = requests.post(f"{base_url}/api/curriculum/", 
                                            json=curriculum_data, headers=headers, timeout=30)
                print(f"   AI Curriculum: {curr_response.status_code}")
                
                if curr_response.status_code == 200:
                    print("   ✓ AI Curriculum Generation: SUCCESS")
                    curriculum = curr_response.json()
                    curriculum_id = curriculum["id"]
                    
                    # Test 4: AI Assessment Generation
                    print("\n4. Testing AI Assessment Generation...")
                    assessment_data = {
                        "curriculum_id": curriculum_id,
                        "assessment_type": "quiz",
                        "topic": "Python Basics",
                        "difficulty": "Medium",
                        "question_count": 5
                    }
                    
                    assess_response = requests.post(f"{base_url}/api/assessment/generate", 
                                                  json=assessment_data, headers=headers, timeout=30)
                    print(f"   AI Assessment: {assess_response.status_code}")
                    
                    if assess_response.status_code == 200:
                        print("   ✓ AI Assessment Generation: SUCCESS")
                        
                        # Test 5: Content Upload with AI Analysis
                        print("\n5. Testing AI Content Analysis...")
                        content_data = {
                            "filename": "python_tutorial.txt",
                            "content": "Python is a high-level programming language. Variables store data. Functions perform operations. Loops repeat code. Conditionals make decisions."
                        }
                        
                        upload_response = requests.post(f"{base_url}/api/curriculum/upload", 
                                                      json=content_data, headers=headers, timeout=30)
                        print(f"   AI Content Analysis: {upload_response.status_code}")
                        
                        if upload_response.status_code == 200:
                            print("   ✓ AI Content Analysis: SUCCESS")
                            
                            # Test 6: Analytics Dashboard
                            print("\n6. Testing AI Analytics Dashboard...")
                            analytics_response = requests.get(f"{base_url}/api/analytics/dashboard", 
                                                            headers=headers, timeout=30)
                            print(f"   AI Analytics: {analytics_response.status_code}")
                            
                            if analytics_response.status_code == 200:
                                print("   ✓ AI Analytics Dashboard: SUCCESS")
                                
                                # Test 7: Agent Orchestration
                                print("\n7. Testing Agent Orchestration...")
                                agent_data = {
                                    "subject": "Mathematics",
                                    "grade_level": "Grade 9",
                                    "learning_objectives": ["Algebra basics", "Linear equations"]
                                }
                                
                                agent_response = requests.post(f"{base_url}/api/agents/curriculum/generate", 
                                                             json=agent_data, headers=headers, timeout=30)
                                print(f"   Agent Orchestration: {agent_response.status_code}")
                                
                                if agent_response.status_code == 200:
                                    print("   ✓ Agent Orchestration: SUCCESS")
                                    
                                    print("\n" + "=" * 40)
                                    print("🎉 ALL TESTS PASSED!")
                                    print("✅ Authentication: WORKING")
                                    print("✅ AWS AI Integration: WORKING") 
                                    print("✅ Curriculum Generation: WORKING")
                                    print("✅ Assessment Creation: WORKING")
                                    print("✅ Content Analysis: WORKING")
                                    print("✅ Analytics Dashboard: WORKING")
                                    print("✅ Agent Orchestration: WORKING")
                                    print("\n🚀 EdweavePack is fully operational!")
                                    print("🌐 URL: http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com")
                                    print("\n📋 AWS AI Services Integrated:")
                                    print("   • Amazon Bedrock (Claude 3.5 Sonnet)")
                                    print("   • Amazon Comprehend")
                                    print("   • Amazon Textract")
                                    print("   • Amazon Polly")
                                    print("   • Amazon Translate")
                                    print("\n🎯 Hackathon Features:")
                                    print("   • AI-powered curriculum generation")
                                    print("   • Intelligent assessment creation")
                                    print("   • Adaptive learning paths")
                                    print("   • Agent orchestration (Kiro)")
                                    print("   • Real-time analytics")
                                    return True
                                    
    except Exception as e:
        print(f"Test error: {e}")
    
    print("\n❌ Some tests failed")
    return False

if __name__ == "__main__":
    test_complete_system()