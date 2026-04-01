# WeTransfer Clone - Instructions

## Overview

WeTransfer Clone is a file-sharing application that allows users to upload files temporarily (auto-delete after 2 minutes). The application uses a monorepo structure with:

- **Frontend**: React + Vite + Tailwind CSS (static S3 hosting)
- **Backend**: Python + AWS Lambda + API Gateway
- **Storage**: S3 for files, DynamoDB for metadata, SQS for async tasks
- **Infrastructure**: Serverless Framework + CloudFormation

## Why This Structure?

### Multi-Lambda Backend
- **Separation of Concerns**: Each Lambda handles one responsibility
- **Independent Scaling**: Upload handlers scale independently from delete handlers
- **Easier Debugging**: Logs and errors are organized per function
- **Cost Control**: You only pay for what you use

### Monorepo Layout
- **Single Repository**: Easier to manage dependencies and versions
- **Clear Boundaries**: Frontend, backend, infra, docs are separate but related
- **Shared Documentation**: Everyone understands the structure

### AWS Services (*as of 31 March 2026)
- **S3**: Free tier includes 5 GB storage (files auto-delete after 2 minutes)
- **DynamoDB**: Free tier includes 25 GB storage with on-demand pricing
- **Lambda**: Free tier includes 1M invocations/month
- **API Gateway**: Free tier includes 1M API calls/month

## Local Setup

### Prerequisites
- Node.js 16+ (for frontend)
- Python 3.11 (for backend)
- AWS CLI v2
- Serverless Framework: `npm install -g serverless@latest`
- Git

### Installation

```bash
# Clone repository
git clone <repo-url>
cd wetransfer-clone

# Frontend setup
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your values

# Backend setup
cd ../backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your values
```

## Running Locally

### Frontend Development

```bash
cd frontend
npm run dev
# Opens at http://localhost:5173
```

### Backend Local Testing

```bash
cd backend
# Run unit tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/

# TODO: Use serverless-offline for local API simulation
# serverless offline start
```

## Deployment

### Frontend Deployment to S3

```bash
cd frontend

# Build
npm run build

# Deploy to S3
# TODO: Implement in scripts/deploy-frontend.sh
# bash ../scripts/deploy-frontend.sh
```

### Backend Deployment with Serverless

```bash
cd backend

# Deploy to dev
serverless deploy --stage dev

# Deploy to production
serverless deploy --stage prod --region us-east-1
```

See `scripts/` for helper scripts.

## Environment Variables

### Frontend (.env.local)
- `VITE_API_BASE_URL`: Backend API URL
- `VITE_MAX_FILE_SIZE_MB`: Maximum file size
- `VITE_FILE_EXPIRATION_MINUTES`: File auto-delete time

### Backend (.env)
- `S3_BUCKET_NAME`: S3 bucket for files
- `DYNAMODB_TABLE_NAME`: DynamoDB metadata table
- `JWT_SECRET`: Secret for JWT tokens
- `AWS_REGION`: AWS region (default: us-east-1)

## Testing

### Frontend Tests
```bash
cd frontend
npm run test              # Run tests once
npm run test:watch       # Run tests in watch mode
```

### Backend Tests
```bash
cd backend
pytest tests/             # Run all tests
pytest tests/test_upload.py  # Run specific test
pytest --cov=src/        # Run with coverage report
```

## Verifying Upload/Download/Delete Flow

1. **Start frontend**: `cd frontend && npm run dev`
2. **Deploy backend**: `cd backend && serverless deploy --stage dev`
3. **Get API URL**: Check serverless deployment output
4. **Update frontend**: Set `VITE_API_BASE_URL` to API URL
5. **Test flow**:
   - Login with demo credentials
   - Upload a file < 2 MB
   - Verify it appears in file list
   - Copy share link and verify in new tab
   - Wait 2 minutes and verify file auto-deletes
   - Try uploading > 2 MB and verify error

## Cost Control for AWS Free Tier

### Safe Limits
- **Files**: Keep under 1000 current files
- **Upload rate**: 100 files/hour per user
- **File size**: 2 MB max per file
- **Retention**: 2 minutes (automatic deletion)
- **Requests**: ~100-1000 per day per user

### Monitoring
- Set CloudWatch alarms for cost spikes
- Use AWS Cost Explorer to track usage
- Review S3, DynamoDB, Lambda metrics weekly

### Cost Optimization
- Use S3 lifecycle policies (configured)
- Use DynamoDB on-demand billing (configured)
- Use Lambda concurrency limits
- Implement rate limiting per user
- Auto-delete files after retention period

## Troubleshooting

### Frontend | Cannot connect to API
- Check `VITE_API_BASE_URL` in `.env.local`
- Verify backend is deployed: `serverless info --stage dev`
- Check browser console for CORS errors
- Verify API Gateway CORS is enabled

### Backend | Lambda errors
- Check CloudWatch logs: `serverless logs -f upload --stage dev`
- Verify S3 bucket exists: `aws s3 ls`
- Check DynamoDB table exists: `aws dynamodb list-tables`
- Verify IAM permissions in `serverless.yml`

### Upload fails
- Verify file size < 2 MB (checked client-side)
- Check S3 bucket permissions
- Verify AWS credentials are valid
- Check CloudWatch logs for errors

## Architecture Diagram

```
┌─────────────────────────────────────┐
│   React Frontend (Vite + Tailwind)  │
│        (Static S3 Hosting)          │
└────────────┬────────────────────────┘
             │ HTTPS
             ▼
┌─────────────────────────────────────┐
│        API Gateway                  │
│        (Rate Limiting)              │
└────────────┬────────────────────────┘
             │
    ┌────────┼────────┬───────────┐
    ▼        ▼        ▼           ▼
  Upload  ListFiles Download Delete
  Lambda  Lambda    Lambda   Lambda
    │        │        │        │
    └─────┬──┴────┬───┴────┬───┘
          ▼       ▼        ▼
        ┌──────────────────────┐
        │  DynamoDB (Metadata) │
        │  (Per-user indexed)  │
        └──────────────────────┘
              │
        ┌─────┴─────┐
        ▼           ▼
      ┌───┐    ┌─────────┐
      │S3 │    │SQS Queue│
      │   │    │(Deletes)│
      └───┘    └─────────┘
```

## Production Hardening (TODO)

Before going to production, implement:

1. **Security**
   - [ ] JWT token refresh
   - [ ] Implement proper auth (OAuth/Email)
   - [ ] Add request signing
   - [ ] Rate limiting per IP and user
   - [ ] WAF rules

2. **Reliability**
   - [ ] Error handling and retries
   - [ ] Dead-letter queue for failed deletions
   - [ ] Backup and disaster recovery
   - [ ] Multi-region failover

3. **Monitoring**
   - [ ] CloudWatch dashboards
   - [ ] X-Ray tracing
   - [ ] Error tracking (Sentry)
   - [ ] Performance monitoring

4. **Compliance**
   - [ ] Encryption at rest and in transit
   - [ ] Audit logging
   - [ ] Data retention policies
   - [ ] Privacy policy

## More Information

- See `docs/KNOWLEDGE.md` for architecture details
- See `docs/architecture.md` for system design
- See backend `serverless.yml` for infrastructure code
- See frontend components for UI implementation details


## Support

TODO: Add support channels, issue tracking, contribution guidelines.
