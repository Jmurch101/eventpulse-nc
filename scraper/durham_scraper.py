# scraper/durham_scraper.py

from base_scraper import BaseScraper
from post_event import post_event
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta

class DurhamCityScraper(BaseScraper):
    """
    Scrapes Durham City public meetings calendar.
    """
    def __init__(self):
        super().__init__(
            "Durham City Meetings",
            "https://durhamnc.gov/Calendar.aspx?CID=1",
            headers={"User-Agent":"Mozilla/5.0"}
        )
        self.org_id = 40
        self.lat, self.lon = 35.9940, -78.8986
        self.event_type = "government"

    def parse_events(self, html):
        soup = BeautifulSoup(html, "html.parser")
        events = []
        # Each event in a .calendar-item div
        for item in soup.select("div.calendar-item"):  
            title_tag = item.select_one("a.calendar-item-link")
            date_tag  = item.select_one("span.calendar-item-date")
            if not (title_tag and date_tag):
                continue

            try:
                start = parser.parse(date_tag.text.strip(), fuzzy=True)
                end   = start + timedelta(hours=1)
            except Exception:
                continue

            events.append({
                "title": title_tag.text.strip(),
                "description": "",
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "location_name": "Durham, NC",
                "latitude": self.lat,
                "longitude": self.lon,
                "organization_id": self.org_id,
                "event_type": self.event_type,
                "source_url": title_tag.get("href")
            })
        print(f"✅ Found {len(events)} Durham meetings")
        return events

    def run_and_post(self):
        for e in self.run():
            post_event(e)