# scraper/ncdot_board_scraper.py

from base_scraper import BaseScraper
from post_event import post_event
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta

class NCDOTBoardScraper(BaseScraper):
    """
    Scrapes NCDOT Board meetings page for scheduled sessions.
    """
    def __init__(self):
        super().__init__(
            "NCDOT Board Meetings",
            "https://www.ncdot.gov/about/board-meetings",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        self.org_id = 33
        self.lat, self.lon = 35.771, -78.638
        self.event_type = "government"

    def parse_events(self, html):
        soup = BeautifulSoup(html, "html.parser")
        events = []
        # Each meeting is in <div class="meeting-item">
        for item in soup.select("div.meeting-item"):  
            title_tag = item.select_one("h3 a")
            date_tag  = item.select_one("time")
            if not (title_tag and date_tag):
                continue

            title = title_tag.text.strip()
            url   = title_tag.get("href")
            date_str = date_tag.get("datetime") or date_tag.text
            try:
                start = parser.parse(date_str, fuzzy=True)
                end   = start + timedelta(hours=2)
            except Exception:
                continue

            events.append({
                "title": title,
                "description": "",
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "location_name": "NCDOT Board Room",
                "latitude": self.lat,
                "longitude": self.lon,
                "organization_id": self.org_id,
                "event_type": self.event_type,
                "source_url": url
            })
        print(f"✅ Found {len(events)} NCDOT Board meetings")
        return events

    def run_and_post(self):
        for e in self.run():
            post_event(e)
