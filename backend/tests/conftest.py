"""
Backend tests - pytest configuration
"""

import pytest
import os


@pytest.fixture
def aws_credentials():
    """Mock AWS credentials for tests"""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'


@pytest.fixture
def env_vars():
    """Set up environment variables for tests"""
    os.environ['S3_BUCKET_NAME'] = 'test-bucket'
    os.environ['DYNAMODB_TABLE_NAME'] = 'test-table'
    os.environ['JWT_SECRET'] = 'test-secret'
