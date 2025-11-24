#!/usr/bin/env python3

import subprocess
import time
import requests
import os
import signal

def kill_port_processes(port):
    """Kill all processes on a specific port"""
    try:
        # Get processes using the port
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        pids = []
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if parts:
                    pid = parts[-1]
                    if pid.isdigit():
                        pids.append(int(pid))
        
        print(f"Found {len(pids)} processes on port {port}: {pids}")
        
        # Kill each process
        for pid in pids:
            try:
                subprocess.run(['taskkill', '/F', '/PID', str(pid)], 
                             capture_output=True, check=False)
                print(f"Killed process {pid}")
            except Exception as e:
                print(f"Could not kill process {pid}: {e}")
        
        return len(pids) > 0
        
    except Exception as e:
        print(f"Error killing processes: {e}")
        return False

def wait_for_port_free(port, timeout=10):
    """Wait for port to be free"""
    for i in range(timeout):
        try:
            requests.get(f'http://localhost:{port}/', timeout=1)
            time.sleep(1)
        except:
            print(f"Port {port} is now free")
            return True
    return False

def robust_server_fix():
    """Robust fix for the server issue"""
    print("=== Robust Server Fix ===")
    
    # 1. Kill all processes on port 8000
    print("Step 1: Killing all processes on port 8000...")
    killed = kill_port_processes(8000)
    
    if killed:
        print("Step 2: Waiting for port to be free...")
        wait_for_port_free(8000)
    
    # 2. Clean Python cache
    print("Step 3: Cleaning Python cache...")
    try:
        for root, dirs, files in os.walk('.'):
            if '__pycache__' in dirs:
                cache_dir = os.path.join(root, '__pycache__')
                subprocess.run(['rmdir', '/S', '/Q', cache_dir], 
                             shell=True, capture_output=True)
                print(f"Cleaned {cache_dir}")
    except Exception as e:
        print(f"Cache cleaning error: {e}")
    
    print("\n=== Fix Complete ===")
    print("Now restart the server with:")
    print("python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    
    return True

if __name__ == "__main__":
    robust_server_fix()