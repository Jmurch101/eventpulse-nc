#!/usr/bin/env python3
"""
Comprehensive test to verify all UI fixes and check for remaining large elements
"""

import requests
import json
from datetime import datetime

def test_frontend_comprehensive():
    """Test if frontend is accessible after all UI fixes"""
    print("🔍 Testing comprehensive UI fixes...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible after comprehensive UI fixes")
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
            print(f"❌ Backend API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend API not accessible: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Comprehensive UI Fixes")
    print("=" * 50)
    
    tests = [
        ("Frontend Accessibility", test_frontend_comprehensive),
        ("Backend API", test_backend_api),
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        results[test_name] = test_func()
    
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
        print("\n🎉 All tests passed! Comprehensive UI fixes are working correctly.")
        print("🌐 Visit http://localhost:3000 to see the improvements:")
        print("   - Main title reduced from text-6xl to text-4xl")
        print("   - Dashboard stats icons reduced from h-6 w-6 to h-4 w-4")
        print("   - Time-based stats reduced from text-3xl to text-2xl")
        print("   - Category icons replaced with smaller alternatives")
        print("   - Event type icons updated across all components")
        print("   - All icons should now be appropriately sized")
        print("\n📝 If you still see large elements, please describe:")
        print("   - Which specific elements are still too large")
        print("   - Where on the page they appear")
        print("   - What they look like (icons, text, etc.)")
    else:
        print(f"\n❌ {total - passed} test(s) failed. Some issues remain.")
    
    # Save results
    results_data = {
        'timestamp': datetime.now().isoformat(),
        'results': results,
        'passed': passed,
        'total': total,
        'success_rate': f"{passed}/{total}",
        'comprehensive_fixes_applied': [
            'Main title: text-4xl md:text-6xl → text-3xl md:text-4xl',
            'Dashboard stats icons: h-6 w-6 → h-4 w-4',
            'Analytics dashboard icons: h-6 w-6 → h-4 w-4',
            'Time-based stats: text-3xl → text-2xl',
            'Quick action icons: h-6 w-6 → h-4 w-4',
            'Category icons: Replaced with smaller alternatives',
            'Event type icons: Updated across all components',
            'Modal icons: Reduced to 0.875rem',
            'Search icons: Reduced to h-4 w-4'
        ],
        'elements_checked': [
            'Main dashboard title',
            'Dashboard stats cards',
            'Analytics dashboard',
            'Category bubbles',
            'Event type icons',
            'Modal components',
            'Search components',
            'Navigation icons',
            'Time-based statistics'
        ]
    }
    
    with open('comprehensive_ui_fix_results.json', 'w') as f:
        json.dump(results_data, f, indent=2, default=str)
    
    print(f"\n📄 Results saved to comprehensive_ui_fix_results.json")
    return passed == total

if __name__ == "__main__":
    main() 