#!/usr/bin/env python3
"""
Test JWKS endpoint connectivity with sample Cognito configuration
"""

import requests

def test_sample_jwks():
    """Test JWKS endpoint with a sample configuration"""
    # Sample JWKS URL format
    sample_region = "us-east-1"
    sample_pool_id = "us-east-1_EXAMPLE123"
    jwks_url = f"https://cognito-idp.{sample_region}.amazonaws.com/{sample_pool_id}/.well-known/jwks.json"
    
    print("Testing JWKS endpoint format...")
    print(f"Sample URL: {jwks_url}")
    
    try:
        response = requests.get(jwks_url, timeout=5)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 404:
            print("Expected 404 - User Pool doesn't exist (this is normal for test)")
            return True
        elif response.status_code == 200:
            print("JWKS endpoint accessible")
            return True
        else:
            print(f"Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

if __name__ == "__main__":
    test_sample_jwks()