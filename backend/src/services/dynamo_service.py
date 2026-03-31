"""
DynamoDB Service - Handles DynamoDB table operations
Manages file metadata, user data, and rate limiting counters
"""

import os
import json
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError

# TODO: Implement DynamoDB service with proper error handling
# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
METADATA_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME', 'wetransfer-clone-metadata-dev')


def get_table(table_name: str = None):
    """Get DynamoDB table resource"""
    table_name = table_name or METADATA_TABLE_NAME
    return dynamodb.Table(table_name)


def save_file_metadata(user_id: str, file_id: str, file_name: str, file_size: int, created_at: str, expires_at: str) -> bool:
    """
    Save file metadata to DynamoDB
    
    Args:
        user_id: User ID (partition key)
        file_id: File ID (sort key)
        file_name: Original file name
        file_size: File size in bytes
        created_at: ISO timestamp
        expires_at: ISO timestamp for expiration
    
    Returns:
        True if successful
    
    TODO: Implement metadata storage
    TODO: Add TTL attribute
    TODO: Handle conflicts
    """
    try:
        table = get_table()
        
        item = {
            'userId': user_id,
            'fileId': file_id,
            'fileName': file_name,
            'fileSize': file_size,
            'createdAt': created_at,
            'expiresAt': expires_at,
            'ttl': int((datetime.fromisoformat(expires_at)).timestamp())
        }
        
        table.put_item(Item=item)
        print(f'Saved metadata for file {file_id} user {user_id}')
        return True
        
    except ClientError as e:
        print(f'DynamoDB error saving metadata: {str(e)}')
        raise


def get_file_metadata(user_id: str, file_id: str):
    """
    Get file metadata from DynamoDB
    
    Args:
        user_id: User ID
        file_id: File ID
    
    Returns:
        Metadata dictionary or None if not found
    
    TODO: Implement metadata retrieval
    TODO: Handle expired files
    """
    try:
        table = get_table()
        
        response = table.get_item(
            Key={
                'userId': user_id,
                'fileId': file_id
            }
        )
        
        return response.get('Item')
        
    except ClientError as e:
        print(f'DynamoDB error getting metadata: {str(e)}')
        raise


def list_user_files(user_id: str, limit: int = 10, next_token: str = None):
    """
    List all files for a user
    
    Args:
        user_id: User ID
        limit: Maximum number of items to return
        next_token: Pagination token
    
    Returns:
        Tuple of (files list, next_token)
    
    TODO: Implement file listing
    TODO: Handle pagination properly
    TODO: Filter expired files
    """
    try:
        table = get_table()
        
        query_params = {
            'KeyConditionExpression': 'userId = :userId',
            'ExpressionAttributeValues': {
                ':userId': user_id
            },
            'Limit': limit
        }
        
        if next_token:
            query_params['ExclusiveStartKey'] = json.loads(next_token)
        
        response = table.query(**query_params)
        
        items = response.get('Items', [])
        last_evaluated_key = response.get('LastEvaluatedKey')
        next_token_out = json.dumps(last_evaluated_key) if last_evaluated_key else None
        
        return items, next_token_out
        
    except ClientError as e:
        print(f'DynamoDB error listing files: {str(e)}')
        raise


def delete_file_metadata(user_id: str, file_id: str) -> bool:
    """
    Delete file metadata from DynamoDB
    
    Args:
        user_id: User ID
        file_id: File ID
    
    Returns:
        True if successful
    
    TODO: Implement metadata deletion
    TODO: Handle not found gracefully
    """
    try:
        table = get_table()
        
        table.delete_item(
            Key={
                'userId': user_id,
                'fileId': file_id
            }
        )
        
        print(f'Deleted metadata for file {file_id} user {user_id}')
        return True
        
    except ClientError as e:
        print(f'DynamoDB error deleting metadata: {str(e)}')
        # Return True for idempotency
        return True


def get_rate_limit_counter(user_id: str, table_name: str = None) -> int:
    """
    Get rate limit counter for user
    
    Args:
        user_id: User ID
        table_name: Optional table name for rate limit counters
    
    Returns:
        Current counter value
    
    TODO: Implement counter retrieval
    """
    try:
        # Use a separate table for rate limits if configured
        table = dynamodb.Table(table_name or f'{METADATA_TABLE_NAME}-rateLimits')
        
        response = table.get_item(
            Key={'userId': user_id}
        )
        
        item = response.get('Item', {})
        return item.get('counter', 0)
        
    except ClientError as e:
        print(f'DynamoDB error getting rate limit: {str(e)}')
        return 0


def increment_rate_counter(user_id: str, window_seconds: int = 900, table_name: str = None):
    """
    Increment rate limit counter atomically
    
    Args:
        user_id: User ID
        window_seconds: TTL window in seconds (default 15 minutes)
        table_name: Optional table name
    
    Returns:
        Reset timestamp
    
    TODO: Implement atomic increment
    TODO: Handle TTL properly
    """
    try:
        table = dynamodb.Table(table_name or f'{METADATA_TABLE_NAME}-rateLimits')
        
        reset_time = int(datetime.utcnow().timestamp()) + window_seconds
        
        response = table.update_item(
            Key={'userId': user_id},
            UpdateExpression='SET #counter = if_not_exists(#counter, :zero) + :one, #ttl = :ttl',
            ExpressionAttributeNames={
                '#counter': 'counter',
                '#ttl': 'ttl'
            },
            ExpressionAttributeValues={
                ':zero': 0,
                ':one': 1,
                ':ttl': reset_time
            },
            ReturnValues='ALL_NEW'
        )
        
        return reset_time
        
    except ClientError as e:
        print(f'DynamoDB error incrementing rate limit: {str(e)}')
        raise


def check_table_exists(table_name: str = None) -> bool:
    """
    Check if DynamoDB table exists
    
    Args:
        table_name: Table name
    
    Returns:
        True if table exists
    
    TODO: Implement table existence check
    """
    try:
        table_name = table_name or METADATA_TABLE_NAME
        table = dynamodb.Table(table_name)
        table.load()
        return True
    except ClientError:
        return False
