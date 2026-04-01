"""
Test list files handler
"""

import json
import pytest
from src.handlers import list_files


def test_list_files_handler(aws_credentials, env_vars):
    """Test list files handler"""
    event = {
        'headers': {
            'Authorization': 'Bearer test-token'
        },
        'queryStringParameters': {
            'limit': '10'
        }
    }
    
    response = list_files.lambda_handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'files' in body
    assert isinstance(body['files'], list)
