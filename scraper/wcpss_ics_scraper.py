# scraper/wcpss_ics_scraper.py

from ics_scrapers import ICSUtils
from post_event import post_event
from urllib.parse import quote

class WCPSSICSScraper:
    """
    Scrape the Wake County Public Schools 2025-26 Traditional Calendar
    using the Google Calendar ICS feed.
    """
    def __init__(self):
        # Calendar ID from the 'cid' parameter in the Google Calendar link
        calendar_id = (
            "Y181ZDU5YzExYjk4MTY0MmFkMzBiNzk2NGNlMmNjNTQ1ZDlkZWExNzc2OGIxMjUwN2Vk"
            "NzlhNTViZTY0YTNhYmQ4QGdyb3VwLmNhbGVuZGFyLmdvb2dsZS5jb20"
        )
        # Percent-encode the calendar ID for URL safety
        encoded_id = quote(calendar_id, safe='')

        # Use the 'full.ics' feed to capture all events
        self.url        = (
            f"https://calendar.google.com/calendar/ical/{encoded_id}/public/full.ics"
        )
        self.org_id     = 20
        self.org_name   = "Wake County Public Schools"
        self.lat        = 35.7796
        self.lon        = -78.6382
        self.event_type = "school_holiday"

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
