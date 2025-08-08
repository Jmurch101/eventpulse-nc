# scraper/lmi_tuesdays_scraper.py

from ics_scrapers import ICSUtils
from post_event import post_event

class LMITuesdaysScraper:
    """
    Scrapes the NC Department of Commerce "LMI Tuesdays" ICS feed.
    """
    def __init__(self):
        # Replace with the actual ICS URL if known
        self.url = "https://www.nccommerce.com/LMI-Tuesdays.ics"
        self.org_id = 32
        self.org_name = "NC Department of Commerce"
        self.lat, self.lon = 35.771, -78.638
        self.event_type = "government"

    def run_and_post(self):
        events = ICSUtils.parse_ics(
            self.url,
            org_id=self.org_id,
            org_name=self.org_name,
            lat=self.lat,
            lon=self.lon,
            event_type=self.event_type
        )
        for ev in events:
            post_event(ev)
