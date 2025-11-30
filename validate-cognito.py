#!/usr/bin/env python3
"""
Cognito Setup Validation Script
Tests JWKS endpoint connectivity and JWT validation functionality
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

def test_jwks_endpoint():
    """Test JWKS endpoint connectivity"""
    pool_id = os.getenv('COGNITO_POOL_ID')
    region = os.getenv('COGNITO_REGION', 'us-east-1')
    jwks_url = os.getenv('COGNITO_JWKS_URL') or f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json"
    
    print(f"Testing JWKS endpoint: {jwks_url}")
    
    try:
        response = requests.get(jwks_url, timeout=10)
        response.raise_for_status()
        jwks = response.json()
        
        print("JWKS endpoint accessible")
        print(f"Found {len(jwks.get('keys', []))} signing keys")
        
        # Display key information
        for i, key in enumerate(jwks.get('keys', [])[:2]):  # Show first 2 keys
            print(f"   Key {i+1}: {key.get('kid', 'N/A')} ({key.get('alg', 'N/A')})")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"JWKS endpoint failed: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def validate_environment():
    """Validate required environment variables"""
    print("Validating environment configuration...")
    
    required_vars = [
        'COGNITO_POOL_ID',
        'COGNITO_CLIENT_ID',
        'COGNITO_REGION'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"{var}: {value}")
    
    if missing_vars:
        print(f"Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    return True

def test_cognito_validator():
    """Test the Cognito JWT validator class"""
    print("Testing Cognito JWT validator...")
    
    try:
        # Import the validator
        sys.path.append('backend')
        from auth.cognito import CognitoJWTValidator
        
        validator = CognitoJWTValidator()
        print("CognitoJWTValidator initialized successfully")
        
        # Test JWKS connection
        if validator.test_jwks_connection():
            print("JWKS connection test passed")
        else:
            print("JWKS connection test failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"Validator test failed: {e}")
        return False

def main():
    """Main validation function"""
    print("EdweavePack Cognito Validation")
    print("=" * 40)
    
    # Test 1: Environment variables
    if not validate_environment():
        print("\nEnvironment validation failed")
        return False
    
    print()
    
    # Test 2: JWKS endpoint
    if not test_jwks_endpoint():
        print("\nJWKS endpoint test failed")
        return False
    
    print()
    
    # Test 3: Cognito validator
    if not test_cognito_validator():
        print("\nCognito validator test failed")
        return False
    
    print()
    print("All Cognito validation tests passed!")
    print("Ready for JWT token validation")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)