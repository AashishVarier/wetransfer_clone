"""
Delete file handler - Deletes file from S3 and metadata from DynamoDB
Triggered by SQS queue after file expiration timer or by user request
"""

import json

# TODO: Import from src.services when implemented
# from src.services.s3_service import delete_file_from_s3
# from src.services.dynamo_service import delete_file_metadata
# from src.utils.logger import log_debug


def lambda_handler(event, context):
    """
    Lambda handler for file deletion
    Can be triggered in two ways:
    1. Direct API call (user initiates deletion)
    2. SQS queue (scheduled deletion after 2 minutes)
    
    Expected event (API):
    {
        "pathParameters": {
            "fileId": "file_xxxxx"
        },
        "headers": {
            "Authorization": "Bearer <token>"
        }
    }
    
    Expected event (SQS):
    {
        "Records": [
            {
                "body": {
                    "userId": "...",
                    "fileId": "..."
                }
            }
        ]
    }
    
    Returns:
    {
        "statusCode": 200 or 204,
        "body": {
            "message": "File deleted successfully"
        }
    }
    
    TODO: Detect if called from API or SQS
    TODO: For API calls: validate authentication and authorization
    TODO: For SQS calls: parse message and skip auth
    TODO: Delete file from S3 bucket
    TODO: Delete metadata from DynamoDB
    TODO: Handle errors gracefully (idempotency)
    TODO: Add proper logging
    """
    
    try:
        # Check if this is an SQS event or API event
        if 'Records' in event:
            # SQS event - handle scheduled deletion
            return handle_sqs_deletion(event)
        else:
            # API event - handle user-initiated deletion
            return handle_api_deletion(event)
        
    except Exception as e:
        print(f'Error in delete_file handler: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }


def handle_api_deletion(event):
    """
    Handle user-initiated file deletion via API
    
    TODO: Extract and validate user ID from auth token
    TODO: Extract fileId from path parameters
    TODO: Verify user owns the file
    TODO: Delete from S3 and DynamoDB
    """
    
    try:
        # TODO: Extract user ID from Authorization header
        # user_id = validate_auth_token(event.get('headers', {}).get('Authorization'))
        
        # TODO: Extract file ID from path parameters
        # path_params = event.get('pathParameters', {}) or {}
        # file_id = path_params.get('fileId')
        
        # TODO: Delete from S3
        # delete_file_from_s3(user_id, file_id)
        
        # TODO: Delete metadata from DynamoDB
        # delete_file_metadata(user_id, file_id)
        
        return {
            'statusCode': 204,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': ''
        }
        
    except Exception as e:
        print(f'Error in handle_api_deletion: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to delete file'})
        }


def handle_sqs_deletion(event):
    """
    Handle scheduled file deletion via SQS
    Called automatically after 2-minute expiration
    
    TODO: Process SQS records
    TODO: Extract userId and fileId from message
    TODO: Delete from S3 and DynamoDB
    TODO: Handle partial failures
    """
    
    deleted_count = 0
    errors = []
    
    for record in event.get('Records', []):
        try:
            # Parse SQS message
            message = json.loads(record.get('body', '{}'))
            user_id = message.get('userId')
            file_id = message.get('fileId')
            
            if not user_id or not file_id:
                errors.append(f'Invalid message format: {record}')
                continue
            
            # TODO: Delete from S3
            # delete_file_from_s3(user_id, file_id)
            
            # TODO: Delete metadata from DynamoDB
            # delete_file_metadata(user_id, file_id)
            
            deleted_count += 1
            print(f'Deleted file {file_id} for user {user_id}')
            
        except json.JSONDecodeError as e:
            errors.append(f'Failed to parse message: {str(e)}')
        except Exception as e:
            errors.append(f'Error deleting file: {str(e)}')
    
    if errors:
        print(f'SQS deletion completed with {len(errors)} errors: {errors}')
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'deletedCount': deleted_count,
            'errors': errors
        })
    }
