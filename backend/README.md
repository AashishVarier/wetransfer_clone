# Backend - WeTransfer Clone

Python + AWS Lambda + Serverless Framework  for the file sharing API.

## Setup

### Prerequisites
- Python 3.11+
- AWS account with configured credentials
- Node.js 16+ (for Serverless Framework)

### Installation

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Install Serverless Framework (if not already installed):
```bash
npm install -g serverless
```

### Local Testing

Run tests:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

### Development

For local development, you can use Serverless Offline plugin:
```bash
# Install plugin (add to package.json or install globally)
npm install --save-dev serverless-offline

# Run locally
serverless offline start
```

API will be available at `http://localhost:3000/api`

### Deployment

Deploy to AWS Lambda:
```bash
serverless deploy
```

This will:
- Create/update Lambda function
- Set up API Gateway triggers
- Output the API endpoint URL

## Project Structure

- `handler.py` - Main Lambda handler with route logic
- `services/s3_service.py` - S3 file operations
- `services/metadata_service.py` - File metadata (DynamoDB)
- `tests/test_handler.py` - Unit tests
- `serverless.yml` - Serverless Framework configuration

## Environment Variables

Add to `.env` or AWS Lambda environment:
- `S3_BUCKET_NAME` - S3 bucket for file storage
- `DYNAMODB_TABLE_NAME` - DynamoDB table for metadata
- `FILE_EXPIRATION_MINUTES` - Auto-delete timeout (default: 2 minutes)

## API Endpoints

### POST /upload
Upload a file

**TODO: Implement request/response format**

### GET /files
List user's files

**TODO: Implement request/response format**

### GET /files/{fileId}
Download a file

**TODO: Implement request/response format**

### DELETE /files/{fileId}
Delete a file

**TODO: Implement request/response format**

## TODO

- [ ] Implement S3 upload logic
- [ ] Implement DynamoDB metadata storage
- [ ] Add authentication/authorization
- [ ] Implement rate limiting
- [ ] Add file expiration logic
- [ ] Implement error handling
- [ ] Add logging
