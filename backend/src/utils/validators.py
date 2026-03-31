"""
Validators - Input validation utilities
"""

from datetime import datetime


def validate_file_size(file_size: int, max_size_bytes: int = 2 * 1024 * 1024) -> bool:
    """
    Validate file size
    
    Args:
        file_size: File size in bytes
        max_size_bytes: Maximum allowed size (default 2 MB)
    
    Returns:
        True if valid
    
    TODO: Implement validation
    """
    return file_size > 0 and file_size <= max_size_bytes


def validate_file_name(file_name: str) -> bool:
    """
    Validate file name
    
    Args:
        file_name: File name
    
    Returns:
        True if valid
    
    TODO: Add validation rules (length, chars, etc.)
    """
    if not file_name or len(file_name) == 0:
        return False
    if len(file_name) > 255:
        return False
    # TODO: Check for invalid characters
    return True


def validate_user_id(user_id: str) -> bool:
    """
    Validate user ID format
    
    Args:
        user_id: User ID
    
    Returns:
        True if valid
    
    TODO: Implement validation based on your user ID format
    """
    if not user_id or not isinstance(user_id, str):
        return False
    if len(user_id) < 3 or len(user_id) > 50:
        return False
    return True


def is_file_expired(expires_at: str) -> bool:
    """
    Check if file has expired
    
    Args:
        expires_at: ISO timestamp string
    
    Returns:
        True if expired
    
    TODO: Implement expiration check
    """
    try:
        expires_dt = datetime.fromisoformat(expires_at)
        now = datetime.utcnow()
        return now > expires_dt
    except Exception:
        return False
