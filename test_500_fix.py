#!/usr/bin/env python3
"""
Test script to verify the 500 error is fixed
"""
import requests
import time
import sys

def test_application():
    """Test the application endpoints"""
    base_url = "http://localhost:5000"
    
    print("Testing application endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"Health endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Health response: {response.json()}")
        else:
            print(f"Health error: {response.text}")
    except Exception as e:
        print(f"Health endpoint failed: {e}")
    
    # Test index endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"Index endpoint: {response.status_code}")
        if response.status_code != 200:
            print(f"Index error: {response.text[:200]}...")
    except Exception as e:
        print(f"Index endpoint failed: {e}")
    
    # Test login endpoint
    try:
        response = requests.get(f"{base_url}/login", timeout=5)
        print(f"Login endpoint: {response.status_code}")
        if response.status_code != 200:
            print(f"Login error: {response.text[:200]}...")
    except Exception as e:
        print(f"Login endpoint failed: {e}")
    
    # Test register endpoint
    try:
        response = requests.get(f"{base_url}/register", timeout=5)
        print(f"Register endpoint: {response.status_code}")
        if response.status_code != 200:
            print(f"Register error: {response.text[:200]}...")
    except Exception as e:
        print(f"Register endpoint failed: {e}")

if __name__ == "__main__":
    print("Waiting for application to start...")
    time.sleep(2)
    test_application()
