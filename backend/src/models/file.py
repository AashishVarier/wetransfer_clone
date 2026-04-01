"""
File model/schema
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class File:
    """File metadata model"""
    
    user_id: str
    file_id: str
    file_name: str
    file_size: int
    created_at: str
    expires_at: str
    
    # Optional fields
    content_type: Optional[str] = None
    s3_key: Optional[str] = None
    ttl: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'userId': self.user_id,
            'fileId': self.file_id,
            'fileName': self.file_name,
            'fileSize': self.file_size,
            'createdAt': self.created_at,
            'expiresAt': self.expires_at,
            'contentType': self.content_type,
            's3Key': self.s3_key,
            'ttl': self.ttl
        }
    
    @classmethod
    def from_dynamo(cls, item: dict) -> 'File':
        """Create from DynamoDB item"""
        return cls(
            user_id=item.get('userId'),
            file_id=item.get('fileId'),
            file_name=item.get('fileName'),
            file_size=item.get('fileSize'),
            created_at=item.get('createdAt'),
            expires_at=item.get('expiresAt'),
            content_type=item.get('contentType'),
            s3_key=item.get('s3Key'),
            ttl=item.get('ttl')
        )
