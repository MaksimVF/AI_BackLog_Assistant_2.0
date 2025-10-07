





"""
S3 Client for AI Backlog Assistant

This module provides S3 file storage functionality.
"""

import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from src.config import Config
import logging

config = Config()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3Client:
    """S3 client for file storage operations"""

    def __init__(self):
        """Initialize the S3 client"""
        self.s3 = boto3.client(
            's3',
            endpoint_url=config.S3_ENDPOINT,
            aws_access_key_id=config.S3_ACCESS_KEY,
            aws_secret_access_key=config.S3_SECRET_KEY
        )
        self.bucket_name = config.S3_BUCKET

    def upload_file(self, file_path: str, s3_key: str) -> bool:
        """Upload a file to S3"""
        try:
            self.s3.upload_file(file_path, self.bucket_name, s3_key)
            logger.info(f"File uploaded to S3: {s3_key}")
            return True
        except (NoCredentialsError, ClientError) as e:
            logger.error(f"Error uploading file to S3: {e}")
            return False

    def download_file(self, s3_key: str, download_path: str) -> bool:
        """Download a file from S3"""
        try:
            self.s3.download_file(self.bucket_name, s3_key, download_path)
            logger.info(f"File downloaded from S3: {s3_key}")
            return True
        except (NoCredentialsError, ClientError) as e:
            logger.error(f"Error downloading file from S3: {e}")
            return False

    def get_file_url(self, s3_key: str) -> str:
        """Get a file URL from S3"""
        return f"{config.S3_ENDPOINT}/{self.bucket_name}/{s3_key}"

    def list_files(self, prefix: str = "") -> list:
        """List files in S3 with optional prefix"""
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified']
                    })
            return files
        except (NoCredentialsError, ClientError) as e:
            logger.error(f"Error listing files from S3: {e}")
            return []

# Create a global S3 client instance
s3_client = S3Client()



