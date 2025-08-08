#!/usr/bin/env python3
"""
Test script for new EventPulse NC scrapers
Tests the high-priority scrapers added based on documentation priority
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chapel_hill_government_scraper import ChapelHillGovernmentScraper
from wake_county_government_scraper import WakeCountyGovernmentScraper
from ncsu_athletics_scraper import NCSUAthleticsScraper
from triangle_tech_events_scraper import TriangleTechEventsScraper

def test_scraper(scraper_name, scraper_instance):
    """Test a single scraper and return results"""
    print(f"\n🧪 Testing {scraper_name}")
    print("-" * 40)
    
    try:
        # Test the scraper
        events = scraper_instance.run()
        
        if events:
            print(f"✅ {scraper_name}: Found {len(events)} events")
            for i, event in enumerate(events[:3]):  # Show first 3 events
                print(f"   {i+1}. {event['title']}")
                print(f"      📅 {event['start_date']}")
                print(f"      📍 {event['location_name']}")
            return True, len(events)
        else:
            print(f"⚠️ {scraper_name}: No events found")
            return False, 0
            
    except Exception as e:
        print(f"❌ {scraper_name}: Error - {str(e)}")
        return False, 0

def main():
    print("🧪 EventPulse NC - Testing New Scrapers")
    print("=" * 50)
    print("Testing high-priority scrapers based on documentation")
    print("=" * 50)
    
    # Test scrapers
    test_scrapers = [
        ("Chapel Hill Government", ChapelHillGovernmentScraper()),
        ("Wake County Government", WakeCountyGovernmentScraper()),
        ("NC State Athletics", NCSUAthleticsScraper()),
        ("Triangle Tech Events", TriangleTechEventsScraper())
    ]
    
    results = []
    total_events = 0
    
    for name, scraper in test_scrapers:
        success, event_count = test_scraper(name, scraper)
        results.append((name, success, event_count))
        total_events += event_count
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    successful = sum(1 for _, success, _ in results if success)
    print(f"✅ Successful scrapers: {successful}/{len(test_scrapers)}")
    print(f"📈 Total events found: {total_events}")
    
    for name, success, count in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} {name}: {count} events")
    
    print("\n🎯 Next Steps:")
    if successful == len(test_scrapers):
        print("   ✅ All scrapers working! Run 'python run_all_scrapers.py' to populate database")
    else:
        print("   ⚠️ Some scrapers need debugging before running full suite")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 