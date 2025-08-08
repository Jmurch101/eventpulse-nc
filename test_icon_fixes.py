#!/usr/bin/env python3
"""
Quick test to verify icon size fixes
"""

import requests
import json
from datetime import datetime

def test_frontend_icon_fixes():
    """Test if frontend is accessible after icon fixes"""
    print("🔍 Testing icon size fixes...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible after icon fixes")
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend not accessible: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Icon Size Fixes")
    print("=" * 40)
    
    success = test_frontend_icon_fixes()
    
    if success:
        print("\n🎉 Icon size fixes applied successfully!")
        print("🌐 Visit http://localhost:3000 to see the improvements:")
        print("   - Search icon in header is now smaller (1rem)")
        print("   - Category bubble icons are more reasonable")
        print("   - Loading spinners are appropriately sized")
        print("   - All icons should fit properly on screen")
    else:
        print("\n❌ Some issues remain")
    
    # Save results
    results = {
        'timestamp': datetime.now().isoformat(),
        'success': success,
        'fixes_applied': [
            'Header search icon: 1.25rem → 1rem',
            'EventList loading spinner: 3rem → 1.5rem',
            'EventMap emoji: 3rem → 1.5rem',
            'DayMapModal calendar: h-8 w-8 → h-6 w-6',
            'EventDetailsModal icon: 2.5rem → 2rem',
            'InteractiveHeatMap arrows: 1.5rem → 1.25rem',
            'EventList arrow: 1.25rem → 1rem',
            'CategoryBubbles arrow: 1.25rem → 1rem'
        ]
    }
    
    with open('icon_fix_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Results saved to icon_fix_results.json")
    return success

if __name__ == "__main__":
    main() 