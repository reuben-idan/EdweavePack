"""
Enhanced security configuration for EdweavePack
Implements enterprise-grade security standards
"""

import os
import json
import boto3
from typing import Optional
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

class SecureConfig:
    """Secure configuration management using AWS Secrets Manager"""
    
    def __init__(self):
        self.is_production = os.getenv("ENVIRONMENT", "development") == "production"
        self.region = os.getenv("AWS_REGION", "eu-north-1")
        self._secrets_cache = {}
        
        if self.is_production:
            self.secrets_client = boto3.client('secretsmanager', region_name=self.region)
    
    def get_secret(self, secret_name: str) -> Optional[dict]:
        """Retrieve and cache secret from AWS Secrets Manager"""
        if not self.is_production:
            return self._get_local_secret(secret_name)
        
        if secret_name in self._secrets_cache:
            return self._secrets_cache[secret_name]
        
        try:
            response = self.secrets_client.get_secret_value(SecretId=secret_name)
            secret_data = json.loads(response['SecretString'])
            self._secrets_cache[secret_name] = secret_data
            return secret_data
        except ClientError as e:
            logger.error(f"Failed to retrieve secret {secret_name}: {e}")
            return None
    
    def _get_local_secret(self, secret_name: str) -> dict:
        """Get local development secrets"""
        local_secrets = {
            'edweavepack/database': {
                'url': os.getenv('DATABASE_URL', 'postgresql://edweave:edweave123@postgres:5432/edweave')
            },
            'edweavepack/jwt': {
                'secret_key': os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
            },
            'edweavepack/redis': {
                'url': os.getenv('REDIS_URL', 'redis://redis:6379/0')
            }
        }
        return local_secrets.get(secret_name, {})
    
    @property
    def database_url(self) -> str:
        """Get secure database URL"""
        secret = self.get_secret('edweavepack/database')
        return secret.get('url', '') if secret else ''
    
    @property
    def jwt_secret_key(self) -> str:
        """Get secure JWT secret key"""
        secret = self.get_secret('edweavepack/jwt')
        return secret.get('secret_key', '') if secret else ''
    
    @property
    def redis_url(self) -> str:
        """Get secure Redis URL"""
        secret = self.get_secret('edweavepack/redis')
        return secret.get('url', '') if secret else ''

# Global secure config instance
secure_config = SecureConfig()

# Security headers middleware
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
}

def get_security_headers() -> dict:
    """Get security headers for production"""
    if secure_config.is_production:
        return SECURITY_HEADERS
    return {}

# Input validation and sanitization
def sanitize_input(data: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not isinstance(data, str):
        return str(data)
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`']
    for char in dangerous_chars:
        data = data.replace(char, '')
    
    return data.strip()

def validate_password_strength(password: str) -> bool:
    """Validate password meets security requirements"""
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
    
    return has_upper and has_lower and has_digit and has_special