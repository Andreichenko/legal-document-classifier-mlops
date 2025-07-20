"""
Simple test script for the Legal Document Classifier API.
"""

import requests
import json
import time

def test_api():
    """Test the API endpoints."""
    
    base_url = "http://localhost:8000"
    
    # Test 1: Root endpoint
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Health check
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: Categories
    print("Testing categories endpoint...")
    try:
        response = requests.get(f"{base_url}/categories")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 4: Classification
    print("Testing classification endpoint...")
    test_texts = [
        "Office space rental agreement",
        "Lawsuit for debt collection",
        "Complaint about poor service quality",
        "Income certificate request"
    ]
    
    for text in test_texts:
        try:
            payload = {"text": text}
            response = requests.post(f"{base_url}/classify", json=payload)
            print(f"Text: {text}")
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            print("-" * 30)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting API tests...")
    print("Make sure the API is running on http://localhost:8000")
    print("="*50)
    
    # Wait a bit for API to start
    time.sleep(2)
    
    test_api() 