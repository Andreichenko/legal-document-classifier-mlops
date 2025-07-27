#!/bin/bash

# Deployment script for Legal Document Classifier to AWS
# Usage: ./deploy.sh [sandbox|prod]

set -e

ENVIRONMENT=${1:-sandbox}
AWS_REGION="us-west-2"
PROJECT_NAME="legal-classifier"

echo "🚀 Deploying Legal Document Classifier to AWS ($ENVIRONMENT)"
echo "=================================================="

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install it first."
    exit 1
fi

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform is not installed. Please install it first."
    exit 1
fi

# Check AWS credentials
echo "🔐 Checking AWS credentials..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run 'aws configure' first."
    exit 1
fi

echo "✅ AWS credentials configured"

# Build Docker image
echo "🐳 Building Docker image..."
docker build -f docker/Dockerfile -t $PROJECT_NAME:$ENVIRONMENT .

# Get ECR repository URL
echo "📦 Getting ECR repository URL..."
ECR_REPO=$(aws ecr describe-repositories --repository-names $PROJECT_NAME-$ENVIRONMENT --query 'repositories[0].repositoryUri' --output text 2>/dev/null || echo "")

if [ -z "$ECR_REPO" ]; then
    echo "📦 Creating ECR repository..."
    aws ecr create-repository --repository-name $PROJECT_NAME-$ENVIRONMENT --region $AWS_REGION
    ECR_REPO=$(aws ecr describe-repositories --repository-names $PROJECT_NAME-$ENVIRONMENT --query 'repositories[0].repositoryUri' --output text)
fi

echo "✅ ECR Repository: $ECR_REPO"

# Login to ECR
echo "🔑 Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO

# Tag and push image
echo "📤 Tagging and pushing image..."
docker tag $PROJECT_NAME:$ENVIRONMENT $ECR_REPO:latest
docker tag $PROJECT_NAME:$ENVIRONMENT $ECR_REPO:$(date +%Y%m%d-%H%M%S)
docker push $ECR_REPO:latest
docker push $ECR_REPO:$(date +%Y%m%d-%H%M%S)

echo "✅ Image pushed to ECR"

# Deploy infrastructure with Terraform
echo "🏗️ Deploying infrastructure with Terraform..."
cd terraform

# Initialize Terraform
echo "📋 Initializing Terraform..."
terraform init

# Plan deployment
echo "📋 Planning deployment..."
terraform plan -var="environment=$ENVIRONMENT" -var="aws_region=$AWS_REGION" -out=tfplan

# Apply deployment
echo "🚀 Applying deployment..."
terraform apply tfplan

# Get outputs
echo "📊 Getting deployment outputs..."
ALB_URL=$(terraform output -raw alb_url)
API_HEALTH_URL=$(terraform output -raw api_health_url)
API_DOCS_URL=$(terraform output -raw api_docs_url)

cd ..

echo ""
echo "🎉 Deployment completed successfully!"
echo "=================================================="
echo "📊 Application Load Balancer: $ALB_URL"
echo "🏥 Health Check: $API_HEALTH_URL"
echo "📚 API Documentation: $API_DOCS_URL"
echo ""
echo "🧪 Testing the deployment..."
sleep 30

# Test the deployment
if curl -f $API_HEALTH_URL > /dev/null 2>&1; then
    echo "✅ Health check passed!"
    echo ""
    echo "🎯 Test the API:"
    echo "curl -X POST \"$ALB_URL/classify\" \\"
    echo "     -H \"Content-Type: application/json\" \\"
    echo "     -d '{\"text\": \"Office space rental agreement\"}'"
else
    echo "❌ Health check failed. Please check the logs:"
    echo "aws logs describe-log-groups --log-group-name-prefix /ecs/$PROJECT_NAME-$ENVIRONMENT"
fi

echo ""
echo "🔧 Useful commands:"
echo "  View ECS service: aws ecs describe-services --cluster $PROJECT_NAME-$ENVIRONMENT --services $PROJECT_NAME-$ENVIRONMENT"
echo "  View logs: aws logs tail /ecs/$PROJECT_NAME-$ENVIRONMENT --follow"
echo "  Destroy infrastructure: cd terraform && terraform destroy" 