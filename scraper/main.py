# scraper/main.py

from ncsu_scraper         import NCSUScraper
from unc_scraper         import UNCScraper
from duke_scraper        import DukeScraper
from holiday_scraper     import HolidayScraper
from raleigh_ics_scraper import RaleighICSScraper
from raleigh_scraper     import RaleighCityScraper
from ncdot_scraper       import NCDOTScraper
from ncdhhs_scraper      import NCDHHSScraper
from nccommerce_scraper  import NCCommerceScraper
from lmi_tuesdays_scraper import LMITuesdaysScraper
from durham_scraper import DurhamCityScraper
from cms_html_scraper import CMSHTMLScraper
from cary_scraper import CaryCityScraper

if __name__ == "__main__":
    print("🚀 Starting EventPulse NC Scraper")
    print("=" * 50)
    
    # Government departments
    print("\n🏛️ Government Events")
    print("-" * 20)
    
    print("🔎 NCDOT Events")
    NCDOTScraper().run_and_post()

    print("🔎 NC DHHS Events")
    NCDHHSScraper().run_and_post()

    print("🔎 NC Commerce Events")
    NCCommerceScraper().run_and_post()

    # Municipalities
    print("\n🏙️ Municipal Events")
    print("-" * 20)
    
    print("🔎 Durham City Events")
    DurhamCityScraper().run_and_post()

    print("🔎 Cary City Events")
    CaryCityScraper().run_and_post()

    print("🔎 Raleigh City Events (HTML)")
    RaleighCityScraper().run_and_post()

    # Special Events
    print("\n🎯 Special Events")
    print("-" * 20)
    
    print("🔎 LMI Tuesdays Events")
    LMITuesdaysScraper().run_and_post()

    print("🔎 CMS Events")
    CMSHTMLScraper().run_and_post()

    # Universities & holidays
    print("\n🎓 Academic Events")
    print("-" * 20)
    
    print("🔎 NC State University (HTML)")
    NCSUScraper().run_and_post()

    print("🔎 UNC Chapel Hill (HTML)")
    UNCScraper().run_and_post()

    print("🔎 Duke University (HTML)")
    DukeScraper().run_and_post()

    print("🔎 US Holidays")
    HolidayScraper().run_and_post()

    # ICS Feeds
    print("\n📅 ICS Calendar Feeds")
    print("-" * 20)
    
    print("🔎 City of Raleigh (ICS)")
    RaleighICSScraper().run_and_post()

    print("\n✅ Scraping completed!")
    print("=" * 50)