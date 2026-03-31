"""
Test rate limit handler
"""

import json
import pytest
from src.handlers import rate_limit


def test_rate_limit_handler_within_limit(aws_credentials, env_vars):
    """Test rate limit handler when within limit"""
    event = {
        'headers': {
            'Authorization': 'Bearer test-token'
        }
    }
    
    response = rate_limit.lambda_handler(event, None)
    
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'allowed' in body
