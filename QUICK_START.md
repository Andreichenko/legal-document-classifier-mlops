# 🚀 Quick Start Guide

## Overview

This project demonstrates a complete MLOps pipeline for a legal document classification service deployed to AWS.

## 📋 What's Included

- ✅ **ML Model**: Text classification with scikit-learn
- ✅ **API Service**: FastAPI REST API
- ✅ **Containerization**: Docker with health checks
- ✅ **Infrastructure**: AWS ECS with Terraform
- ✅ **CI/CD**: GitHub Actions automation
- ✅ **Monitoring**: CloudWatch integration

## 🎯 Quick Start (5 minutes)

### 1. Local Development

```bash
# Clone and setup
git clone <your-repo>
cd legal-document-classifier-mlops

# Install dependencies
python3 -m pip install --user -r requirements.txt

# Prepare data and train model
python3 src/prepare_data.py
python3 src/train_model.py

# Run API locally
python3 run_api.py
```

### 2. Docker Testing

```bash
# Build and run with Docker
./docker/build_and_run.sh

# Or use docker-compose
cd docker
docker-compose up --build
```

### 3. AWS Deployment

#### Option A: GitHub Actions (Recommended)
1. Add AWS secrets to GitHub repository
2. Push to main branch
3. Monitor deployment in Actions tab

#### Option B: Manual Deployment
```bash
# Configure AWS credentials
aws configure

# Deploy to Pluralsight sandbox
./deploy.sh sandbox
```

## 🔗 API Endpoints

Once deployed, your API will be available at:
- **Health Check**: `http://your-alb-url/health`
- **API Docs**: `http://your-alb-url/docs`
- **Classification**: `http://your-alb-url/classify`

## 🧪 Test the API

```bash
# Health check
curl http://your-alb-url/health

# Classify document
curl -X POST "http://your-alb-url/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "Office space rental agreement"}'
```

## 📊 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub        │───▶│   GitHub        │───▶│   AWS ECS       │
│   Repository    │    │   Actions       │    │   Fargate       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   AWS ECR       │
                       │   Docker Images │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   AWS ALB       │
                       │   Load Balancer │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   CloudWatch    │
                       │   Monitoring    │
                       └─────────────────┘
```

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.9
- **ML**: scikit-learn, TF-IDF, Naive Bayes
- **Containerization**: Docker
- **Infrastructure**: Terraform, AWS ECS, ECR, ALB
- **CI/CD**: GitHub Actions
- **Monitoring**: CloudWatch

## 📁 Project Structure

```
legal-document-classifier-mlops/
├── src/                    # Source code
│   ├── main.py            # FastAPI application
│   ├── train_model.py     # ML model training
│   └── prepare_data.py    # Data preparation
├── docker/                 # Docker configuration
│   ├── Dockerfile         # Container definition
│   ├── docker-compose.yml # Local development
│   └── build_and_run.sh   # Build script
├── terraform/              # Infrastructure as Code
│   ├── main.tf            # Main configuration
│   ├── variables.tf       # Variables
│   ├── outputs.tf         # Outputs
│   └── modules/           # Terraform modules
├── .github/workflows/      # CI/CD pipelines
│   └── deploy.yml         # Deployment workflow
├── requirements.txt        # Python dependencies
├── deploy.sh              # Manual deployment script
└── README.md              # Project documentation
```

## 🎓 Learning Outcomes

After completing this project, you'll understand:

1. **MLOps Pipeline**: End-to-end ML deployment
2. **Containerization**: Docker best practices
3. **Infrastructure as Code**: Terraform with AWS
4. **CI/CD**: Automated deployment with GitHub Actions
5. **Cloud Deployment**: AWS ECS, ECR, ALB
6. **Monitoring**: CloudWatch integration

## 🚨 Important Notes

### For Pluralsight Sandbox:
- 4-hour time limit
- Estimated cost: ~$1.40 for 4 hours
- Auto-cleanup after expiration
- Region: us-west-2

### Security:
- ALB is publicly accessible
- ECS tasks run in private subnets
- Security groups restrict access

## 🔧 Troubleshooting

### Common Issues:

1. **Docker not found**: Install Docker Desktop
2. **AWS credentials**: Run `aws configure`
3. **Terraform errors**: Check AWS permissions
4. **ECS tasks failing**: Check CloudWatch logs

### Useful Commands:

```bash
# Check deployment status
aws ecs describe-services --cluster legal-classifier-dev

# View logs
aws logs tail /ecs/legal-classifier-dev --follow

# Destroy infrastructure
cd terraform && terraform destroy
```

## 📚 Next Steps

1. **Enhance the model** with more data
2. **Add authentication** to the API
3. **Implement auto-scaling**
4. **Add monitoring dashboards**
5. **Set up alerts and notifications**

## 🎉 Congratulations!

You've successfully built and deployed a production-ready MLOps pipeline! This demonstrates real-world skills in:

- Machine Learning deployment
- Cloud infrastructure
- DevOps practices
- API development
- Container orchestration

This project is perfect for your portfolio and demonstrates practical MLOps experience. 