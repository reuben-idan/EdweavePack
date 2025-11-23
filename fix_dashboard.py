#!/usr/bin/env python3
"""
Quick fix for dashboard data loading issue
"""
import requests
import json

def test_dashboard_endpoint():
    """Test if the analytics dashboard endpoint is working"""
    try:
        # Test without auth first
        response = requests.get("http://localhost:8000/api/analytics/dashboard")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 401:
            print("Endpoint exists but requires authentication")
            return True
        elif response.status_code == 200:
            print("Endpoint working")
            return True
        else:
            print(f"Endpoint issue: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("Backend server not running on localhost:8000")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_health_check():
    """Test if backend is running"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("Backend server is running")
            return True
        else:
            print(f"Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("Backend server not running")
        return False

if __name__ == "__main__":
    print("Diagnosing dashboard issue...")
    
    if test_health_check():
        test_dashboard_endpoint()
    else:
        print("\nSolution: Start the backend server")
        print("   cd backend && python -m uvicorn main:app --reload")