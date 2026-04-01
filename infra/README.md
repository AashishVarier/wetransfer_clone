# Infrastructure

This folder contains infrastructure-as-code (IaC) definitions for the WeTransfer Clone backend.

## CloudFormation

Contains CloudFormation templates for AWS resources:
- S3 buckets for file storage
- DynamoDB tables for metadata
- SQS queues for async tasks
- IAM roles and policies
- API Gateway configurations

## Deployment

The Serverless Framework (in `backend/serverless.yml`) handles most infrastructure, but CloudFormation templates can be used for:
- Pre-production setup
- Multi-region deployments
- Custom resource configurations

## AWS Free Tier Considerations

- DynamoDB: Use PAY_PER_REQUEST billing mode to avoid overages
- S3: Lifecycle policies auto-delete old versions after 7 days
- Lambda: Keep within 1M requests per month
- Rate limiting prevents abuse

See `../docs/KNOWLEDGE.md` for detailed information.
