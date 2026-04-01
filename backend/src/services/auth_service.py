"""
Auth Service - Handles authentication and authorization
"""

import os
import jwt
from functools import wraps

# TODO: Implement authentication service
# Configure with your JWT secret
JWT_SECRET = os.getenv('JWT_SECRET', 'dev-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'


def get_user_from_token(token: str) -> dict:
    """
    Extract user information from JWT token
    
    Args:
        token: JWT token (may include "Bearer " prefix)
    
    Returns:
        User dictionary with user_id and other claims
    
    TODO: Add proper JWT validation
    TODO: Handle expired tokens
    TODO: Add token refresh logic
    TODO: Add role-based access control
    """
    try:
        # Remove "Bearer " prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        # TODO: Verify token signature
        # TODO: Check token expiration
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        return {
            'user_id': payload.get('sub'),
            'email': payload.get('email'),
            'roles': payload.get('roles', [])
        }
        
    except jwt.ExpiredSignatureError:
        print('Token has expired')
        raise ValueError('Token expired')
    except jwt.InvalidTokenError as e:
        print(f'Invalid token: {str(e)}')
        raise ValueError('Invalid token')


def validate_auth_token(auth_header: str) -> str:
    """
    Validate Authorization header and extract user ID
    
    Args:
        auth_header: Authorization header value (e.g., "Bearer <token>")
    
    Returns:
        User ID
    
    TODO: Implement proper validation
    TODO: Add error handling
    """
    if not auth_header:
        raise ValueError('Authorization header required')
    
    try:
        token = auth_header.replace('Bearer ', '')
        user_info = get_user_from_token(token)
        return user_info['user_id']
    except Exception as e:
        print(f'Auth validation failed: {str(e)}')
        raise ValueError('Invalid authorization')


def create_jwt_token(user_id: str, email: str = None, roles: list = None, expires_in: int = 3600) -> str:
    """
    Create a new JWT token
    
    Args:
        user_id: User ID
        email: User email
        roles: User roles
        expires_in: Token expiration in seconds
    
    Returns:
        JWT token
    
    TODO: Implement token creation with proper claims
    TODO: Add token refresh logic
    """
    try:
        import time
        
        payload = {
            'sub': user_id,
            'email': email,
            'roles': roles or [],
            'iat': int(time.time()),
            'exp': int(time.time()) + expires_in
        }
        
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
        
    except Exception as e:
        print(f'Error creating token: {str(e)}')
        raise


def verify_user_owns_file(user_id: str, file_user_id: str) -> bool:
    """
    Verify that a user owns a file
    
    Args:
        user_id: Requesting user ID
        file_user_id: File owner user ID
    
    Returns:
        True if user owns file
    
    TODO: Add admin override
    """
    return user_id == file_user_id


def require_auth(handler):
    """
    Decorator to require authentication for a handler
    
    Usage:
        @require_auth
        def my_handler(event, context, user_id):
            ...
    
    TODO: Implement decorator
    """
    @wraps(handler)
    def wrapper(event, context):
        try:
            auth_header = event.get('headers', {}).get('Authorization', '')
            user_id = validate_auth_token(auth_header)
            return handler(event, context, user_id)
        except ValueError as e:
            return {
                'statusCode': 401,
                'body': {'error': str(e)}
            }
    return wrapper


def is_admin(user_id: str) -> bool:
    """
    Check if user is an admin
    
    Args:
        user_id: User ID
    
    Returns:
        True if user is admin
    
    TODO: Implement admin check (query database or cache)
    """
    # TODO: Check against admin list in DynamoDB or cache
    return False
