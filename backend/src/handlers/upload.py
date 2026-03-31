"""
Upload handler - Manages file upload requests
Generates presigned URLs or upload instructions
Enforces 2 MB file size limit
Creates metadata records
Enqueues delayed delete events
"""

import json
import os
import uuid
from datetime import datetime, timedelta

# TODO: Import from src.services when services are implemented
# from src.services.s3_service import get_presigned_upload_url
# from src.services.dynamo_service import save_file_metadata
# from src.services.auth_service import get_user_from_token
# from src.utils.validators import validate_file_size
# from src.utils.response_formatter import format_response


def lambda_handler(event, context):
    """
    Lambda handler for file upload requests
    
    Expected event:
    {
        "headers": {
            "Authorization": "Bearer <token>",
            "Content-Type": "application/json"
        },
        "body": {
            "fileName": "document.pdf",
            "fileSize": 1048576
        }
    }
    
    Returns:
    {
        "statusCode": 200,
        "body": {
            "fileId": "...",
            "presignedUrl": "...",
            "expiresIn": 300
        }
    }
    
    TODO: Implement authentication validation
    TODO: Validate file size (2 MB max)
    TODO: Call S3 service for presigned URL
    TODO: Save metadata to DynamoDB
    TODO: Enqueue SQS message for delayed deletion
    TODO: Add proper error handling and logging
    """
    
    try:
        # Extract and parse request body
        body = json.loads(event.get('body', '{}'))
        file_name = body.get('fileName')
        file_size = body.get('fileSize')
        
        # TODO: Extract user ID from Authorization header and token
        # user_id = validate_auth_token(event.get('headers', {}).get('Authorization'))
        user_id = 'user_placeholder'  # Placeholder
        
        if not file_name or not file_size:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'fileName and fileSize required'})
            }
        
        # TODO: Validate file size (2 MB max)
        max_file_size_bytes = 2 * 1024 * 1024  # 2 MB
        if file_size > max_file_size_bytes:
            return {
                'statusCode': 413,
                'body': json.dumps({'error': f'File size exceeds 2 MB limit'})
            }
        
        # Generate unique file ID
        file_id = f"file_{uuid.uuid4().hex[:8]}_{int(datetime.utcnow().timestamp())}"
        
        # TODO: Call S3 service to generate presigned upload URL
        # presigned_url = get_presigned_upload_url(user_id, file_id, file_size)
        presigned_url = f"https://s3.amazonaws.com/presigned_url_placeholder"
        
        # TODO: Save metadata to DynamoDB
        # save_file_metadata(
        #     user_id=user_id,
        #     file_id=file_id,
        #     file_name=file_name,
        #     file_size=file_size,
        #     created_at=datetime.utcnow().isoformat(),
        #     expires_at=(datetime.utcnow() + timedelta(minutes=2)).isoformat()
        # )
        
        # TODO: Enqueue SQS message for delayed deletion (2 minutes)
        # enqueue_delete_task(user_id, file_id, delay_seconds=120)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'fileId': file_id,
                'presignedUrl': presigned_url,
                'expiresIn': 300,  # URL expires in 5 minutes
                'fileDeleteAt': (datetime.utcnow() + timedelta(minutes=2)).isoformat()
            })
        }
        
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    except Exception as e:
        print(f'Error in upload handler: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
