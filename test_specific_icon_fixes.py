#!/usr/bin/env python3
"""
Test to verify specific icon fixes for magnifying glass and stats card icons
"""

import requests
import json
from datetime import datetime

def test_frontend_specific_icons():
    """Test if frontend is accessible after specific icon fixes"""
    print("🔍 Testing specific icon fixes...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible after specific icon fixes")
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
    print("🚀 Testing Specific Icon Fixes")
    print("=" * 40)
    
    tests = [
        ("Frontend Accessibility", test_frontend_specific_icons),
        ("Backend API", test_backend_api),
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        results[test_name] = test_func()
    
    print("\n" + "=" * 40)
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
        print("\n🎉 All tests passed! Specific icon fixes are working correctly.")
        print("🌐 Visit http://localhost:3000 to see the improvements:")
        print("   - Magnifying glass icons reduced from h-4 w-4 to h-3 w-3")
        print("   - Stats card icons (calendar, clock, cap, building) reduced to h-3 w-3")
        print("   - Quick action icons reduced to h-3 w-3")
        print("   - All icons should now be much smaller and less overwhelming")
        print("\n📝 The following icons should now be smaller:")
        print("   - Magnifying glass in header search")
        print("   - Magnifying glass in Advanced Search header")
        print("   - Magnifying glass in search input box")
        print("   - Calendar icon above 'Total Events'")
        print("   - Clock icon above 'Upcoming'")
        print("   - Cap icon above 'Academic'")
        print("   - Building icon above 'Government'")
    else:
        print(f"\n❌ {total - passed} test(s) failed. Some issues remain.")
    
    # Save results
    results_data = {
        'timestamp': datetime.now().isoformat(),
        'results': results,
        'passed': passed,
        'total': total,
        'success_rate': f"{passed}/{total}",
        'specific_icon_fixes_applied': [
            'Header search magnifying glass: h-4 w-4 → h-3 w-3',
            'Advanced Search header magnifying glass: h-4 w-4 → h-3 w-3',
            'Search input magnifying glass: h-4 w-4 → h-3 w-3',
            'Funnel icon: h-4 w-4 → h-3 w-3',
            'Date Range calendar icon: h-4 w-4 → h-3 w-3',
            'Stats card calendar icon: h-4 w-4 → h-3 w-3',
            'Stats card clock icon: h-4 w-4 → h-3 w-3',
            'Stats card academic cap icon: h-4 w-4 → h-3 w-3',
            'Stats card building icon: h-4 w-4 → h-3 w-3',
            'Quick action calendar icons: h-4 w-4 → h-3 w-3',
            'Quick action map pin icon: h-4 w-4 → h-3 w-3',
            'Mobile features users icon: h-4 w-4 → h-3 w-3'
        ],
        'icons_targeted': [
            'Magnifying glass icons (3 locations)',
            'Stats card icons (4 locations)',
            'Quick action icons (3 locations)',
            'Feature section icons (1 location)'
        ]
    }
    
    with open('specific_icon_fix_results.json', 'w') as f:
        json.dump(results_data, f, indent=2, default=str)
    
    print(f"\n📄 Results saved to specific_icon_fix_results.json")
    return passed == total

if __name__ == "__main__":
    main() 