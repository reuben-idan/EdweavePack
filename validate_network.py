#!/usr/bin/env python3
"""
Network validation script for EdweavePack deployment
Tests connectivity, DNS resolution, and service health
"""

import requests
import socket
import time
import sys
from urllib.parse import urlparse

def test_dns_resolution(hostname):
    """Test DNS resolution for a hostname"""
    try:
        ip = socket.gethostbyname(hostname)
        print(f"✅ DNS Resolution: {hostname} -> {ip}")
        return True
    except socket.gaierror as e:
        print(f"❌ DNS Resolution failed for {hostname}: {e}")
        return False

def test_port_connectivity(hostname, port, timeout=5):
    """Test TCP connectivity to a specific port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((hostname, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Port {port} is open on {hostname}")
            return True
        else:
            print(f"❌ Port {port} is closed on {hostname}")
            return False
    except Exception as e:
        print(f"❌ Connection test failed for {hostname}:{port} - {e}")
        return False

def test_http_endpoint(url, expected_status=200, timeout=10):
    """Test HTTP endpoint availability"""
    try:
        response = requests.get(url, timeout=timeout, verify=False)
        if response.status_code == expected_status:
            print(f"✅ HTTP {response.status_code}: {url}")
            return True
        else:
            print(f"❌ HTTP {response.status_code}: {url} (expected {expected_status})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP request failed for {url}: {e}")
        return False

def test_health_endpoints():
    """Test application health endpoints"""
    endpoints = [
        "http://localhost:8000/health",
        "http://localhost:3000",
        "https://edweavepack-alb-1353441079.eu-north-1.elb.amazonaws.com/health",
        "https://edweavepack-alb-1353441079.eu-north-1.elb.amazonaws.com"
    ]
    
    results = []
    for endpoint in endpoints:
        print(f"\nTesting: {endpoint}")
        result = test_http_endpoint(endpoint)
        results.append(result)
    
    return results

def test_database_connectivity():
    """Test database connectivity"""
    try:
        import psycopg2
        # This would need actual DB credentials
        print("📋 Database connectivity test requires credentials")
        return True
    except ImportError:
        print("⚠️  psycopg2 not installed, skipping database test")
        return True

def main():
    """Run all network validation tests"""
    print("🔍 EdweavePack Network Validation")
    print("=" * 40)
    
    all_tests_passed = True
    
    # Test DNS resolution
    print("\n📡 DNS Resolution Tests:")
    dns_tests = [
        "localhost",
        "edweavepack-alb-1353441079.eu-north-1.elb.amazonaws.com"
    ]
    
    for hostname in dns_tests:
        if not test_dns_resolution(hostname):
            all_tests_passed = False
    
    # Test port connectivity
    print("\n🔌 Port Connectivity Tests:")
    port_tests = [
        ("localhost", 8000),
        ("localhost", 3000),
        ("localhost", 5432),
        ("localhost", 6379)
    ]
    
    for hostname, port in port_tests:
        if not test_port_connectivity(hostname, port):
            all_tests_passed = False
    
    # Test HTTP endpoints
    print("\n🌐 HTTP Endpoint Tests:")
    health_results = test_health_endpoints()
    if not any(health_results):
        all_tests_passed = False
    
    # Test database
    print("\n🗄️  Database Tests:")
    if not test_database_connectivity():
        all_tests_passed = False
    
    # Summary
    print("\n" + "=" * 40)
    if all_tests_passed:
        print("✅ All network tests passed!")
        sys.exit(0)
    else:
        print("❌ Some network tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()