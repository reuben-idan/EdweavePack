#!/usr/bin/env python3
"""Quick AWS credentials setup for EdweavePack"""

import os
import subprocess
import sys

def setup_aws_credentials():
    """Setup AWS credentials with multiple options"""
    
    print("🔧 EdweavePack AWS Credentials Setup")
    print("=" * 50)
    
    # Check if AWS CLI is installed
    try:
        subprocess.run(["aws", "--version"], capture_output=True, check=True)
        print("✅ AWS CLI detected")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ AWS CLI not found. Install with: pip install awscli")
        return False
    
    # Option 1: Use existing AWS CLI credentials
    try:
        result = subprocess.run(["aws", "sts", "get-caller-identity"], 
                              capture_output=True, text=True, check=True)
        print("✅ Existing AWS credentials found")
        print("🚀 Amazon Q Developer will use these credentials")
        return True
    except subprocess.CalledProcessError:
        pass
    
    # Option 2: Configure new credentials
    print("\n🔑 Configure AWS credentials:")
    print("1. Get credentials from AWS Console > IAM > Users > Security Credentials")
    print("2. Run: aws configure")
    print("3. Enter your Access Key ID and Secret Access Key")
    
    configure = input("\nRun 'aws configure' now? (y/n): ").lower().strip()
    if configure == 'y':
        try:
            subprocess.run(["aws", "configure"], check=True)
            print("✅ AWS credentials configured")
            return True
        except subprocess.CalledProcessError:
            print("❌ Configuration failed")
    
    # Option 3: Environment variables
    print("\n🌍 Alternative: Set environment variables:")
    print("export AWS_ACCESS_KEY_ID=your_access_key")
    print("export AWS_SECRET_ACCESS_KEY=your_secret_key")
    print("export AWS_REGION=us-east-1")
    
    return False

def test_bedrock_access():
    """Test Bedrock access"""
    try:
        import boto3
        client = boto3.client('bedrock-runtime', region_name='us-east-1')
        client.list_foundation_models()
        print("✅ Amazon Bedrock access confirmed")
        return True
    except Exception as e:
        print(f"⚠️  Bedrock access test failed: {e}")
        print("💡 Ensure your AWS account has Bedrock access enabled")
        return False

if __name__ == "__main__":
    success = setup_aws_credentials()
    if success:
        test_bedrock_access()
        print("\n🎉 Setup complete! Amazon Q Developer is ready.")
    else:
        print("\n⚠️  Manual setup required. Enhanced fallback mode will be used.")