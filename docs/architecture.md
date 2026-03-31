# Architecture

> **Disclaimer:** These are recommendations based on my experience and research into current industry best practices.

## System Components

### Frontend Deployment
```
React/Vite App (Built HTML/CSS/JS)
        ↓
   S3 Static Hosting
        ↓
  CloudFront (CDN) [Optional]
        ↓
   Browser/Client
```

### Backend Architecture
```
Client (Browser)
        │ HTTPS
        ↓
   API Gateway
   ├─ Rate Limiting
   ├─ CORS Headers
   ├─ Request Logging
        │
        ├────────┬────────┬──────────┬───────────┐
        ▼        ▼        ▼          ▼           ▼
   Upload   List    Download   Delete     RateLimit
   Lambda   Files   Lambda    Lambda     Authorizer
   Lambda                      │
        │        │        │    │         │
        └────────┼────────┴────┼─────────┘
                 ▼             │
            DynamoDB  ◄────────┘
            (Metadata)
                 │
          ┌──────┴──────┐
          ▼             ▼
      Metadata    RateLimit
      Table       Table (TTL)
      (Per-user)
                 
          Upload ──────► Delete
          Lambda        Lambda
            │               │
            ▼               ▼
          S3 Bucket  ◄─── SQS Queue
          (Files)         (Async Delete)
```

## Data Flow

### 1. Upload Flow

```
Client                 API Gateway           Lambda (upload)
  │                          │                      │
  │ 1. Select File           │                      │
  ├─────────────────────────►│                      │
  │                          │ 2. Invoke Handler   │
  │                          ├─────────────────────►│
  │                          │                      │ 3. Validate size
  │                          │                      │ 4. Get presigned URL
  │                          │◄─────────────────────┤
  │                          │ 5.Return presigned  │
  │◄─────────────────────────┤    URL + fileId    │
  │                          │                      │
  │ 6. Upload to S3 (direct) │                      │
  │────────────────────────────────────────────────►│ (S3)
  │                          │                      │
  │ 7. Show file in list     │                      │ 8. SQS: Schedule
  ├──────────────────────────────────────────────────►   deletion
  │                          │                      │    (2 min)
  │ Done                     │                      │
```

### 2. List Files Flow

```
Client                 API Gateway           Lambda (list_files)
  │                          │                      │
  │ 1. Request: GET /files   │                      │
  ├─────────────────────────►│                      │
  │                          │ 2. Check Auth       │
  │                          ├─────────────────────►│
  │                          │                      │ 3. Query DynamoDB
  │                          │◄─────────────────────┤
  │                          │    [file1, file2]   │
  │◄─────────────────────────┤                      │
  │ 4. Display Files         │                      │
```

### 3. Download Flow

```
Client                 API Gateway           Lambda (download)
  │                          │                      │
  │ Click Download Button    │                      │
  │                          │                      │
  │ 1. GET /files/{fileId}   │                      │
  ├─────────────────────────►│                      │
  │                          │ 2. Get presigned URL│
  │                          ├─────────────────────►│
  │                          │                      │ 3. Query metadata
  │                          │                      │ 4. Check expiration
  │                          │◄─────────────────────┤
  │                          │   presigned URL    │
  │◄─────────────────────────┤                      │
  │                          │                      │
  │ 5. Download from S3 (direct)                   │
  │────────────────────────────────────────────────►│ (S3)
  │◄────────────────────────────────────────────────┤
  │ 6. File saved locally    │                      │
```

### 4. Auto-Delete Flow

```
After 2 minutes:

SQS Queue                 Lambda (delete_file)
    │                            │
    │ 1. Check scheduled messages│
    │                            │
    ├─ Message Ready ────────────►│
    │   {userId, fileId}         │
    │                            │ 2. Delete from S3
    │                            │ 3. Delete metadata
    │                            │ 4. Log completion
    │◄─ ACK (message processed)  │
    │                            │
    │ Message removed            │
```

## Technology Choices

### Frontend: React + Vite
- **Why React**: Component-based, large ecosystem, easy to scale
- **Why Vite**: Fast build (HMR), modern tooling, small bundle
- **Styling**: Tailwind CSS (utility-first, no CSS bloat)
- **Testing**: Jest + React Testing Library (standard)

### Backend: Python + Lambda
- **Why Lambda**: Serverless (no ops), scales automatically, cheap
- **Why Python**: Easy to read, large library ecosystem, good for AWS
- **Deployment**: Serverless Framework (infrastructure as code)
- **Testing**: pytest (standard in Python)

