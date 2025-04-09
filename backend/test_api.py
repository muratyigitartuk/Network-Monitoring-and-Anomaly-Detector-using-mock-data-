#!/usr/bin/env python
"""
Test script for the Network Anomaly Detection API.
This script tests the basic functionality of the API.
"""

import requests
import time
import sys
import json
from datetime import datetime

# API URL
API_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_network_metrics():
    """Test the network metrics endpoint"""
    try:
        response = requests.get(f"{API_URL}/api/network/metrics/current")
        if response.status_code == 200:
            data = response.json()
            print("✅ Network metrics endpoint passed")
            print(f"   Timestamp: {data.get('timestamp')}")
            print(f"   Incoming traffic: {data.get('incoming_traffic')} Mbps")
            print(f"   Outgoing traffic: {data.get('outgoing_traffic')} Mbps")
            print(f"   Active connections: {data.get('active_connections')}")
            return True
        else:
            print(f"❌ Network metrics endpoint failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Network metrics endpoint failed: {e}")
        return False

def test_login():
    """Test the login endpoint"""
    try:
        response = requests.post(
            f"{API_URL}/api/users/token",
            data={"username": "admin", "password": "password"}
        )
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print("✅ Login endpoint passed")
            print(f"   Token: {token[:10]}...")
            return token
        else:
            print(f"❌ Login endpoint failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Login endpoint failed: {e}")
        return None

def test_user_me(token):
    """Test the user/me endpoint"""
    if not token:
        print("❌ User/me endpoint skipped: No token")
        return False
    
    try:
        response = requests.get(
            f"{API_URL}/api/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ User/me endpoint passed")
            print(f"   Username: {data.get('username')}")
            print(f"   Role: {data.get('role')}")
            return True
        else:
            print(f"❌ User/me endpoint failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ User/me endpoint failed: {e}")
        return False

def main():
    """Main function"""
    print(f"Testing API at {API_URL}")
    print(f"Time: {datetime.now().isoformat()}")
    print("-" * 50)
    
    # Test health endpoint
    if not test_health():
        print("❌ API is not healthy, aborting tests")
        return 1
    
    # Test network metrics endpoint
    test_network_metrics()
    
    # Test login endpoint
    token = test_login()
    
    # Test user/me endpoint
    test_user_me(token)
    
    print("-" * 50)
    print("Tests completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
