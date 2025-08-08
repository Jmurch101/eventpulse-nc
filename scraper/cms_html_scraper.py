# scraper/cms_html_scraper.py

from base_scraper import BaseScraper
from post_event import post_event
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta

class CMSHTMLScraper(BaseScraper):
    """
    Scrapes Charlotte-Mecklenburg Schools calendar page for school events.
    """
    def __init__(self):
        super().__init__(
            "CMS Calendar",
            "https://www.cms.k12.nc.us/calendar",
            headers={"User-Agent":"Mozilla/5.0"}
        )
        self.org_id = 41
        self.lat, self.lon = 35.2271, -80.8431
        self.event_type = "school_holiday"

    def parse_events(self, html):
        soup = BeautifulSoup(html, "html.parser")
        events = []
        # Each event in list with class .event-entry
        for item in soup.select("div.event-entry"):  
            title_tag = item.select_one("h4.event-title")
            date_tag  = item.select_one("time")
            if not (title_tag and date_tag):
                continue

            try:
                start = parser.parse(date_tag.get("datetime") or date_tag.text, fuzzy=True)
                end   = start + timedelta(hours=1)
            except Exception:
                continue

            events.append({
                "title": title_tag.text.strip(),
                "description": "",
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "location_name": "CMS District",
                "latitude": self.lat,
                "longitude": self.lon,
                "organization_id": self.org_id,
                "event_type": self.event_type,
                "source_url": self.base_url
            })
        print(f"✅ Found {len(events)} CMS events")
        return events

    def run_and_post(self):
        for e in self.run():
            post_event(e)