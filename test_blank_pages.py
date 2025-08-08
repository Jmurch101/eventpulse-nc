#!/usr/bin/env python3
"""
Test Blank Pages Issue
Diagnose why pages are blank when clicking links
"""

import requests
import json
from datetime import datetime

def test_blank_pages():
    """Test why pages are blank when clicking links"""
    print("🔍 Testing Blank Pages Issue")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: Check if React is mounting on different routes
    routes_to_test = [
        "/",
        "/analytics", 
        "/calendar"
    ]
    
    for route in routes_to_test:
        print(f"🔍 Testing route: {route}")
        try:
            response = requests.get(f"http://localhost:3000{route}", timeout=10)
            if response.status_code == 200:
                html_content = response.text
                
                # Check if React is mounting
                if '<div id="root"></div>' in html_content:
                    print(f"❌ Route {route}: React not mounting (empty root div)")
                elif '<div id="root">' in html_content and '</div>' in html_content:
                    print(f"✅ Route {route}: React is mounting")
                    
                    # Check for specific content
                    if 'EventPulse NC' in html_content:
                        print(f"✅ Route {route}: Dashboard content found")
                    elif 'Analytics' in html_content:
                        print(f"✅ Route {route}: Analytics content found")
                    elif 'Event Calendar' in html_content:
                        print(f"✅ Route {route}: Calendar content found")
                    else:
                        print(f"⚠️ Route {route}: Content not found")
                        
                else:
                    print(f"❓ Route {route}: React mounting status unclear")
                    
            else:
                print(f"❌ Route {route}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Route {route}: Error - {e}")
        
        print()
    
    # Test 2: Check for JavaScript errors in bundle
    print("🔍 Checking for JavaScript errors...")
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
                
            # Check for component imports
            components_to_check = ['Analytics', 'EventCalendar', 'AnalyticsDashboard']
            for component in components_to_check:
                if component in bundle_content:
                    print(f"✅ {component} found in bundle")
                else:
                    print(f"❌ {component} not found in bundle")
                    
        else:
            print(f"❌ Cannot access bundle.js: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking bundle.js: {e}")
    
    print()
    print("📋 DIAGNOSIS SUMMARY:")
    print("=" * 50)
    print("🎯 The issue is likely one of these:")
    print("1. JavaScript errors preventing component rendering")
    print("2. Missing dependencies (react-big-calendar, date-fns, etc.)")
    print("3. Component import/export issues")
    print("4. Browser caching the old JavaScript")
    print()
    print("🔧 IMMEDIATE FIXES TO TRY:")
    print("1. Open browser developer tools (F12)")
    print("2. Check Console tab for red error messages")
    print("3. Hard refresh browser (Ctrl+Shift+R)")
    print("4. Try incognito/private window")
    print("5. Check if all npm packages are installed")
    print()
    print("💡 SPECIFIC CHECKS:")
    print("• Analytics page might need react-big-calendar dependency")
    print("• EventCalendar might need date-fns dependency")
    print("• Check if all Heroicons are properly imported")
    print("• Verify all component files are properly exported")

if __name__ == "__main__":
    test_blank_pages() 