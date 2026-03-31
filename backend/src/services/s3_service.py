"""
S3 Service - Handles S3 bucket operations
Manages file uploads, downloads, deletions, and presigned URLs
"""

import os
import boto3
from botocore.exceptions import ClientError

# TODO: Implement S3 service with proper error handling
# Initialize S3 client
s3_client = boto3.client('s3')
BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'wetransfer-clone-files-dev')


def get_presigned_upload_url(user_id: str, file_id: str, file_size: int, expires_in: int = 300) -> str:
    """
    Generate a presigned URL for file upload
    
    Args:
        user_id: User ID
        file_id: File ID
        file_size: File size in bytes (used for validation)
        expires_in: URL expiration time in seconds
    
    Returns:
        Presigned upload URL
    
    TODO: Implement presigned URL generation
    TODO: Add Content-Type and Content-Length validation
    TODO: Add S3 metadata tags
    TODO: Handle S3 errors gracefully
    """
    try:
        # TODO: Validate file_size against 2 MB limit at S3 level
        # TODO: Generate presigned URL with conditions
        # TODO: Add metadata headers
        
        s3_key = f"uploads/{user_id}/{file_id}"
        
        # This is a placeholder - implement actual presigned URL generation
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': s3_key,
                'ContentType': 'application/octet-stream'
            },
            ExpiresIn=expires_in
        )
        
        return presigned_url
        
    except ClientError as e:
        print(f'S3 error generating upload URL: {str(e)}')
        raise


def get_presigned_download_url(user_id: str, file_id: str, expires_in: int = 300) -> str:
    """
    Generate a presigned URL for file download
    
    Args:
        user_id: User ID
        file_id: File ID
        expires_in: URL expiration time in seconds
    
    Returns:
        Presigned download URL
    
    TODO: Implement presigned URL generation
    TODO: Add proper error handling
    """
    try:
        s3_key = f"uploads/{user_id}/{file_id}"
        
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': s3_key
            },
            ExpiresIn=expires_in
        )
        
        return presigned_url
        
    except ClientError as e:
        print(f'S3 error generating download URL: {str(e)}')
        raise


def delete_file_from_s3(user_id: str, file_id: str) -> bool:
    """
    Delete a file from S3
    
    Args:
        user_id: User ID
        file_id: File ID
    
    Returns:
        True if deletion successful
    
    TODO: Implement file deletion
    TODO: Add error handling and logging
    TODO: Handle file not found gracefully (idempotency)
    """
    try:
        s3_key = f"uploads/{user_id}/{file_id}"
        
        s3_client.delete_object(
            Bucket=BUCKET_NAME,
            Key=s3_key
        )
        
        print(f'Deleted S3 object: {s3_key}')
        return True
        
    except ClientError as e:
        print(f'S3 error deleting file: {str(e)}')
        # Return True anyway for idempotency
        return True


def get_file_metadata_from_s3(user_id: str, file_id: str):
    """
    Get file metadata from S3 (size, last modified, etc.)
    
    Args:
        user_id: User ID
        file_id: File ID
    
    Returns:
        Metadata dictionary or None if file not found
    
    TODO: Implement metadata retrieval
    TODO: Add error handling
    """
    try:
        s3_key = f"uploads/{user_id}/{file_id}"
        
        response = s3_client.head_object(
            Bucket=BUCKET_NAME,
            Key=s3_key
        )
        
        return {
            'size': response.get('ContentLength'),
            'lastModified': response.get('LastModified'),
            'contentType': response.get('ContentType')
        }
        
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return None
        print(f'S3 error getting metadata: {str(e)}')
        raise


def check_s3_bucket_exists() -> bool:
    """
    Check if S3 bucket exists and is accessible
    
    Returns:
        True if bucket exists and is accessible
    
    TODO: Implement bucket validation
    """
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
        return True
    except ClientError:
        return False
