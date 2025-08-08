# scraper/holiday_scraper.py

from base_scraper import BaseScraper
from post_event import post_event
from bs4 import BeautifulSoup
from datetime import datetime

class HolidayScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            "US Holidays",
            "https://www.timeanddate.com/holidays/us/",
            headers={"User-Agent": "Mozilla/5.0"}
        )

    def parse_events(self, html):
        soup = BeautifulSoup(html, "html.parser")
        events = []

        # All rows in zebra table (skip header)
        for row in soup.select("table.zebra.tb-hover tbody tr"):
            cols = row.find_all("td")
            if len(cols) < 2:
                continue

            date_text = cols[0].text.strip()
            name      = cols[1].text.strip()
            if not name:
                continue

            try:
                # e.g. "Jan 1" + current year
                date_obj = datetime.strptime(f"{date_text} {datetime.now().year}", "%b %d %Y")
            except Exception as e:
                print(f"❌ Holiday parse error '{name}': {e}")
                continue

            events.append({
                "title":          name,
                "description":    "Observed public holiday in the U.S.",
                "start_date":     date_obj.isoformat(),
                "end_date":       date_obj.replace(hour=23, minute=59).isoformat(),
                "location_name":  "North Carolina, USA",
                "latitude":       35.7596,
                "longitude":     -79.0193,
                "organization_id": 99,
                "event_type":     "holiday",
                "source_url":     self.base_url
            })

        print(f"✅ Found {len(events)} holidays")
        return events

    def run_and_post(self):
        for e in self.run():
            post_event(e)
