#!/usr/bin/env python3

import requests

def test_simple_endpoints():
    """Test simple endpoints to verify server is working"""
    
    # Test root endpoint
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        print(f"Root endpoint - Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Root endpoint error: {e}")
    
    # Test assessment endpoint directly
    try:
        response = requests.get('http://localhost:8000/api/assessment/2', timeout=5)
        print(f"Assessment GET - Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Assessment GET error: {e}")
    
    # Test assessment submit
    try:
        response = requests.post('http://localhost:8000/api/assessment/2/submit',
                               json={"answers": {"1": 0}}, timeout=5)
        print(f"Assessment POST - Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Assessment POST error: {e}")

if __name__ == "__main__":
    test_simple_endpoints()