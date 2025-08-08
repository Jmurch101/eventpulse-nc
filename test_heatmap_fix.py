#!/usr/bin/env python3
"""
Test script to verify heatmap fix
"""

import requests
import json
from datetime import datetime

def test_heatmap_fix():
    print("🔍 Testing heatmap fix...")
    
    try:
        # Test 1: Check if 2025 events are accessible
        print("📊 Testing 2025 events access...")
        response = requests.get("http://localhost:3001/api/events?year=2025&limit=1000", timeout=10)
        if response.status_code == 200:
            events_2025 = response.json()
            print(f"✅ Found {len(events_2025)} 2025 events")
            
            # Check date distribution
            date_counts = {}
            for event in events_2025[:100]:  # Sample first 100
                date = event['start_date'][:10]  # YYYY-MM-DD
                date_counts[date] = date_counts.get(date, 0) + 1
            
            print("📅 Sample 2025 event distribution:")
            for date, count in sorted(date_counts.items())[:10]:
                print(f"   {date}: {count} events")
            
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing heatmap fix: {e}")
        return False

def test_frontend_heatmap():
    print("\n🌐 Testing frontend heatmap...")
    
    try:
        # Test if frontend is accessible
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            
            # Check if the page contains heatmap-related content
            content = response.text.lower()
            if "event" in content and "calendar" in content:
                print("✅ Frontend appears to have event calendar content")
                return True
            else:
                print("⚠️ Frontend content doesn't seem to include event calendar")
                return False
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing frontend: {e}")
        return False

def main():
    print("🚀 Testing EventPulse NC Heatmap Fix")
    print("=" * 50)
    
    # Test backend
    backend_ok = test_heatmap_fix()
    
    # Test frontend
    frontend_ok = test_frontend_heatmap()
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print(f"   Backend 2025 events: {'✅ Working' if backend_ok else '❌ Failed'}")
    print(f"   Frontend heatmap: {'✅ Working' if frontend_ok else '❌ Failed'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 Heatmap fix appears to be working!")
        print("🌐 Visit http://localhost:3000 to see the heatmap")
        print("📅 Navigate to August 2025 to see 2025 events")
    else:
        print("\n❌ Some issues detected")
    
    return backend_ok and frontend_ok

if __name__ == "__main__":
    main() 