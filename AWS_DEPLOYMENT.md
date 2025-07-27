# 🚀 AWS Deployment Guide

## Pluralsight/ACloudGuru Sandbox Setup

This guide will help you deploy the Legal Document Classifier to AWS using Pluralsight sandbox.

## 📋 Prerequisites

1. **Pluralsight Sandbox Access**
   - Access to Pluralsight/ACloudGuru sandbox
   - AWS credentials (Access Key ID, Secret Access Key)
   - Region: `us-west-2`

2. **Local Tools**
   - AWS CLI
   - Docker
   - Terraform
   - Git

## 🔐 Setting up GitHub Secrets

For automated deployment with GitHub Actions, you need to add these secrets to your repository:

### 1. Go to your GitHub repository
- Navigate to `Settings` → `Secrets and variables` → `Actions`

### 2. Add the following secrets:
```
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
```

### 3. How to get AWS credentials from Pluralsight:
1. Log into your Pluralsight sandbox
2. Navigate to AWS Console
3. Go to IAM → Users → Your User
4. Create Access Key
5. Copy Access Key ID and Secret Access Key

## 🚀 Deployment Options

### Option 1: Automated Deployment (GitHub Actions)

1. **Push to main branch**
   ```bash
   git add .
   git commit -m "Add AWS deployment configuration"
   git push origin main
   ```

2. **Monitor deployment**
   - Go to your GitHub repository
   - Click on `Actions` tab
   - Watch the deployment progress

3. **Get deployment URL**
   - After successful deployment, check the Actions logs
   - Look for the ALB URL in the output

### Option 2: Manual Deployment

1. **Configure AWS CLI**
   ```bash
   aws configure
   # Enter your Access Key ID
   # Enter your Secret Access Key
   # Enter region: us-west-2
   # Enter output format: json
   ```

2. **Run deployment script**
   ```bash
   ./deploy.sh sandbox
   ```

3. **Test the deployment**
   ```bash
   # Get the ALB URL from the output
   curl http://your-alb-url/health
   ```

## 🏗️ Infrastructure Components

The deployment creates:

### **Networking**
- VPC with public and private subnets
- Internet Gateway and NAT Gateway
- Security Groups for ALB and ECS tasks

### **Container Registry**
- ECR repository for Docker images
- Lifecycle policy to keep last 5 images

### **Compute**
- ECS Fargate cluster
- ECS service with load balancer
- Auto-scaling configuration

### **Load Balancing**
- Application Load Balancer (ALB)
- Target group with health checks
- HTTP listener on port 80

### **Monitoring**
- CloudWatch log group
- Container insights enabled
- Health checks configured

## 📊 Cost Estimation (Pluralsight Sandbox)

Estimated costs for 4-hour sandbox session:
- **ECR**: ~$0.10 (storage)
- **ECS Fargate**: ~$0.50 (1 task for 4 hours)
- **ALB**: ~$0.20 (4 hours)
- **NAT Gateway**: ~$0.50 (4 hours)
- **Data Transfer**: ~$0.10
- **Total**: ~$1.40 for 4 hours

## 🔧 Useful Commands

### Check deployment status
```bash
# View ECS service
aws ecs describe-services \
  --cluster legal-classifier-dev \
  --services legal-classifier-dev

# View ALB
aws elbv2 describe-load-balancers \
  --names legal-classifier-dev

# View logs
aws logs tail /ecs/legal-classifier-dev --follow
```

### Test the API
```bash
# Health check
curl http://your-alb-url/health

# Classify text
curl -X POST "http://your-alb-url/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "Office space rental agreement"}'

# View API docs
open http://your-alb-url/docs
```

### Clean up (when sandbox expires)
```bash
cd terraform
terraform destroy -auto-approve
```

## 🚨 Important Notes

1. **Sandbox Limitations**
   - 4-hour time limit
   - Limited resources
   - Auto-cleanup after expiration

2. **Security**
   - ALB is publicly accessible
   - ECS tasks run in private subnets
   - Security groups restrict access

3. **Monitoring**
   - Check CloudWatch logs for issues
   - Monitor ECS service health
   - Verify ALB health checks

## 🔍 Troubleshooting

### Common Issues

1. **ECS tasks not starting**
   ```bash
   aws ecs describe-tasks \
     --cluster legal-classifier-dev \
     --tasks $(aws ecs list-tasks --cluster legal-classifier-dev --query 'taskArns[]' --output text)
   ```

2. **ALB health checks failing**
   ```bash
   aws elbv2 describe-target-health \
     --target-group-arn $(aws elbv2 describe-target-groups --names legal-classifier-dev --query 'TargetGroups[0].TargetGroupArn' --output text)
   ```

3. **Image pull errors**
   ```bash
   aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query 'Account' --output text).dkr.ecr.us-west-2.amazonaws.com
   ```

## 📚 Next Steps

After successful deployment:

1. **Test all API endpoints**
2. **Monitor performance**
3. **Set up alerts** (if needed)
4. **Document the deployment**
5. **Plan for production deployment**

## 🎯 Production Considerations

For production deployment, consider:

1. **Security**
   - HTTPS/TLS certificates
   - WAF protection
   - Private subnets only

2. **Scalability**
   - Auto-scaling policies
   - Multiple availability zones
   - Load balancing strategies

3. **Monitoring**
   - CloudWatch dashboards
   - Custom metrics
   - Alerting rules

4. **Cost Optimization**
   - Reserved instances
   - Spot instances
   - Resource tagging 