### Storage: S3 + DynamoDB + SQS
- **S3**: Best for files (cheap storage, automatic scaling)
- **DynamoDB**: Best for metadata (fast queries, NoSQL flexibility)
- **SQS**: Best for async tasks (reliable message queue, distributed)

### Why Not Alternatives?

| Choice | Alternative | Why Not Used |
|--------|-------------|-------------|
| Lambda | EC2 | More ops overhead, harder to scale, more expensive |
| Lambda | App Engine | vendor lock-in to GCP, less flexible |
| S3 | RDS + EBS | Slower for large files, more expensive, more setup |
| DynamoDB | MongoDB | Need AWS integration, simpler schema |
| Vite | Webpack | Slower builds, older tooling |
| React | Vue | Either works; React has larger ecosystem |

## Security Architecture

```
┌────────────────────────────────────────┐
│ Client (Browser)                       │
│ - Demo login (TODO: Real OAuth)        │
│ - JWT stored in localStorage           │
│ - HTTPS only                           │
└────────────┬───────────────────────────┘
             │
        ┌────▼─────────────────┐
        │ API Gateway          │
        │ - TLS/HTTPS 1.2+     │
        │ - CORS validation    │
        │ - Request logging    │
        │ - DDoS protection    │
        └────┬──────────────────┘
             │
        ┌────▼─────────────────┐
        │ Lambda Handler       │
        │ - Validate JWT       │
        │ - Rate limit check   │
        │ - Input validation   │
        └────┬──────────────────┘
             │
        ┌────▼─────────────────┐
        │ AWS Services         │
        │ - S3 (private)       │
        │ - DynamoDB (private) │
        │ - Encryption (KMS)   │
        └──────────────────────┘
```

## Cost Architecture as of 31 March 2026

```
User Action          AWS Service        Cost (Free Tier)
─────────────────────────────────────────────────────
Upload 1 MB file     Lambda             $0.00 (1M/mo free)
                     API Gateway        $0.00 (1M/mo free)
                     GetObject (S3)     $0.00 (free tier)
                     PutObject (S3)     $0.00 (free tier)
                     DynamoDB Write     $0.00 (25GB free)

List files           Lambda             $0.00
                     API Gateway        $0.00
                     DynamoDB Query     $0.00

Download file        S3 (GetObject)     $0.00

Auto-delete (2 min)  Lambda (delete)    $0.00
                     SQS                $0.00 (free tier)
                     DynamoDB Delete    $0.00

Monthly total (100 users, 10 files each)
                     Lambda Requests    ~100K (under 1M)
                     API Calls          ~100K (under 1M)
                     S3 Storage         ~100GB (under free, but could exceed)
                     DynamoDB           <25GB

⚠️  Monitor S3 storage if files stay longer than 2 minutes!
```

## Scaling Strategy (Reommendations based on my experince and research)

### Current (Placeholder)
- ✓ Single-region deployment
- ✓ On-demand DynamoDB scaling
- ✓ Lambda auto-scaling
- ✓ Presigned URLs avoid Lambda bottleneck

### Production
- [ ] Multi-region failover
- [ ] DynamoDB global tables
- [ ] CloudFront CDN for frontend
- [ ] Lambda provisioned concurrency
- [ ] S3 transfer acceleration
- [ ] Caching layer (ElastiCache)

## Monitoring & Alerts

### Key Metrics
1. **Lambda**: Duration, Errors, Throttles, Cold Starts
2. **DynamoDB**: Read/Write Throttles, Latency
3. **S3**: 4xx/5xx Errors, Upload Duration
4. **API Gateway**: Count, Latency, 4xx/5xx Errors
5. **Application**: Successful Uploads, Failed Uploads, Avg File Size

### Recommended Alarms
- Lambda error rate > 1%
- DynamoDB throttles > 0
- API latency > 1s (p99)
- Cost spike > 2x normal

### Dashboards (TODO)
- Create CloudWatch dashboard
- Add custom metrics
- Set up automated reports

## Disaster Recovery

### RTO (Recovery Time Objective): 1 hour
### RPO (Recovery Point Objective): 5 minutes

### Backup Strategy
- [ ] S3 cross-region replication
- [ ] DynamoDB point-in-time recovery
- [ ] Regular database snapshots
- [ ] Code backups (git)

### Recovery Procedures
1. S3 bucket lost → Restore from replica (5 min)
2. DynamoDB data corruption → Restore from backup (30 min)
3. Lambda code issue → Rollback to previous version (5 min)
4. API Gateway misconfiguration → Revert serverless.yml (10 min)

## References
- Check the "References" in `docs/KNOWLEDGE.md` for Architecture Foundation, AWS Services Used and Best Practices

