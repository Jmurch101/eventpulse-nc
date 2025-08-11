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
from chapel_hill_legistar_ics import ChapelHillLegistarICSScraper
from wake_legistar_ics import WakeCountyLegistarICSScraper
from durham_ics_scraper import DurhamICSScraper
from raleigh_ics_scraper import RaleighICSScraper
from wcpss_ics_scraper import WCPSSICSScraper
from durham_agendacenter_scraper import DurhamAgendaCenterScraper
from durham_bpac_scraper import DurhamBPACScraper
from durham_cultural_advisory_scraper import DurhamCulturalAdvisoryScraper
from orange_county_legistar_ics import OrangeCountyLegistarICSScraper
from orange_county_civicplus_ics import OrangeCountyCivicPlusICSScraper
from cary_iqm2_ics import CaryIQM2ICSScraper
from durham_county_scraper import DurhamCountyScraper
from orange_county_html_scraper import OrangeCountyHTMLScraper
from carrboro_legistar_ics import CarrboroLegistarICSScraper
from chatham_county_legistar_ics import ChathamCountyLegistarICSScraper
from wfu_events_scraper import WakeForestEventsScraper
from federal_holidays_ics_scraper import FederalHolidaysICSScraper
from uncg_events_ics import UNCGEventsICSScraper
from ncdot_meetings_scraper import NCDOTMeetingsScraper
from ncdhhs_events_scraper import NCDHHSEventsScraper
from campo_calendar_scraper import CAMPOCalendarScraper
from uncc_events_ics import UNCCEventsICSScraper
from ecu_events_ics import ECUEventsICSScraper
from nc_admin_events_scraper import NCAdminEventsScraper
from uncc_html_scraper import UNCCHTMLEventsScraper
from ecu_html_scraper import ECUHTMLEventsScraper
from nc_dpi_events_scraper import NCDPIEventsScraper
from nc_deq_events_scraper import NCDEQEventsScraper
from nc_dncr_a250_events_scraper import NCDNCRAmerica250Scraper
from nc_commerce_events_scraper import NCCommerceEventsScraper
from nc_courts_appeals_scraper import NCCourtOfAppealsScraper
from nc_courts_supreme_scraper import NCSupremeCourtScraper

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
        ("Wake County Legistar (ICS)", WakeCountyLegistarICSScraper()),
        ("Chapel Hill Legistar (ICS)", ChapelHillLegistarICSScraper()),
        ("Durham City (ICS)", DurhamICSScraper()),
        ("Durham Agenda Center", DurhamAgendaCenterScraper()),
        ("Durham BPAC", DurhamBPACScraper()),
        ("Durham Cultural Advisory Board", DurhamCulturalAdvisoryScraper()),
        ("Raleigh (ICS)", RaleighICSScraper()),
        ("Orange County (Legistar ICS)", OrangeCountyLegistarICSScraper()),
        ("Orange County (CivicPlus ICS)", OrangeCountyCivicPlusICSScraper()),
        ("Orange County (HTML)", OrangeCountyHTMLScraper()),
        ("Durham County (HTML)", DurhamCountyScraper()),
        ("Carrboro (Legistar ICS)", CarrboroLegistarICSScraper()),
        ("Chatham County (Legistar ICS)", ChathamCountyLegistarICSScraper()),
        ("Wake Forest University Events", WakeForestEventsScraper()),
        ("US Federal Holidays (ICS)", FederalHolidaysICSScraper()),
        ("UNC Greensboro (ICS)", UNCGEventsICSScraper()),
        ("UNC Charlotte (ICS)", UNCCEventsICSScraper()),
        ("UNC Charlotte (HTML)", UNCCHTMLEventsScraper()),
        ("East Carolina University (ICS)", ECUEventsICSScraper()),
        ("East Carolina University (HTML)", ECUHTMLEventsScraper()),
        ("NCDOT Public Meetings (HTML)", NCDOTMeetingsScraper()),
        ("NCDHHS Events (HTML)", NCDHHSEventsScraper()),
        ("CAMPO Calendar (HTML)", CAMPOCalendarScraper()),
        ("NC Department of Administration (HTML)", NCAdminEventsScraper()),
        ("NC DPI (HTML)", NCDPIEventsScraper()),
        ("NC DEQ (HTML)", NCDEQEventsScraper()),
        ("NC DNCR America 250 (HTML)", NCDNCRAmerica250Scraper()),
        ("NC Commerce (HTML)", NCCommerceEventsScraper()),
        ("NC Courts – Court of Appeals (HTML)", NCCourtOfAppealsScraper()),
        ("NC Courts – Supreme Court (HTML)", NCSupremeCourtScraper()),
        ("Cary (IQM2 ICS)", CaryIQM2ICSScraper()),
        
        # High Priority: University Athletics
        ("NC State Athletics", NCSUAthleticsScraper()),
        
        # Medium Priority: Tech Events
        ("Triangle Tech Events", TriangleTechEventsScraper()),
        
        # Existing Core Scrapers
        ("NC State University Events", NCSURealEventsScraper()),
        ("Raleigh Government Events", RaleighGovernmentEventsScraper()),
        ("NC Holidays & School Breaks", NCHolidays2024Scraper()),
        ("WCPSS (ICS)", WCPSSICSScraper()),
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