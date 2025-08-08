#!/usr/bin/env python3
"""
Test script to verify UI fixes for EventPulse NC
"""

import requests
import json
import time
from datetime import datetime

def test_frontend_accessibility():
    """Test if frontend is accessible"""
    print("🌐 Testing frontend accessibility...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend not accessible: {e}")
        return False

def test_backend_api():
    """Test if backend API is working"""
    print("🔧 Testing backend API...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:3001/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend health check passed")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
        
        # Test events endpoint
        response = requests.get("http://localhost:3001/api/events?limit=10", timeout=10)
        if response.status_code == 200:
            events = response.json()
            print(f"✅ Backend API returned {len(events)} events")
            return True
        else:
            print(f"❌ Backend API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Backend API error: {e}")
        return False

def test_2025_events():
    """Test if 2025 events are accessible"""
    print("📅 Testing 2025 events...")
    
    try:
        response = requests.get("http://localhost:3001/api/events?year=2025&limit=10", timeout=10)
        if response.status_code == 200:
            events = response.json()
            if events:
                print(f"✅ Found {len(events)} 2025 events")
                # Check first event date
                first_event = events[0]
                if first_event['start_date'].startswith('2025'):
                    print("✅ 2025 events have correct dates")
                    return True
                else:
                    print(f"❌ First event has wrong date: {first_event['start_date']}")
                    return False
            else:
                print("❌ No 2025 events found")
                return False
        else:
            print(f"❌ 2025 events API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 2025 events test error: {e}")
        return False

def test_ui_components():
    """Test if UI components are working"""
    print("🎨 Testing UI components...")
    
    try:
        # Get the frontend page content
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            content = response.text.lower()
            
            # Check for key UI elements
            checks = [
                ("event calendar", "calendar component"),
                ("category", "category bubbles"),
                ("search", "search functionality"),
                ("dashboard", "dashboard layout")
            ]
            
            all_present = True
            for term, description in checks:
                if term in content:
                    print(f"✅ {description} present")
                else:
                    print(f"⚠️ {description} not found")
                    all_present = False
            
            return all_present
        else:
            print(f"❌ Could not fetch frontend content: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ UI components test error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing EventPulse NC UI Fixes")
    print("=" * 50)
    
    # Run all tests
    tests = [
        ("Frontend Accessibility", test_frontend_accessibility),
        ("Backend API", test_backend_api),
        ("2025 Events", test_2025_events),
        ("UI Components", test_ui_components)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        results[test_name] = test_func()
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! UI fixes are working correctly.")
        print("🌐 Visit http://localhost:3000 to see the improvements:")
        print("   - Smaller, more reasonable icon sizes")
        print("   - Click on calendar dates to see events in modal")
        print("   - 2025 events are accessible and displayed")
    else:
        print(f"\n❌ {total - passed} test(s) failed. Some issues remain.")
    
    # Save results
    test_results = {
        'timestamp': datetime.now().isoformat(),
        'results': results,
        'passed': passed,
        'total': total,
        'success_rate': f"{passed}/{total}"
    }
    
    with open('ui_fix_test_results.json', 'w') as f:
        json.dump(test_results, f, indent=2, default=str)
    
    print(f"\n📄 Results saved to ui_fix_test_results.json")
    return passed == total

if __name__ == "__main__":
    main() 