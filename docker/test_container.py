#!/usr/bin/env python3
"""
Test script for Docker containerized Legal Document Classifier API.
"""

import requests
import json
import time
import sys

def test_docker_container():
    """Test the API running in Docker container."""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Docker Containerized API")
    print("=" * 50)
    
    # Test 1: Root endpoint
    print("1. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print()
    
    # Test 2: Health check
    print("2. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        health_data = response.json()
        print(f"   Status: {health_data.get('status')}")
        print(f"   Model loaded: {health_data.get('model_loaded')}")
        print(f"   Uptime: {health_data.get('uptime', 0):.2f}s")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print()
    
    # Test 3: Categories
    print("3. Testing categories endpoint...")
    try:
        response = requests.get(f"{base_url}/categories", timeout=10)
        print(f"   Status: {response.status_code}")
        categories = response.json()
        print(f"   Available categories: {categories.get('categories', [])}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print()
    
    # Test 4: Classification
    print("4. Testing classification endpoint...")
    test_texts = [
        "Office space rental agreement",
        "Lawsuit for debt collection",
        "Complaint about poor service quality",
        "Income certificate request"
    ]
    
    for i, text in enumerate(test_texts, 1):
        try:
            payload = {"text": text}
            response = requests.post(f"{base_url}/classify", json=payload, timeout=10)
            print(f"   Test {i}: '{text}'")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   Category: {result.get('category')}")
                print(f"   Confidence: {result.get('confidence', 0):.3f}")
                print(f"   Processing time: {result.get('processing_time', 0):.3f}s")
            else:
                print(f"   ❌ Error: {response.text}")
            
            print("   " + "-" * 30)
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    print()
    print("✅ All tests completed successfully!")
    print("🎉 Docker container is working correctly!")
    
    return True

def main():
    """Main function."""
    print("🐳 Docker Container Test for Legal Document Classifier")
    print("Make sure the Docker container is running on port 8000")
    print("=" * 60)
    
    # Wait a bit for container to be ready
    print("Waiting for container to be ready...")
    time.sleep(3)
    
    success = test_docker_container()
    
    if success:
        print("\n🎯 Container test PASSED!")
        sys.exit(0)
    else:
        print("\n❌ Container test FAILED!")
        print("Check if the container is running:")
        print("  docker ps")
        print("  docker logs legal-classifier-api")
        sys.exit(1)

if __name__ == "__main__":
    main() 