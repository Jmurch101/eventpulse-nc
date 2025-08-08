#!/usr/bin/env python3
"""
Test to check current icon sizes and identify the large magnifying glass
"""

import requests
import json
from datetime import datetime

def test_frontend_current_state():
    """Test current frontend state to identify icon issues"""
    print("🔍 Testing current frontend state...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            
            # Check if there are any large icons in the HTML
            html_content = response.text.lower()
            
            # Look for potential icon-related issues
            if 'magnifyingglassicon' in html_content:
                print("⚠️ Found MagnifyingGlassIcon in HTML")
            
            if 'h-1 w-1' in html_content:
                print("✅ Found h-1 w-1 classes (small icons)")
            
            if 'h-2 w-2' in html_content:
                print("⚠️ Found h-2 w-2 classes")
            
            if 'h-3 w-3' in html_content:
                print("⚠️ Found h-3 w-3 classes")
            
            if 'h-4 w-4' in html_content:
                print("⚠️ Found h-4 w-4 classes")
            
            if 'h-5 w-5' in html_content:
                print("⚠️ Found h-5 w-5 classes")
            
            if 'h-6 w-6' in html_content:
                print("❌ Found h-6 w-6 classes (large icons)")
            
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend not accessible: {e}")
        return False

def test_backend_api():
    """Test if backend API is working"""
    print("🔍 Testing backend API...")
    
    try:
        response = requests.get("http://localhost:3001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is working")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("🔍 ICON SIZE DIAGNOSTIC TEST")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test backend
    backend_ok = test_backend_api()
    print()
    
    # Test frontend
    frontend_ok = test_frontend_current_state()
    print()
    
    # Summary
    print("=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    
    if backend_ok and frontend_ok:
        print("✅ Both backend and frontend are running")
        print("🔍 Check the browser for the large magnifying glass icon")
        print("💡 The icon might be cached - try hard refresh (Ctrl+F5)")
    else:
        print("❌ Some services are not running properly")
    
    print()
    print("🎯 NEXT STEPS:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Right-click on the large magnifying glass icon")
    print("3. Select 'Inspect Element' to see the HTML")
    print("4. Check the CSS classes to identify the size")
    print("5. Hard refresh the page (Ctrl+F5 or Cmd+Shift+R)")

if __name__ == "__main__":
    main() 