import os
import boto3
import logging
from typing import Optional, Dict
from botocore.exceptions import ClientError, NoCredentialsError

logger = logging.getLogger(__name__)

class CredentialManager:
    """Secure AWS credential management for Amazon Q Developer integration"""
    
    @staticmethod
    def get_aws_credentials() -> Optional[Dict[str, str]]:
        """Get AWS credentials from various sources"""
        
        # Try environment variables first
        access_key = os.getenv('AWS_ACCESS_KEY_ID')
        secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        region = os.getenv('AWS_REGION', 'us-east-1')
        
        if access_key and secret_key:
            logger.info("Using AWS credentials from environment variables")
            return {
                'aws_access_key_id': access_key,
                'aws_secret_access_key': secret_key,
                'region_name': region
            }
        
        # Try AWS credentials file
        try:
            session = boto3.Session()
            credentials = session.get_credentials()
            if credentials:
                logger.info("Using AWS credentials from credentials file")
                return {
                    'aws_access_key_id': credentials.access_key,
                    'aws_secret_access_key': credentials.secret_key,
                    'region_name': region
                }
        except Exception as e:
            logger.debug(f"Could not load credentials from file: {e}")
        
        # Try IAM role (for EC2/ECS)
        try:
            session = boto3.Session()
            credentials = session.get_credentials()
            if credentials and credentials.access_key:
                logger.info("Using AWS credentials from IAM role")
                return {
                    'aws_access_key_id': credentials.access_key,
                    'aws_secret_access_key': credentials.secret_key,
                    'region_name': region
                }
        except Exception as e:
            logger.debug(f"Could not load credentials from IAM role: {e}")
        
        logger.warning("No AWS credentials found")
        return None
    
    @staticmethod
    def test_credentials() -> bool:
        """Test if AWS credentials are valid"""
        try:
            creds = CredentialManager.get_aws_credentials()
            if not creds:
                return False
            
            # Test with STS get-caller-identity
            sts_client = boto3.client('sts', **creds)
            sts_client.get_caller_identity()
            logger.info("AWS credentials validated successfully")
            return True
            
        except (ClientError, NoCredentialsError) as e:
            logger.warning(f"AWS credential validation failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during credential validation: {e}")
            return False
    
    @staticmethod
    def get_bedrock_client():
        """Get configured Bedrock client"""
        creds = CredentialManager.get_aws_credentials()
        if not creds:
            raise Exception("No AWS credentials available for Bedrock")
        
        try:
            return boto3.client('bedrock-runtime', **creds)
        except Exception as e:
            logger.error(f"Failed to create Bedrock client: {e}")
            raise
    
    @staticmethod
    def get_s3_client():
        """Get configured S3 client"""
        creds = CredentialManager.get_aws_credentials()
        if not creds:
            raise Exception("No AWS credentials available for S3")
        
        try:
            return boto3.client('s3', **creds)
        except Exception as e:
            logger.error(f"Failed to create S3 client: {e}")
            raise