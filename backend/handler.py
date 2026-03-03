"""
Main Lambda handler for WeTransfer Clone API
"""
import json
import os
from urllib.parse import parse_qs
from services.s3_service import upload_file, download_file, delete_file
from services.metadata_service import save_metadata, get_metadata, list_user_files


def lambda_handler(event, context):
    """
    Main Lambda handler for all API requests
    
    TODO: Implement proper routing
    TODO: Add authentication validation
    TODO: Add error handling
    """
    
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    
    # Parse request body
    body = None
    if event.get('body'):
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            body = {}
    
    # TODO: Extract and validate authentication token
    # user_id = validate_auth_token(event.get('headers', {}).get('Authorization'))
    
    # Simple routing
    if path == '/upload' and http_method == 'POST':
        return handle_upload(body)
    
    elif path == '/files' and http_method == 'GET':
        return handle_list_files()
    
    elif path.startswith('/files/') and http_method == 'GET':
        file_id = path.split('/')[-1]
        return handle_download(file_id)
    
    elif path.startswith('/files/') and http_method == 'DELETE':
        file_id = path.split('/')[-1]
        return handle_delete(file_id)
    
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Route not found'})
        }


def handle_upload(body):
    """
    Handle file upload
    
    TODO: Validate request format
    TODO: Validate file size (2MB limit)
    TODO: Call S3 service to upload
    TODO: Save metadata to DynamoDB
    """
    
    print('handle_upload called with body:', body)
    
    if not body:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Request body required'})
        }
    
    # TODO: Validate required fields (userId, filename, etc.)
    # TODO: Implement actual upload logic
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Upload endpoint ready',
            'fileId': 'file_' + str(int(__import__('time').time()))
        })
    }


def handle_list_files():
    """
    Handle listing user files
    
    TODO: Get user ID from authentication
    TODO: Call metadata service
    """
    
    print('handle_list_files called')
    
    # TODO: Implement actual listing
    # TODO: Add pagination
    # TODO: Filter expired files
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'files': [],
            'message': 'Files list endpoint ready'
        })
    }


def handle_download(file_id):
    """
    Handle file download
    
    TODO: Validate file exists
    TODO: Check user has access
    TODO: Generate presigned S3 URL
    """
    
    print(f'handle_download called with file_id: {file_id}')
    
    # TODO: Implement download logic
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Download endpoint ready',
            'fileId': file_id
        })
    }


def handle_delete(file_id):
    """
    Handle file deletion
    
    TODO: Validate user owns file
    TODO: Delete from S3
    TODO: Delete metadata from DynamoDB
    """
    
    print(f'handle_delete called with file_id: {file_id}')
    
    # TODO: Implement deletion logic
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'File deleted',
            'fileId': file_id
        })
    }
