# Backend - WeTransfer Clone

Python + AWS Lambda + Serverless Framework for the file sharing API.

Multi-Lambda architecture with separate handlers for each operation.

## Setup

### Prerequisites
- Python 3.11+
- AWS account with configured credentials
- Node.js 16+ (for Serverless Framework)
- Bash shell

### Installation

Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

Install Serverless Framework (if not already installed):
```bash
npm install -g serverless
```

### Local Testing

Run backend tests using pytest:
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_upload.py
```

### Development

Use the development helper script from the root directory:
```bash
bash scripts/dev.sh setup     # First-time setup
bash scripts/dev.sh backend   # Run all backend tests
bash scripts/dev.sh test      # Run all tests (frontend + backend)
```

Or run tests locally:
```bash
python -m pytest tests/ -v
```

### Deployment

Deploy to AWS Lambda:
```bash
bash ../scripts/deploy-backend.sh dev
```

Or use Serverless directly:
```bash
serverless deploy --stage dev
```

This will:
- Create Lambda functions for each handler
- Set up API Gateway with routes
- Create S3 bucket, DynamoDB tables, and SQS queue
- Set up IAM roles and permissions
- Output the API endpoint URL

## Project Structure

```
backend/
├── src/
│   ├── handlers/              # 5 separate Lambda functions
│   │   ├── upload.py          # POST /upload - File upload with presigned URL
│   │   ├── list_files.py      # GET /files - List user's files
│   │   ├── download.py        # GET /files/{fileId} - Presigned download URL
│   │   ├── delete_file.py     # DELETE /files/{fileId} + SQS trigger
│   │   └── rate_limit.py      # API Gateway rate limit authorizer
│   ├── services/              # Reusable business logic
│   │   ├── s3_service.py      # S3 operations (presigned URLs, deletion)
│   │   ├── dynamo_service.py  # DynamoDB operations (metadata, rate limits)
│   │   └── auth_service.py    # JWT validation and user extraction
│   ├── utils/                 # Shared utilities
│   │   ├── validators.py      # Input validation (file size, names, etc.)
│   │   ├── response_formatter.py  # Consistent API response format
│   │   └── logger.py          # Structured logging to CloudWatch
│   └── models/
│       └── file.py            # File metadata dataclass
├── tests/                     # pytest test suite
│   ├── conftest.py            # pytest fixtures
│   ├── test_upload.py
│   ├── test_list_files.py
│   ├── test_download.py
│   ├── test_delete_file.py
│   └── test_rate_limit.py
├── requirements.txt           # Python dependencies
├── serverless.yml             # Serverless Framework IaC configuration
├── .env.example               # Environment variables template
└── README.md

Key files:
- **serverless.yml** - Complete AWS infrastructure definition (S3, DynamoDB, SQS, Lambda, IAM)
- **requirements.txt** - boto3, PyJWT, pytest, pytest-cov
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key variables:
- `AWS_REGION` - AWS region (default: us-east-1)
- `S3_BUCKET_NAME` - S3 bucket for file storage
- `DYNAMODB_TABLE_NAME` - DynamoDB table for file metadata
- `DYNAMODB_RATELIMIT_TABLE` - DynamoDB table for rate limit counters
- `SQS_QUEUE_URL` - SQS queue for delayed file deletion
- `JWT_SECRET` - Secret key for JWT validation
- `FILE_EXPIRATION_MINUTES` - Auto-delete timeout (default: 2)
- `RATE_LIMIT_REQUESTS` - Max requests per window (default: 100)
- `RATE_LIMIT_WINDOW_MINUTES` - Rate limit window (default: 15)

## API Endpoints

All endpoints require `Authorization: Bearer <JWT_TOKEN>` header.

### POST /upload
Upload a file (max 2 MB)
```json
Request: { "filename": "doc.pdf" }
Response: { "uploadUrl": "https://...", "fileId": "...", "expiration": "..." }
```

