#!/usr/bin/env python3

import subprocess
import json

def test_with_curl():
    """Test registration with curl to see raw response"""
    print("=== Testing with curl ===")
    
    data = {
        "email": "testuser2@example.com",
        "full_name": "Test User 2",
        "password": "testpassword123",
        "institution": "Test Institution",
        "role": "teacher"
    }
    
    curl_cmd = [
        "curl", "-X", "POST",
        "http://localhost:8000/api/auth/register",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(data),
        "-v"
    ]
    
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=10)
        print(f"Exit code: {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_with_curl()