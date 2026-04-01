"""
Rate limit handler - Per-user request limiting
Uses DynamoDB atomic counters with TTL for rate limiting
"""

import json
import time

# TODO: Import from src.services when implemented
# from src.services.dynamo_service import check_rate_limit, increment_rate_counter
# from src.services.auth_service import get_user_from_token


def lambda_handler(event, context):
    """
    Lambda handler for rate limiting
    Can be used as an authorizer or called directly
    
    Expected event (as authorizer):
    {
        "type": "TOKEN",
        "methodArn": "arn:aws:execute-api:...",
        "authorizationToken": "Bearer <token>"
    }
    
    Expected event (as direct call):
    {
        "headers": {
            "Authorization": "Bearer <token>"
        }
    }
    
    Returns (as authorizer):
    {
        "principalId": "user_id",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow" or "Deny",
                    "Resource": "arn:..."
                }
            ]
        }
    }
    
    Returns (as direct call):
    {
        "statusCode": 200 or 429,
        "body": {
            "allowed": true/false,
            "remaining": X,
            "resetAt": timestamp
        }
    }
    
    TODO: Extract user ID from Authorization header
    TODO: Query DynamoDB for rate limit counter
    TODO: Compare against limit (e.g., 100 requests per 15 minutes)
    TODO: Increment counter atomically
    TODO: Set TTL on counter
    TODO: Return allow or deny policy
    TODO: Add logging
    
    RATE LIMIT STRATEGY:
    - 100 requests per 15 minutes per user
    - Counter stored in DynamoDB with TTL of 15 minutes
    - Use atomic increment to avoid race conditions
    """
    
    try:
        # TODO: Extract user ID from Authorization header or token
        # user_id = validate_auth_token(get_token_from_event(event))
        user_id = 'user_placeholder'  # Placeholder
        
        # Rate limit configuration
        MAX_REQUESTS = 100
        WINDOW_MINUTES = 15
        WINDOW_SECONDS = WINDOW_MINUTES * 60
        
        # TODO: Query DynamoDB rate limit counter for this user
        # current_count = get_rate_limit_counter(user_id)
        current_count = 1  # Placeholder
        
        # Check if rate limit exceeded
        allowed = current_count <= MAX_REQUESTS
        
        # TODO: Increment counter atomically in DynamoDB
        # reset_time = increment_rate_counter(user_id, window_seconds=WINDOW_SECONDS)
        reset_time = int(time.time()) + WINDOW_SECONDS
        
        if event.get('type') == 'TOKEN':
            # Return authorizer policy
            return {
                'principalId': user_id,
                'policyDocument': {
                    'Version': '2012-10-17',
                    'Statement': [
                        {
                            'Action': 'execute-api:Invoke',
                            'Effect': 'Allow' if allowed else 'Deny',
                            'Resource': event.get('methodArn', '*')
                        }
                    ]
                },
                'context': {
                    'remainingRequests': str(max(0, MAX_REQUESTS - current_count)),
                    'resetAt': str(reset_time)
                }
            }
        else:
            # Return direct response
            status_code = 200 if allowed else 429
            return {
                'statusCode': status_code,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'X-RateLimit-Limit': str(MAX_REQUESTS),
                    'X-RateLimit-Remaining': str(max(0, MAX_REQUESTS - current_count)),
                    'X-RateLimit-Reset': str(reset_time)
                },
                'body': json.dumps({
                    'allowed': allowed,
                    'remaining': max(0, MAX_REQUESTS - current_count),
                    'resetAt': reset_time
                })
            }
        
    except Exception as e:
        print(f'Error in rate_limit handler: {str(e)}')
        # Default to allow in case of error
        return {
            'principalId': 'user',
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Effect': 'Allow',
                        'Resource': event.get('methodArn', '*')
                    }
                ]
            }
        }
