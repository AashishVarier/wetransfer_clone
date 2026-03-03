"""
S3 service for file storage operations
"""
import os
import boto3
from botocore.exceptions import ClientError


s3_client = boto3.client('s3')
BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'wetransfer-clone-files-dev')


def upload_file(user_id, file_id, file_content):
    """
    Upload a file to S3
    
    TODO: Implement file upload with proper error handling
    TODO: Add metadata/tags to S3 object
    TODO: Validate file size (2MB limit)
    TODO: Return S3 object URL
    
    Args:
        user_id: User ID
        file_id: Unique file identifier
        file_content: File content (bytes)
    
    Returns:
        dict with s3_key and url
    """
    
    print(f'upload_file called: user_id={user_id}, file_id={file_id}')
    
    # TODO: Implement actual S3 upload
    # s3_key = f'{user_id}/{file_id}'
    # s3_client.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=file_content)
    
    return {
        's3_key': f'{user_id}/{file_id}',
        'url': f'https://{BUCKET_NAME}.s3.amazonaws.com/{user_id}/{file_id}'
    }


def download_file(user_id, file_id):
    """
    Download a file from S3
    
    TODO: Implement file download
    TODO: Add access validation
    TODO: Generate presigned URL for direct download
    
    Args:
        user_id: User ID
        file_id: File ID
    
    Returns:
        File content (bytes) or presigned URL
    """
    
    print(f'download_file called: user_id={user_id}, file_id={file_id}')
    
    # TODO: Implement actual S3 download
    # s3_key = f'{user_id}/{file_id}'
    # response = s3_client.get_object(Bucket=BUCKET_NAME, Key=s3_key)
    # return response['Body'].read()
    
    return b'File content'


def delete_file(user_id, file_id):
    """
    Delete a file from S3
    
    TODO: Implement file deletion
    TODO: Add access validation
    
    Args:
        user_id: User ID
        file_id: File ID
    
    Returns:
        bool: True if successful
    """
    
    print(f'delete_file called: user_id={user_id}, file_id={file_id}')
    
    # TODO: Implement actual S3 deletion
    # s3_key = f'{user_id}/{file_id}'
    # s3_client.delete_object(Bucket=BUCKET_NAME, Key=s3_key)
    
    return True


def get_presigned_url(user_id, file_id, expiration=3600):
    """
    Generate a presigned URL for file download
    
    TODO: Implement presigned URL generation
    
    Args:
        user_id: User ID
        file_id: File ID
        expiration: URL expiration in seconds (default 1 hour)
    
    Returns:
        str: Presigned URL
    """
    
    print(f'get_presigned_url called: user_id={user_id}, file_id={file_id}')
    
    # TODO: Implement presigned URL generation
    # s3_key = f'{user_id}/{file_id}'
    # url = s3_client.generate_presigned_url(
    #     'get_object',
    #     Params={'Bucket': BUCKET_NAME, 'Key': s3_key},
    #     ExpiresIn=expiration
    # )
    
    return f'https://{BUCKET_NAME}.s3.amazonaws.com/presigned-url'
