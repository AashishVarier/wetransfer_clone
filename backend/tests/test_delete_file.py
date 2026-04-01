"""
Test delete file handler
"""

import json
import pytest
from src.handlers import delete_file


def test_delete_file_handler_api_deletion(aws_credentials, env_vars):
    """Test delete file handler for API deletion"""
    event = {
        'pathParameters': {
            'fileId': 'file_test_123'
        },
        'headers': {
            'Authorization': 'Bearer test-token'
        }
    }
    
    response = delete_file.lambda_handler(event, None)
    
    # Should return 204 No Content or 200
    assert response['statusCode'] in [200, 204]


def test_delete_file_handler_sqs_deletion(aws_credentials, env_vars):
    """Test delete file handler for SQS deletion"""
    event = {
        'Records': [
            {
                'body': json.dumps({
                    'userId': 'user_placeholder',
                    'fileId': 'file_test_123'
                })
            }
        ]
    }
    
    response = delete_file.lambda_handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'deletedCount' in body
