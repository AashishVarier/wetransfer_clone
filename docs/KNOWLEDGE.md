# WeTransfer Clone - Knowledge Base

> **Disclaimer:** These are opinions based on my experience and research into current industry best practices.

## Architecture Overview

### Why Multi-Lambda?

**Single Lambda (Bad)**
```
┌─────────────────────┐
│  Single Lambda      │
│  - Upload           │
│  - List Files       │
│  - Download         │
│  - Delete           │
│  - Rate Limit       │
│  (1000+ lines)      │
└─────────────────────┘
Problems:
- Hard to test individual functions
- Can't scale upload independently
- One failure affects everything
- Large deployment packages
- Difficult to understand code
```

**Multi-Lambda (Good)**
```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Upload       │ │ Delete       │ │ Download     │
│ Lambda       │ │ Lambda       │ │ Lambda       │
│ (150 lines)  │ │ (150 lines)  │ │ (150 lines)  │
└──────────────┘ └──────────────┘ └──────────────┘
Benefits:
- Each function has clear purpose
- Scale upload during peak time
- Delete runs on schedule
- Easier testing
- Clear separation of concerns
- Reusable services layer
```

### Service Layer Pattern

```
┌─────────────────────────────────────────┐
│ Lambda Handlers (Thin)                  │
│ - Event parsing                         │
│ - Input validation                      │
│ - Response formatting                   │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ Services (Business Logic)               │
│ - s3_service.py (S3 operations)        │
│ - dynamo_service.py (metadata)         │
│ - auth_service.py (authentication)     │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ AWS SDK (boto3)                         │
│ - Actual AWS API calls                 │
└─────────────────────────────────────────┘
```

**Why?**
- Handlers stay thin and focused
- Services are reusable across handlers
- Easy to test services independently (mock AWS)
- Easy to replace implementations (e.g., switch storage backend)

### Data Flow

#### Upload Request
```
1. Client (React) → API Gateway → upload.lambda_handler
2. Validate file size (2 MB max)
3. Call s3_service.get_presigned_upload_url()
4. Call dynamo_service.save_file_metadata()
5. Call sqs_service.enqueue_delete_task()
6. Return presigned URL to client
7. Client uploads file to S3 directly (presigned URL)
```

#### Delete Request (After 2 minutes)
```
1. SQS sends message to delete_file.lambda_handler
2. Extract userId and fileId
3. Call s3_service.delete_file_from_s3()
4. Call dynamo_service.delete_file_metadata()
5. Log completion
6. SQS marks message as processed
```

## Folder Structure Design

```
/wetransfer_clone
├── frontend/              # React/Vite app
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── services/      # API client wrappers
│   │   ├── hooks/         # Custom React hooks (TODO)
│   │   └── styles/        # Global styles (TODO)
│   └── tests/             # React testing library tests
│
├── backend/               # Python/Lambda backend
│   ├── src/               # Source code
│   │   ├── handlers/      # Lambda entry points (thin)
│   │   ├── services/      # Business logic (reusable)
│   │   ├── models/        # Data models
│   │   └── utils/         # Utilities (validators, formatters)
│   ├── tests/             # pytest tests
│   └── serverless.yml     # Infrastructure as code
│
├── infra/                 # Infrastructure
│   ├── cloudformation/    # CF templates (optional)
│   └── notes.md           # Deployment notes
│
├── docs/                  # Documentation
│   ├── INSTRUCTION.md     # How to use
│   ├── KNOWLEDGE.md       # (This file) Architecture
│   └── architecture.md    # System design diagrams
│
├── scripts/               # Deployment scripts
│   ├── deploy-frontend.sh
│   ├── deploy-backend.sh
│   └── dev.sh
│
├── .github/workflows/     # CI/CD (GitHub Actions)
└── root config files      # package.json, .gitignore, etc.
```

**Design Principles:**
- Clear separation: frontend vs backend vs infra
- Each folder is independently meaningful
- Services are shared (not duplicated)
- Tests live next to code they test
- Documentation is comprehensive
- Scripts are simple and reusable

