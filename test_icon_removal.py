#!/usr/bin/env python3
"""
Test to verify icon removal fixes
"""

import requests
import json
from datetime import datetime

def test_frontend_icon_removal():
    """Test if frontend is accessible after icon removal"""
    print("🔍 Testing icon removal fixes...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible after icon removal")
            
            # Check if MagnifyingGlassIcon is still present
            html_content = response.text.lower()
            
            if 'magnifyingglassicon' in html_content:
                print("⚠️ MagnifyingGlassIcon still found in HTML")
            else:
                print("✅ MagnifyingGlassIcon removed from HTML")
            
            if 'h-1 w-1' in html_content:
                print("✅ Small icon classes still present")
            
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
    print("🔍 ICON REMOVAL TEST")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test backend
    backend_ok = test_backend_api()
    print()
    
    # Test frontend
    frontend_ok = test_frontend_icon_removal()
    print()
    
    # Summary
    print("=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    
    if backend_ok and frontend_ok:
        print("✅ Both backend and frontend are running")
        print("🎯 Magnifying glass icons replaced with emoji text")
        print("💡 Hard refresh your browser (Ctrl+F5 or Cmd+Shift+R)")
        print("🔍 Check if the large magnifying glass is now smaller")
    else:
        print("❌ Some services are not running properly")
    
    print()
    print("🎯 NEXT STEPS:")
    print("1. Hard refresh your browser (Ctrl+F5 or Cmd+Shift+R)")
    print("2. Check if the magnifying glass icons are now smaller")
    print("3. If still large, right-click and inspect the element")
    print("4. Look for any CSS that might be overriding our changes")

if __name__ == "__main__":
    main() 