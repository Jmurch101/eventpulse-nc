# scraper/duke_scraper.py

from base_scraper import BaseScraper
from api_client import batch_post
from datetime import timedelta
from bs4 import BeautifulSoup
from dateutil import parser

class DukeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            "Duke University",
            "https://calendar.duke.edu/",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
        )

    def parse_events(self, html):
        soup = BeautifulSoup(html, "html.parser")
        events = []

        # Duke uses single-events-container for each event
        for card in soup.select(".single-events-container"):
            title_tag = card.select_one("h2.event-title a")
            date_tag = card.select_one(".featured-info[itemprop='date']")
            time_tag = card.select_one(".featured-info[itemprop='time']")
            location_tag = card.select_one(".featured-info[itemprop='location'] a")

            if not title_tag or not date_tag:
                continue

            title = title_tag.text.strip()
            date_str = date_tag.text.strip()
            time_str = time_tag.text.strip() if time_tag else ""
            url = title_tag.get("href")
            
            # Extract start time from time ranges (e.g., "6:00 pm - 8:00 pm" -> "6:00 pm")
            if " - " in time_str:
                time_str = time_str.split(" - ")[0].strip()
            
            # Combine date and time for parsing
            datetime_str = f"{date_str} {time_str}".strip()

            try:
                start = parser.parse(datetime_str, fuzzy=True)
                # Default to 1-hour duration if no end time specified
                end = start + timedelta(hours=1)
            except Exception as e:
                print(f"❌ Duke date parse error '{title}': {e}")
                continue

            events.append({
                "title":          title,
                "description":    "",
                "start_date":     start.isoformat(),
                "end_date":       end.isoformat(),
                "location_name":  location_tag.text.strip() if location_tag else "Duke University",
                "latitude":       36.0014,
                "longitude":     -78.9382,
                "organization_id": 3,
                "event_type":     "academic",
                "source_url":     url
            })

        print(f"✅ Found {len(events)} Duke events")
        return events

    def run_and_post(self):
        events = self.run()
        if events:
            stats = batch_post(events)
            print("Duke batch:", stats)