## AWS Free Tier

### Service Limits

| Service | Free Tier | Monthly Cost (if exceeded) |
|---------|-----------|---------------------------|
| Lambda | 1M requests + 400K GB-seconds | $0.20 per 1M requests + $0.0000166667 per GB-second |
| DynamoDB | 25 GB storage | $1.25 per GB of storage + read/write charges |
| S3 | 5 GB storage | $0.023 per GB (after 1 year) |
| API Gateway | 1M requests | $3.50 per 1M requests |
| CloudWatch | 10 GB ingestion | $0.50 per GB |

### Safe Estimation

For typical usage (100 users, 10 files per user daily):

- **Lambda**: ~50K requests/month (well under 1M)
- **DynamoDB**: ~10 MB storage (< 25 GB)
- **S3**: ~400–600 MB (if files average 200 KB and keep for 48-72 hours)
- **API Gateway**: ~100K calls/month

**Total: FREE** (*under these usage assumptions **AND** if the first-year AWS free tier is still active, this workload is very likely free)

### What Breaks the Budget?

- Users uploading > 10 GB/day
- Files lasting > 7 days (instead of 2 minutes)
- Thousands of concurrent users
- Large file sizes (> 100 MB)

-> Monitor costs weekly!

## Security Considerations

### Current (Placeholder)

```python
# ❌ Not secure - for development only
user_id = 'user_placeholder'  # No auth
JWT_SECRET = 'dev-secret-change-in-production'
```

### TODO: Production Security

1. **Authentication**
   - Implement OAuth2 (Google, GitHub)
   - Or email/password with JWT
   - Store hashed passwords in DynamoDB
   - Use secure password generation

2. **Authorization**
   - Verify user owns file before download/delete
   - Rate limit: 100 requests per 15 minutes per user
   - Implement admin roles

3. **Data Protection**
   - Encrypt files in S3 (KMS)
   - Encrypt data in transit (HTTPS already done by AWS)
   - Encrypt sensitive fields in DynamoDB

4. **Compliance**
   - Log access (CloudTrail)
   - Regular security audits
   - Follow AWS Well-Architected Framework
   - Comply with regulations (GDPR, CCPA, etc.)

## Common Questions

### Q: Why 2-minute expiration?
- For demo purpose and for fast cleanup to keep storage costs low
- Discourages using for permanent storage
- Design choice: prioritize cost over convenience
- Can be updated by changing `FILE_EXPIRATION_MINUTES`

### Q: Why S3 + DynamoDB instead of database?
- S3: Optimized for large files, cheaper storage
- DynamoDB: Fast metadata queries, simple structure
- Alternative: Use RDS + EBS (more setup, more cost)

### Q: How do presigned URLs work?
- Client gets time-limited URL from Lambda
- Client uploads file directly to S3 (bypasses Lambda)
- Saves Lambda compute time
- S3 validates signature before accepting

### Q: Can I use this for large files?
- 2 MB limit by design (Free Tier optimization)
- Change `MAX_FILE_SIZE_BYTES` to 100 MB
- Cost warning: 100 MB × 1000 uploads = 100 GB/month

### Q: What happens if delete fails?
- SQS retries 3 times (default)
- Failed messages go to dead-letter queue
- Manual cleanup needed
- TODO: Implement better error handling

### Q: How do I add real authentication?
1. Add OAuth provider (Auth0, Cognito, etc.)
2. Implement login endpoint
3. Exchange OAuth token for JWT
4. Store JWT in localStorage
5. Include JWT in API requests (already done in api.js)
6. Validate JWT server-side (partly done in auth_service.py)

## Future Improvements

### Short Term (Easy)
- [ ] Add drag-and-drop upload
- [ ] Add file preview thumbnails
- [ ] Add real auth (not placeholder)
- [ ] Improve error messages

### Medium Term (Moderate)
- [ ] Add shareable links (public download without login)
- [ ] Add email/WhatsApp sharing
- [ ] Add upload batch operations
- [ ] Add file compression


