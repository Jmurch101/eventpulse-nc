#!/usr/bin/env python3
"""
Script to help identify what might be causing a 135x135 pixel image issue
"""

import requests
import json
from datetime import datetime

def test_frontend_accessibility():
    """Test if frontend is accessible"""
    print("🔍 Testing frontend accessibility...")
    
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

def analyze_events_data():
    """Analyze events data to see if there are any image-related issues"""
    print("🔍 Analyzing events data...")
    
    try:
        response = requests.get("http://localhost:3001/api/events?limit=5", timeout=10)
        if response.status_code == 200:
            events = response.json()
            print(f"✅ Retrieved {len(events)} events")
            
            # Check for any image-related fields
            for i, event in enumerate(events[:3]):
                print(f"\n📅 Event {i+1}: {event.get('title', 'No title')}")
                print(f"   Type: {event.get('event_type', 'No type')}")
                print(f"   Date: {event.get('start_date', 'No date')}")
                
                # Check for any fields that might contain image data
                for key, value in event.items():
                    if isinstance(value, str) and ('image' in key.lower() or 'icon' in key.lower()):
                        print(f"   {key}: {value[:100]}...")
                        
        else:
            print(f"❌ Failed to get events: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error analyzing events: {e}")
        return False

def check_for_icon_issues():
    """Check for potential icon-related issues"""
    print("🔍 Checking for icon-related issues...")
    
    # Common icon sizes that might be causing issues
    icon_sizes = [
        "h-1 w-1", "h-2 w-2", "h-3 w-3", "h-4 w-4", "h-5 w-5", "h-6 w-6",
        "h-8 w-8", "h-10 w-10", "h-12 w-12", "h-16 w-16", "h-20 w-20",
        "h-24 w-24", "h-32 w-32", "h-40 w-40", "h-48 w-48"
    ]
    
    print("📋 Common icon size classes to check:")
    for size in icon_sizes:
        print(f"   {size}")
    
    print("\n💡 If you're seeing a 135x135 image, it might be:")
    print("   1. An emoji that's being rendered too large")
    print("   2. An SVG icon with custom dimensions")
    print("   3. An image element with inline styles")
    print("   4. A CSS class that's not being applied correctly")
    print("   5. A browser default rendering issue")

def main():
    """Main function to run all tests"""
    print("🔍 Finding 135x135 Image Issue")
    print("=" * 50)
    
    # Test basic functionality
    frontend_ok = test_frontend_accessibility()
    backend_ok = test_backend_api()
    
    if frontend_ok and backend_ok:
        print("\n✅ Both frontend and backend are running")
        
        # Analyze data
        analyze_events_data()
        
        # Check for icon issues
        check_for_icon_issues()
        
        print("\n🎯 Next Steps:")
        print("   1. Open browser developer tools (F12)")
        print("   2. Inspect the 135x135 element")
        print("   3. Check the element's CSS classes and inline styles")
        print("   4. Look for any image, svg, or emoji elements")
        print("   5. Check if it's a Heroicon, emoji, or custom image")
        
    else:
        print("\n❌ Cannot proceed - services not available")
        print("   Please ensure both frontend and backend are running")

if __name__ == "__main__":
    main() 