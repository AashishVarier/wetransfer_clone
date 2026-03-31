#!/bin/bash
# deploy-frontend.sh - Deploy frontend to S3

set -e

STAGE="${1:-dev}"
REGION="${2:-us-east-1}"
BUCKET_NAME="wetransfer-clone-frontend-${STAGE}"

echo "═══════════════════════════════════════"
echo "  WeTransfer Clone - Frontend Deploy"
echo "═══════════════════════════════════════"
echo ""
echo "Stage: $STAGE"
echo "Region: $REGION"
echo "S3 Bucket: $BUCKET_NAME"
echo ""

# TODO: Implement production deployment
# 1. Verify environment
# 2. Build frontend
# 3. Sync to S3
# 4. Invalidate CloudFront cache
# 5. Verify deployment

echo "TODO: Implement S3 deployment"
echo ""
echo "Manual steps:"
echo "1. cd frontend"
echo "2. npm run build"
echo "3. aws s3 sync dist/ s3://$BUCKET_NAME/ --region $REGION --delete"
echo "4. Open: https://$BUCKET_NAME.s3.amazonaws.com/index.html"
