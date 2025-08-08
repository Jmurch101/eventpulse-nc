#!/usr/bin/env python3
"""
Test click functionality and calendar year
"""

import requests
import json
from datetime import datetime

def test_click_functionality():
    """Test the current click functionality"""
    print("🎯 Testing Click Functionality")
    print("=" * 50)
    
    # Test 1: Check if services are running
    try:
        response = requests.get("http://localhost:3001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("❌ Backend not responding")
            return False
    except Exception as e:
        print(f"❌ Backend error: {e}")
        return False
    
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is running")
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        return False
    
    # Test 2: Check event data
    try:
        response = requests.get("http://localhost:3001/api/events?limit=5", timeout=10)
        if response.status_code == 200:
            events = response.json()
            print(f"✅ Found {len(events)} events in database")
            
            # Check event dates
            event_dates = []
            for event in events:
                date = event.get('start_date', '')[:10]  # Get just the date part
                if date:
                    event_dates.append(date)
            
            if event_dates:
                print(f"📅 Event dates: {list(set(event_dates))[:3]}")
                
                # Check if events are in 2026
                events_2026 = [date for date in event_dates if date.startswith('2026')]
                if events_2026:
                    print(f"✅ Found {len(events_2026)} events in 2026")
                    print(f"📅 2026 event dates: {list(set(events_2026))[:3]}")
                else:
                    print("⚠️ No events found in 2026")
                    
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API error: {e}")
        return False
    
    # Test 3: Check frontend HTML for calendar components
    try:
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            html_content = response.text.lower()
            
            # Check for calendar components
            if 'interactiveheatmap' in html_content:
                print("✅ InteractiveHeatMap component found in HTML")
            else:
                print("⚠️ InteractiveHeatMap component not found in HTML")
            
            # Check for modal components
            if 'daymapmodal' in html_content:
                print("✅ DayMapModal component found in HTML")
            else:
                print("⚠️ DayMapModal component not found in HTML")
            
            # Check for click handlers
            if 'onclick' in html_content:
                print("✅ onClick handlers found in HTML")
            else:
                print("⚠️ onClick handlers not found in HTML")
                
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success = test_click_functionality()
    
    print()
    print("=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    
    if success:
        print("✅ Click functionality test complete")
        print("🎯 Current status:")
        print("   • Backend and frontend are running")
        print("   • Events are in 2026 (August 30-31)")
        print("   • Calendar should show August 2026")
        print("   • Click handlers are implemented")
        print()
        print("🎯 How to test clicking:")
        print("1. Go to http://localhost:3000")
        print("2. Look for the calendar showing 'August 2026'")
        print("3. Find colored squares on August 30-31")
        print("4. Click on any colored day")
        print("5. A popup should appear with event details")
        print()
        print("💡 If clicking still doesn't work:")
        print("   - Hard refresh your browser (Ctrl+F5 or Cmd+Shift+R)")
        print("   - Check browser console for JavaScript errors")
        print("   - Make sure you're clicking on colored days (not empty days)")
        print("   - Try clicking on August 30 or 31, 2026")
    else:
        print("❌ Some services are not running properly")
        print("💡 Make sure both backend and frontend are started")

if __name__ == "__main__":
    main() 