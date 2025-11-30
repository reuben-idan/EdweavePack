import boto3
import logging
from typing import Optional
from botocore.exceptions import ClientError
from .credential_manager import CredentialManager

logger = logging.getLogger(__name__)

class S3Service:
    """AWS S3 service for file storage and management"""
    
    def __init__(self, bucket_name: Optional[str] = None):
        self.bucket_name = bucket_name or "edweavepack-storage"
        try:
            self.s3_client = CredentialManager.get_s3_client()
            self.available = True
            logger.info("S3 service initialized successfully")
        except Exception as e:
            logger.warning(f"S3 service unavailable: {e}")
            self.s3_client = None
            self.available = False
    
    def upload_file(self, file_content: bytes, file_key: str, content_type: str = "application/octet-stream") -> Optional[str]:
        """Upload file to S3 bucket"""
        if not self.available:
            logger.warning("S3 service not available")
            return None
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_key,
                Body=file_content,
                ContentType=content_type
            )
            
            # Generate URL
            url = f"https://{self.bucket_name}.s3.amazonaws.com/{file_key}"
            logger.info(f"File uploaded successfully: {file_key}")
            return url
            
        except ClientError as e:
            logger.error(f"S3 upload failed: {e}")
            return None
    
    def download_file(self, file_key: str) -> Optional[bytes]:
        """Download file from S3 bucket"""
        if not self.available:
            return None
        
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
            return response['Body'].read()
        except ClientError as e:
            logger.error(f"S3 download failed: {e}")
            return None
    
    def delete_file(self, file_key: str) -> bool:
        """Delete file from S3 bucket"""
        if not self.available:
            return False
        
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_key)
            logger.info(f"File deleted successfully: {file_key}")
            return True
        except ClientError as e:
            logger.error(f"S3 delete failed: {e}")
            return False
    
    def list_files(self, prefix: str = "") -> list:
        """List files in S3 bucket"""
        if not self.available:
            return []
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'].isoformat()
                    })
            
            return files
            
        except ClientError as e:
            logger.error(f"S3 list failed: {e}")
            return []
    
    def generate_presigned_url(self, file_key: str, expiration: int = 3600) -> Optional[str]:
        """Generate presigned URL for file access"""
        if not self.available:
            return None
        
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': file_key},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logger.error(f"Presigned URL generation failed: {e}")
            return None