## Monitoring & Debugging

### CloudWatch Logs
```bash
# View Lambda logs
serverless logs -f upload --stage dev --tail

# Filter by error
serverless logs -f upload --stage dev --filter "ERROR"

# View specific time range
serverless logs -f upload --stage dev --startTime 1m
```

### Metrics to Monitor
- Lambda: Duration, Errors, Throttles, Cold Starts
- DynamoDB: Consumed RCU/WCU, Throttles, Latency
- S3: Request Rate, 4xx/5xx Errors, Transfer Rate
- API Gateway: Count, IntegrationLatency, Latency

### X-Ray Tracing (TODO)
Add for production debugging:
```yaml
# In serverless.yml
provider:
  tracing:
    lambda: true
    apiGateway: true
```

## Testing Strategy

### Unit Tests
- Test each handler independently
- Mock S3, DynamoDB responses
- Test validation logic
- Fast execution (< 100ms)

### Integration Tests
- Test handler + services together
- Use LocalStack or moto for AWS mocking
- Test error scenarios

### End-to-End Tests
- Test full flow through deployed API
- Use customer-like credentials
- Run in staging environment

### Load Testing
- Use locust or k6
- Simulate 100+ concurrent users
- Monitor costs during test

## Performance Optimization

### Lambda
- Cold start: First request takes ~3s (use provisioned concurrency)
- Warm execution: ~100-200ms per request
- Memory: 256 MB default (adjust if needed)

### DynamoDB
- On-demand billing: Scale automatically
- Indexes: Add GSI for faster queries
- TTL: Automatic deletion of expired items

### S3
- CloudFront CDN: Cache downloads globally
- Transfer acceleration: Faster uploads
- S3 Select: Query file contents without downloading

## References

### Architecture Foundation
- AWS Serverless Architecture - https://aws.amazon.com/serverless/
- AWS Well-Architected Framework - https://aws.amazon.com/architecture/well-architected/
- Serverless Framework Docs - https://www.serverless.com/framework/docs
- Event-Driven Architecture on AWS - https://aws.amazon.com/event-driven-architecture/

### AWS Services Used
- Lambda - Compute Service - https://docs.aws.amazon.com/lambda/
- API Gateway - REST APIs - https://docs.aws.amazon.com/apigateway/
- S3 - Object Storage - https://docs.aws.amazon.com/s3/
- DynamoDB - NoSQL Database - https://docs.aws.amazon.com/dynamodb/
- SQS - Message Queue - https://docs.aws.amazon.com/sqs/
- CloudWatch - Monitoring - https://docs.aws.amazon.com/cloudwatch/

### Implementation Essentials
- Serverless Framework AWS Provider Guide - https://www.serverless.com/framework/docs/providers/aws/
- React 18 Documentation - https://react.dev/
- Vite Guide - https://vitejs.dev/guide/
- boto3 AWS SDK for Python - https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- pytest Documentation - https://docs.pytest.org/

### AWS Service Deep Dives
- Lambda Best Practices - https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html
- S3 Presigned URLs - https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html
- S3 Lifecycle Policies - https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html
- DynamoDB Best Practices - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html
- DynamoDB TTL - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html
- SQS Best Practices - https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-best-practices.html
- API Gateway Rate Limiting - https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html

### Security & Authentication
- JWT.io Introduction - https://jwt.io/introduction
- PyJWT Documentation - https://pyjwt.readthedocs.io/
- AWS IAM Best Practices - https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- OAuth 2.0 Specification - https://tools.ietf.org/html/rfc6749
- OWASP Top 10 - https://owasp.org/www-project-top-ten/

### Cost Management
- AWS Free Tier Overview - https://aws.amazon.com/free/
- AWS Pricing Calculator - https://calculator.aws/
- Lambda Cold Starts Optimization - https://aws.amazon.com/blogs/compute/operating-lambda-performance-optimization-part-1/

### Testing
- React Testing Library - https://testing-library.com/docs/react-testing-library/intro/
- pytest Documentation - https://docs.pytest.org/

