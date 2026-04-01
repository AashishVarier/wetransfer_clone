#!/bin/bash
# deploy-backend.sh - Deploy backend with Serverless Framework

set -e

STAGE="${1:-dev}"
REGION="${2:-us-east-1}"

echo "═══════════════════════════════════════"
echo "  WeTransfer Clone - Backend Deploy"
echo "═══════════════════════════════════════"
echo ""
echo "Stage: $STAGE"
echo "Region: $REGION"
echo ""

# Change to backend directory
cd "$(dirname "$0")/../backend" || exit 1

# Check if serverless is installed
if ! command -v serverless &> /dev/null; then
    echo "❌ Serverless Framework not found"
    echo "   Install with: npm install -g serverless@latest"
    exit 1
fi

# Deploy using Serverless Framework
echo "🚀 Deploying Lambda functions..."
serverless deploy \
    --stage "$STAGE" \
    --region "$REGION" \
    --config serverless.yml

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Outputs:"
serverless info --stage "$STAGE" --region "$REGION"

echo ""
echo "📝 Next steps:"
echo "1. Get API URL from CloudFormation outputs"
echo "2. Update frontend: VITE_API_BASE_URL in .env.local"
echo "3. Test upload flow"
echo "4. Monitor CloudWatch logs: serverless logs -f upload --stage $STAGE --tail"
