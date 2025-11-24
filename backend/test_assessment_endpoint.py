#!/usr/bin/env python3

import requests
import json

def test_assessment_endpoint():
    """Test the assessment endpoint directly"""
    print("=== Testing Assessment Endpoint ===")
    
    # Test without auth
    try:
        response = requests.post('http://localhost:8000/api/assessment/2/submit', 
                               json={"answers": {}}, timeout=10)
        print(f"No auth - Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"No auth error: {e}")
    
    # Test with mock token
    try:
        headers = {"Authorization": "Bearer fake-token"}
        response = requests.post('http://localhost:8000/api/assessment/2/submit',
                               json={"answers": {}}, headers=headers, timeout=10)
        print(f"With fake token - Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Fake token error: {e}")

if __name__ == "__main__":
    test_assessment_endpoint()