### GET /files
List user's uploaded files with pagination
```json
Response: {
  "files": [
    {"fileId": "...", "filename": "...", "size": 1024, "uploadedAt": "...", "expiresAt": "..."}
  ],
  "nextToken": "..."
}
```

### GET /files/{fileId}
Get presigned download URL for a file
```json
Response: { "downloadUrl": "https://...", "expiresAt": "..." }
```

### DELETE /files/{fileId}
Delete a file (queued via SQS)
```json
Response: { "status": "deletion_queued", "fileId": "..." }
```

### Custom Authorization
Rate limit authorizer: `X-Rate-Limit-Check` header
```
Response: API Gateway policy (allow/deny based on rate limits)
```

## Architecture Decisions

**Multi-Lambda (not monolithic):**
- Each handler (upload, list, download, delete, rate_limit) is independent
- Enables independent scaling, testing, and deployment
- Clear separation of concerns

**Presigned URLs:**
- Frontend/client uploads directly to S3, bypassing Lambda
- Reduces Lambda compute, saves bandwidth and costs
- Same for downloads

**DynamoDB on-demand:**
- Currently considering automatic scaling with per-request billing
- TTL policies auto-delete expired files metadata
- Rate limit counters with atomic operations

**SQS for file deletion:**
- Decouples deletion from API response
- 120s visibility timeout for duplicate handling
- Eventually consistent cleanup

**Service layer pattern:**
- Handlers: Parse event, validate, coordinate services
- Services: Encapsulate AWS SDK calls, business logic
- Utils: Cross-cutting concerns (validation, formatting, logging)

See `../../docs/KNOWLEDGE.md` and `../../docs/architecture.md` for detailed architecture discussion.

## Testing

The test suite includes:
- Input validation tests
- API response format verification
- DynamoDB operation mocking
- S3 presigned URL generation
- JWT token validation
- Rate limit counter logic
- SQS message handling

Run tests:
```bash
pytest tests/ -v --cov=src
```

See `conftest.py` for fixture setup and AWS credential mocking.

## Deployment Checklist

1. **Configure AWS credentials:**
   ```bash
   aws configure
   ```

2. **Set environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   npm install -g serverless
   ```

4. **Deploy backend:**
   ```bash
   bash ../scripts/deploy-backend.sh dev
   ```

5. **Verify deployment:**
   - Check CloudFormation stack in AWS Console
   - Test API endpoints with Authorization header
   - Verify S3 bucket created with correct permissions

6. **Monitor:**
   - CloudWatch Logs: `/aws/lambda/wetransfer-*`
   - DynamoDB: Check table contents and TTL cleanup
   - API Gateway: Check request/response metrics

## Troubleshooting

**Lambda function not found:**
- Check `serverless.yml` handler paths match actual file structure
- Verify `src/handlers/__init__.py` exists (Python package marker)

**DynamoDB access denied:**
- Verify IAM role has `DynamoDB:*` permissions
- Check table names in environment variables match `serverless.yml`

**S3 presigned URL invalid:**
- Check bucket name and region in environment variables
- Verify S3 bucket exists and handler has `s3:*` permissions

**Tests failing:**
- Ensure pytest fixtures in `conftest.py` mock AWS services correctly
- Check Python version (requires 3.11+)
- Run `pip install -r requirements.txt` to get latest dependencies

See `../../docs/INSTRUCTION.md` for complete troubleshooting guide.

## Production Hardening

The code includes TODO comments marking areas for production implementation:
- [ ] Real JWT validation (currently stubbed)
- [ ] S3/DynamoDB error handling (currently placeholder)
- [ ] Comprehensive logging context
- [ ] Dead-letter queue for failed deletions
- [ ] CloudWatch alarms and monitoring
- [ ] Rate limit fine-tuning based on metrics

Start with `src/services/auth_service.py` and `src/handlers/*.py` TODO sections.
