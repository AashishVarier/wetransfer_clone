"""
Logger - Logging utilities
"""

import json
from datetime import datetime


def log_debug(message: str, extra: dict = None):
    """Log debug message"""
    log_message('DEBUG', message, extra)


def log_info(message: str, extra: dict = None):
    """Log info message"""
    log_message('INFO', message, extra)


def log_warning(message: str, extra: dict = None):
    """Log warning message"""
    log_message('WARNING', message, extra)


def log_error(message: str, extra: dict = None):
    """Log error message"""
    log_message('ERROR', message, extra)


def log_message(level: str, message: str, extra: dict = None):
    """
    Log message with consistent format
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        message: Log message
        extra: Extra data to include
    """
    log_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'level': level,
        'message': message
    }
    
    if extra:
        log_data.update(extra)
    
    print(json.dumps(log_data))
