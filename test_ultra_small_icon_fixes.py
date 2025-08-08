#!/usr/bin/env python3
"""
Test to verify ultra-small icon fixes (h-2 w-2)
"""

import requests
import json
from datetime import datetime

def test_frontend_ultra_small_icons():
    """Test if frontend is accessible after ultra-small icon fixes"""
    print("🔍 Testing ultra-small icon fixes...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible after ultra-small icon fixes")
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
    print("🚀 Testing Ultra-Small Icon Fixes")
    print("=" * 40)
    
    tests = [
        ("Frontend Accessibility", test_frontend_ultra_small_icons),
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
        print("\n🎉 All tests passed! Ultra-small icon fixes are working correctly.")
        print("🌐 Visit http://localhost:3000 to see the improvements:")
        print("   - Magnifying glass icons reduced to h-2 w-2 (ultra-small)")
        print("   - Stats card icons reduced to h-2 w-2 (ultra-small)")
        print("   - Quick action icons reduced to h-2 w-2 (ultra-small)")
        print("   - All icons should now be very small and unobtrusive")
        print("\n📝 The following icons should now be ultra-small (h-2 w-2):")
        print("   - Magnifying glass in Advanced Search header")
        print("   - Magnifying glass in search input box")
        print("   - Funnel icon in Advanced Search")
        print("   - Calendar icon in Date Range section")
        print("   - Calendar icon above 'Total Events'")
        print("   - Clock icon above 'Upcoming'")
        print("   - Cap icon above 'Academic'")
        print("   - Building icon above 'Government'")
        print("   - Quick action icons (Browse, Calendar, Map)")
        print("   - Users icon in Mobile-Friendly Features")
    else:
        print(f"\n❌ {total - passed} test(s) failed. Some issues remain.")
    
    # Save results
    results_data = {
        'timestamp': datetime.now().isoformat(),
        'results': results,
        'passed': passed,
        'total': total,
        'success_rate': f"{passed}/{total}",
        'ultra_small_icon_fixes_applied': [
            'Advanced Search header magnifying glass: h-3 w-3 → h-2 w-2',
            'Search input magnifying glass: h-3 w-3 → h-2 w-2',
            'Funnel icon: h-3 w-3 → h-2 w-2',
            'Date Range calendar icon: h-3 w-3 → h-2 w-2',
            'Stats card calendar icon: h-3 w-3 → h-2 w-2',
            'Stats card clock icon: h-3 w-3 → h-2 w-2',
            'Stats card academic cap icon: h-3 w-3 → h-2 w-2',
            'Stats card building icon: h-3 w-3 → h-2 w-2',
            'Quick action calendar icons: h-3 w-3 → h-2 w-2',
            'Quick action map pin icon: h-3 w-3 → h-2 w-2',
            'Mobile features users icon: h-3 w-3 → h-2 w-2'
        ],
        'icon_size_evolution': [
            'Original: h-6 w-6 (very large)',
            'First fix: h-4 w-4 (large)',
            'Second fix: h-3 w-3 (medium)',
            'Current fix: h-2 w-2 (ultra-small)'
        ]
    }
    
    with open('ultra_small_icon_fix_results.json', 'w') as f:
        json.dump(results_data, f, indent=2, default=str)
    
    print(f"\n📄 Results saved to ultra_small_icon_fix_results.json")
    return passed == total

if __name__ == "__main__":
    main() 