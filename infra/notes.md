# Infrastructure Notes

## CloudFormation

TODO: Create CloudFormation templates for:
1. S3 Bucket (file storage, versioning, lifecycle)
2. DynamoDB Tables (metadata, rate limits)
3. SQS Queue (delayed deletion)
4. IAM Roles and Policies
5. API Gateway

## Deployment Checklist

- [ ] Test serverless framework deployment locally
- [ ] Create AWS account and IAM user
- [ ] Configure AWS credentials
- [ ] Deploy to dev environment
- [ ] Run integration tests
- [ ] Deploy to production
- [ ] Set up monitoring and alerts
- [ ] Configure backups
- [ ] Set up CI/CD pipeline

## Cost Monitoring

Use AWS Cost Explorer to track:
- Lambda invocations
- DynamoDB read/write units
- S3 storage and transfers
- Data transfer costs

Set up CloudWatch alarms for unexpected spikes.

## Security

- [ ] Enable S3 block public access
- [ ] Enable DynamoDB point-in-time recovery
- [ ] Enable S3 versioning and MFA delete
- [ ] Use KMS encryption for sensitive data
- [ ] Enable CloudTrail for audit logs
- [ ] Implement WAF rules for API Gateway
- [ ] Use Secrets Manager for JWT secrets

## Disaster Recovery

- [ ] Configure S3 cross-region replication
- [ ] Set up DynamoDB backups
- [ ] Document recovery procedures
- [ ] Test recovery regularly
