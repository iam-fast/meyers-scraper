#!/usr/bin/env python3
"""
Test script for the Meyers Scraper API
"""

import requests
import json
import time
from datetime import datetime

# API base URL
API_BASE = "http://localhost:5015"

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_get_all_menus():
    """Test getting all menus."""
    print("\nTesting get all menus...")
    try:
        response = requests.get(f"{API_BASE}/api/menus", timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ Get all menus passed: {data['metadata']['total_dates']} dates found")
                return True
            else:
                print(f"❌ Get all menus failed: {data['message']}")
                return False
        else:
            print(f"❌ Get all menus failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get all menus error: {e}")
        return False

def test_get_menu_by_date():
    """Test getting menu for a specific date."""
    print("\nTesting get menu by date...")
    try:
        # Use today's date
        today = datetime.now().strftime('%Y-%m-%d')
        response = requests.get(f"{API_BASE}/api/menus/{today}", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ Get menu by date passed: Found menu for {today}")
                return True
            else:
                print(f"❌ Get menu by date failed: {data['message']}")
                return False
        elif response.status_code == 404:
            print(f"⚠️  No menu data for {today} (this might be normal)")
            return True
        else:
            print(f"❌ Get menu by date failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get menu by date error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Starting Meyers Scraper API Tests")
    print("=" * 50)
    
    # Wait a moment for API to be ready
    print("Waiting for API to be ready...")
    time.sleep(2)
    
    tests = [
        test_health_check,
        test_get_all_menus,
        test_get_menu_by_date
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API logs for more details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 