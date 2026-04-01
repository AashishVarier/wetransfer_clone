"""
Response Formatter - Consistent API response formatting
"""

import json


def format_success_response(data: dict, status_code: int = 200) -> dict:
    """
    Format successful API response
    
    Args:
        data: Response data
        status_code: HTTP status code
    
    Returns:
        Formatted Lambda response
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(data)
    }


def format_error_response(error: str, status_code: int = 400) -> dict:
    """
    Format error API response
    
    Args:
        error: Error message
        status_code: HTTP status code
    
    Returns:
        Formatted Lambda response
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': error})
    }


def format_notfound_response() -> dict:
    """Format 404 not found response"""
    return format_error_response('Not found', 404)


def format_unauthorized_response() -> dict:
    """Format 401 unauthorized response"""
    return format_error_response('Unauthorized', 401)


def format_forbidden_response() -> dict:
    """Format 403 forbidden response"""
    return format_error_response('Forbidden', 403)


def format_ratelimit_response(retry_after: int = 60) -> dict:
    """Format 429 rate limit response"""
    return {
        'statusCode': 429,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Retry-After': str(retry_after)
        },
        'body': json.dumps({'error': 'Rate limit exceeded'})
    }
