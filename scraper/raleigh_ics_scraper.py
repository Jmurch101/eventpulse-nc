# scraper/raleigh_ics_scraper.py

from ics_scrapers import ICSUtils
from post_event import post_event

class RaleighICSScraper:
    def __init__(self):
        # Full URL for the “Add All Events to Calendar” ICS feed
        self.url        = "https://raleighnc.gov/events/22846/22846/events.ics"
        self.org_id     = 10
        self.org_name   = "City of Raleigh"
        self.lat        = 35.7796
        self.lon        = -78.6382
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
