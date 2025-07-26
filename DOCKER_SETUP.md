# 🐳 Docker Setup Guide

## Quick Docker Installation

### macOS
1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
2. Install and start Docker Desktop
3. Verify installation: `docker --version`

### Windows
1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
2. Install and start Docker Desktop
3. Verify installation: `docker --version`

### Linux (Ubuntu/Debian)
```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Add user to docker group
sudo usermod -aG docker $USER

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker
```

## 🚀 Quick Start with Docker

Once Docker is installed:

```bash
# Build and run the container
./docker/build_and_run.sh

# Or manually:
docker build -f docker/Dockerfile -t legal-classifier:latest .
docker run -d --name legal-classifier-api -p 8000:8000 legal-classifier:latest

# Test the API
python3 docker/test_container.py
```

## 📚 More Information

For detailed Docker instructions, see [docker/README.md](docker/README.md). 