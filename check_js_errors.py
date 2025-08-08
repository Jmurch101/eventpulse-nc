#!/usr/bin/env python3
"""
Check for JavaScript errors preventing React mounting
"""

import requests
import json
from datetime import datetime

def check_js_errors():
    """Check for JavaScript errors"""
    print("🔍 Checking for JavaScript errors...")
    print("=" * 50)
    
    # Check if bundle.js has any obvious errors
    try:
        response = requests.get("http://localhost:3000/static/js/bundle.js", timeout=10)
        if response.status_code == 200:
            bundle_content = response.text
            
            # Check for common error patterns
            error_patterns = [
                'SyntaxError',
                'ReferenceError', 
                'TypeError',
                'Cannot read property',
                'is not defined',
                'Unexpected token',
                'Module not found'
            ]
            
            found_errors = []
            for pattern in error_patterns:
                if pattern in bundle_content:
                    found_errors.append(pattern)
            
            if found_errors:
                print(f"⚠️ Found potential error patterns: {found_errors}")
            else:
                print("✅ No obvious error patterns found in bundle")
                
            # Check for React mounting issues
            if 'ReactDOM.render' in bundle_content or 'createRoot' in bundle_content:
                print("✅ React mounting code found in bundle")
            else:
                print("❌ React mounting code not found in bundle")
                
        else:
            print(f"❌ Cannot access bundle.js: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking bundle.js: {e}")
    
    # Check if there are any network errors
    print("\n🔍 Checking for network issues...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            html_content = response.text
            
            # Check for missing resources
            if 'bundle.js' in html_content:
                print("✅ bundle.js referenced in HTML")
            else:
                print("❌ bundle.js not referenced in HTML")
                
            if 'static/css' in html_content:
                print("✅ CSS files referenced in HTML")
            else:
                print("⚠️ CSS files not found in HTML")
                
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking frontend: {e}")
    
    # Check backend API
    print("\n🔍 Checking backend API...")
    
    try:
        response = requests.get("http://localhost:3001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check passed")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Backend error: {e}")
    
    # Check events API
    try:
        response = requests.get("http://localhost:3001/api/events?limit=1", timeout=10)
        if response.status_code == 200:
            events = response.json()
            print(f"✅ Events API working (found {len(events)} events)")
        else:
            print(f"❌ Events API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Events API error: {e}")

def main():
    """Main function"""
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    check_js_errors()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    print("🎯 The issue is React not mounting due to a JavaScript error.")
    print("💡 To fix this:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Press F12 to open Developer Tools")
    print("3. Look at the Console tab for red error messages")
    print("4. The error message will tell us exactly what's wrong")
    print("5. Common causes:")
    print("   - Missing dependencies")
    print("   - Import/export errors")
    print("   - TypeScript compilation errors")
    print("   - Browser compatibility issues")
    print()
    print("🔧 Quick fixes to try:")
    print("1. Hard refresh browser (Ctrl+Shift+R)")
    print("2. Clear browser cache")
    print("3. Restart frontend: cd frontend && npm start")
    print("4. Check if all npm packages are installed: npm install")

if __name__ == "__main__":
    main() 