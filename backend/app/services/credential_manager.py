import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging

logger = logging.getLogger(__name__)

class CredentialManager:
    """Manages AWS credentials with multiple fallback methods"""
    
    @staticmethod
    def get_aws_credentials():
        """Get AWS credentials from multiple sources"""
        
        # Method 1: Environment variables
        if all([os.getenv('AWS_ACCESS_KEY_ID'), os.getenv('AWS_SECRET_ACCESS_KEY')]):
            return {
                'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
                'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
                'region_name': os.getenv('AWS_REGION', 'us-east-1')
            }
        
        # Method 2: AWS CLI credentials
        try:
            session = boto3.Session()
            credentials = session.get_credentials()
            if credentials:
                return {
                    'aws_access_key_id': credentials.access_key,
                    'aws_secret_access_key': credentials.secret_key,
                    'aws_session_token': credentials.token,
                    'region_name': os.getenv('AWS_REGION', 'us-east-1')
                }
        except Exception:
            pass
        
        # Method 3: IAM Role (for EC2/ECS)
        try:
            session = boto3.Session()
            session.client('sts').get_caller_identity()
            return {'region_name': os.getenv('AWS_REGION', 'us-east-1')}
        except Exception:
            pass
        
        return None
    
    @staticmethod
    def test_credentials():
        """Test if AWS credentials work"""
        try:
            creds = CredentialManager.get_aws_credentials()
            if not creds:
                return False
            
            client = boto3.client('bedrock-runtime', **creds)
            # Simple test call
            client.list_foundation_models()
            return True
        except Exception as e:
            logger.warning(f"AWS credentials test failed: {e}")
            return False