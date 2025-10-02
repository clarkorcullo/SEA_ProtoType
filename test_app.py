#!/usr/bin/env python3
"""
Test script to debug the 500 error
"""
import traceback
import sys

try:
    print("Importing app...")
    from app import app
    print("App imported successfully")
    
    print("Testing app configuration...")
    print(f"Debug mode: {app.config.get('DEBUG')}")
    print(f"Environment: {app.config.get('FLASK_ENV')}")
    
    print("Testing database connection...")
    from app import db
    with app.app_context():
        db.session.execute(db.text("SELECT 1"))
    print("Database connection successful")
    
    print("Testing health endpoint...")
    with app.test_client() as client:
        response = client.get('/health')
        print(f"Health endpoint status: {response.status_code}")
        if response.status_code == 200:
            print(f"Health response: {response.get_json()}")
        else:
            print(f"Health error: {response.data}")
    
    print("Testing index endpoint...")
    with app.test_client() as client:
        response = client.get('/')
        print(f"Index endpoint status: {response.status_code}")
        if response.status_code != 200:
            print(f"Index error: {response.data}")
    
except Exception as e:
    print(f"Error occurred: {e}")
    traceback.print_exc()
    sys.exit(1)
