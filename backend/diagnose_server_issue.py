#!/usr/bin/env python3

import requests
import subprocess
import time
import json

def diagnose_server_issue():
    """Diagnose the main server issue and provide fix"""
    print("=== Diagnosing Main Server Issue ===")
    
    # 1. Check if multiple servers are running
    try:
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        port_8000_lines = [line for line in result.stdout.split('\n') if ':8000' in line and 'LISTENING' in line]
        port_8002_lines = [line for line in result.stdout.split('\n') if ':8002' in line and 'LISTENING' in line]
        
        print(f"Port 8000 processes: {len(port_8000_lines)}")
        print(f"Port 8002 processes: {len(port_8002_lines)}")
        
        if len(port_8000_lines) > 1:
            print("WARNING: Multiple processes on port 8000 detected")
            
    except Exception as e:
        print(f"Could not check processes: {e}")
    
    # 2. Test current server response
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        print(f"Main server responding: {response.status_code}")
    except Exception as e:
        print(f"Main server not responding: {e}")
        return False
    
    # 3. Test registration endpoint with unique data
    test_data = {
        "email": f"diagnostic_{int(time.time())}@example.com",
        "full_name": "Diagnostic User",
        "password": "testpassword123",
        "institution": "Test Institution",
        "role": "teacher"
    }
    
    try:
        response = requests.post('http://localhost:8000/api/auth/register', json=test_data, timeout=10)
        print(f"Registration status: {response.status_code}")
        print(f"Registration response: {response.json()}")
        
        if "UPDATED_CODE" in str(response.json()):
            print("✓ Updated code is running")
            return True
        else:
            print("✗ Old code still running")
            return False
            
    except Exception as e:
        print(f"Registration test failed: {e}")
        return False

if __name__ == "__main__":
    diagnose_server_issue()