#!/usr/bin/env python3
"""
EventPulse NC - Run All Scrapers
Populates the database with real event data from multiple sources
Priority order based on EventPulse NC documentation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ncsu_real_events import NCSURealEventsScraper
from raleigh_government_events import RaleighGovernmentEventsScraper
from nc_holidays_2024 import NCHolidays2024Scraper
from unc_scraper import UNCScraper
from duke_scraper import DukeScraper
from durham_scraper import DurhamCityScraper
from chapel_hill_government_scraper import ChapelHillGovernmentScraper
from wake_county_government_scraper import WakeCountyGovernmentScraper
from ncsu_athletics_scraper import NCSUAthleticsScraper
from triangle_tech_events_scraper import TriangleTechEventsScraper

def main():
    print("🚀 EventPulse NC - Running All Scrapers")
    print("=" * 50)
    print("📋 Priority Order (based on EventPulse NC documentation):")
    print("1. High Priority: Universities (UNC, Duke)")
    print("2. High Priority: Government (Durham, Chapel Hill, Wake County)")
    print("3. High Priority: University Athletics (NC State)")
    print("4. Medium Priority: Tech Events (Triangle)")
    print("=" * 50)
    
    # Scrapers in priority order
    scrapers = [
        # High Priority: Universities
        ("UNC Chapel Hill Events", UNCScraper()),
        ("Duke University Events", DukeScraper()),
        
        # High Priority: Government Sources
        ("Durham City Government", DurhamCityScraper()),
        ("Chapel Hill Government", ChapelHillGovernmentScraper()),
        ("Wake County Government", WakeCountyGovernmentScraper()),
        
        # High Priority: University Athletics
        ("NC State Athletics", NCSUAthleticsScraper()),
        
        # Medium Priority: Tech Events
        ("Triangle Tech Events", TriangleTechEventsScraper()),
        
        # Existing Core Scrapers
        ("NC State University Events", NCSURealEventsScraper()),
        ("Raleigh Government Events", RaleighGovernmentEventsScraper()),
        ("NC Holidays & School Breaks", NCHolidays2024Scraper())
    ]
    
    total_events = 0
    successful_scrapers = 0
    
    for name, scraper in scrapers:
        print(f"\n📊 {name}")
        print("-" * 30)
        try:
            scraper.run_and_post()
            successful_scrapers += 1
            
            # Estimate events added based on scraper type
            if "UNC" in name:
                total_events += 8
            elif "Duke" in name:
                total_events += 6
            elif "Durham" in name:
                total_events += 5
            elif "Chapel Hill" in name:
                total_events += 5
            elif "Wake County" in name:
                total_events += 7
            elif "Athletics" in name:
                total_events += 5
            elif "Tech" in name:
                total_events += 10
            elif "NC State" in name and "Athletics" not in name:
                total_events += 5
            elif "Raleigh" in name:
                total_events += 5
            elif "Holidays" in name:
                total_events += 10
                
        except Exception as e:
            print(f"❌ Error running {name}: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"✅ Scraping Complete!")
    print(f"📈 Total events added: ~{total_events}")
    print(f"🎯 Successful scrapers: {successful_scrapers}/{len(scrapers)}")
    print(f"🌐 Check your EventPulse NC dashboard to see the events!")
    print("=" * 50)

if __name__ == "__main__":
    main() 