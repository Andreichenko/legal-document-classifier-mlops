# Docker Setup for Legal Document Classifier

## 🐳 Docker Configuration

This directory contains Docker configuration files for containerizing the Legal Document Classifier API.

## 📁 Files

- `Dockerfile` - Main Docker image definition
- `docker-compose.yml` - Multi-container setup for development
- `build_and_run.sh` - Automated build and run script

## 🚀 Quick Start

### Prerequisites

1. **Install Docker Desktop** (if not already installed):
   - **macOS**: Download from [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - **Windows**: Download from [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - **Linux**: Follow [Docker Engine installation](https://docs.docker.com/engine/install/)

2. **Verify Docker installation**:
   ```bash
   docker --version
   docker-compose --version
   ```

### Building and Running

#### Option 1: Using the automated script
```bash
# Make script executable (if needed)
chmod +x docker/build_and_run.sh

# Run the script
./docker/build_and_run.sh
```

#### Option 2: Manual Docker build
```bash
# Build the Docker image
docker build -f docker/Dockerfile -t legal-classifier:latest .

# Run the container
docker run -d \
  --name legal-classifier-api \
  -p 8000:8000 \
  legal-classifier:latest
```

#### Option 3: Using Docker Compose
```bash
# Navigate to docker directory
cd docker

# Start services
docker-compose up -d

# View logs
docker-compose logs -f legal-classifier-api
```

## 🧪 Testing the Containerized API

Once the container is running, test the API:

```bash
# Health check
curl http://localhost:8000/health

# Test classification
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "Office space rental agreement"}'

# View API documentation
open http://localhost:8000/docs
```

## 📊 Container Management

### View running containers
```bash
docker ps
```

### View container logs
```bash
docker logs legal-classifier-api
```

### Stop the container
```bash
docker stop legal-classifier-api
```

### Remove the container
```bash
docker rm legal-classifier-api
```

### Remove the image
```bash
docker rmi legal-classifier:latest
```

## 🔧 Docker Configuration Details

### Dockerfile Features
- **Base Image**: Python 3.9-slim for smaller size
- **Security**: Non-root user for running the application
- **Health Check**: Automatic health monitoring
- **Optimization**: Multi-stage build for efficiency

### Environment Variables
- `PYTHONDONTWRITEBYTECODE=1` - Prevents Python from writing bytecode
- `PYTHONUNBUFFERED=1` - Ensures Python output is sent straight to terminal
- `PYTHONPATH=/app` - Sets Python path for imports

### Ports
- **8000**: API service port

### Volumes (Development)
- `../src:/app/src:ro` - Mount source code for development
- `../data:/app/data:ro` - Mount data files

## 🚀 Production Deployment

For production deployment, consider:

1. **Environment Variables**: Set production-specific variables
2. **Secrets Management**: Use Docker secrets or external secret management
3. **Logging**: Configure proper logging to stdout/stderr
4. **Monitoring**: Add monitoring and alerting
5. **Security**: Regular security updates and vulnerability scanning

## 🔍 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Check what's using port 8000
   lsof -i :8000
   
   # Use different port
   docker run -p 8001:8000 legal-classifier:latest
   ```

2. **Permission denied**:
   ```bash
   # Fix file permissions
   chmod +x docker/build_and_run.sh
   ```

3. **Container fails to start**:
   ```bash
   # Check container logs
   docker logs legal-classifier-api
   
   # Run interactively for debugging
   docker run -it legal-classifier:latest /bin/bash
   ```

4. **Model not found**:
   - Ensure model files are in the correct location
   - Check file permissions in the container

## 📈 Performance Optimization

- **Image Size**: Uses slim base image to reduce size
- **Layer Caching**: Requirements installed before copying code
- **Multi-stage Build**: Can be extended for production optimization
- **Health Checks**: Automatic monitoring of container health 