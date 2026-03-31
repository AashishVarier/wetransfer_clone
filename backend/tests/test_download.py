"""
Test download handler
"""

import json
import pytest
from src.handlers import download


def test_download_handler_missing_file_id(aws_credentials, env_vars):
    """Test download handler with missing file ID"""
    event = {
        'pathParameters': None,
        'headers': {
            'Authorization': 'Bearer test-token'
        }
    }
    
    response = download.lambda_handler(event, None)
    
    assert response['statusCode'] == 400
