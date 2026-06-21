# Legal Document Classifier - MLOps Project

## 🎯 Project Overview

This project demonstrates a complete MLOps pipeline for a legal document classification service. It includes:

- **ML Model**: Text classification for legal documents (contracts, lawsuits, complaints, requests)
- **API Service**: FastAPI-based REST API for document classification
- **Containerization**: Docker containerization for deployment
- **Infrastructure**: AWS ECS deployment with Terraform
- **CI/CD**: GitHub Actions pipeline
- **Monitoring**: CloudWatch integration and health checks

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │───▶│   FastAPI API   │───▶│   ML Model      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Docker        │
                       │   Container     │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   AWS ECS       │
                       │   (Fargate)     │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   CloudWatch    │
                       │   Monitoring    │
                       └─────────────────┘
```

## 📁 Project Structure

```
legal-document-classifier-mlops/
├── src/                    # Source code
│   ├── main.py            # FastAPI application
│   ├── train_model.py     # ML model training
│   └── prepare_data.py    # Data preparation
├── data/                   # Data files
│   └── training_data.csv  # Training dataset
├── docker/                 # Docker configuration
│   ├── Dockerfile         # Container definition
│   └── docker-compose.yml # Local development
├── aws/                    # AWS configuration
│   └── task-definition.json
├── terraform/              # Infrastructure as Code
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── test/                   # Tests
│   └── load_test.py       # Load testing
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker
- AWS CLI configured
- Terraform

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd legal-document-classifier-mlops
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare data and train model**
   ```bash
   python src/prepare_data.py
   python src/train_model.py
   ```

5. **Run API locally**
   ```bash
   python src/main.py
   ```

6. **Test the API**
   ```bash
   curl -X POST "http://localhost:8000/classify" \
        -H "Content-Type: application/json" \
        -d '{"text": "Договор поставки товаров"}'
   ```

### Docker Development

#### Option 1: Using Docker Compose
```bash
cd docker
docker-compose up --build
```

#### Option 2: Using automated script
```bash
./docker/build_and_run.sh
```

#### Option 3: Manual Docker build
```bash
# Build the image
docker build -f docker/Dockerfile -t legal-classifier:latest .

# Run the container
docker run -d --name legal-classifier-api -p 8000:8000 legal-classifier:latest
```

For detailed Docker instructions, see [docker/README.md](docker/README.md).

## 🏗️ Infrastructure Deployment

### Using Terraform

1. **Initialize Terraform**
   ```bash
   cd terraform
   terraform init
   ```

2. **Deploy infrastructure**
   ```bash
   terraform plan
   terraform apply
   ```

3. **Deploy application**
   ```bash
   ./deploy.sh
   ```

## 📊 API Documentation

Once the API is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /classify` - Classify document text
- `GET /categories` - Get available categories

## 🧪 Testing

### Unit Tests
```bash
pytest test/
```

### Load Testing
```bash
python test/load_test.py
```

## 📈 Monitoring

- **Prometheus Metrics**: Available at `/metrics` endpoint, exposing HTTP request statistics (rates, latencies, status codes) and system/Python runtime metrics.
- **CloudWatch Logs**: Application logs
- **CloudWatch Metrics**: Performance metrics
- **Health Checks**: Automatic health monitoring

## 🔧 Configuration

Environment variables:
- `LOG_LEVEL`: Logging level (INFO, DEBUG, ERROR)
- `AWS_REGION`: AWS region for deployment
- `MODEL_PATH`: Path to the ML model file

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For questions and support, please open an issue in the GitHub repository. 