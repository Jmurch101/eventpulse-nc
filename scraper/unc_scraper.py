# scraper/unc_scraper.py

from base_scraper import BaseScraper
from api_client import batch_post
from datetime import timedelta
from bs4 import BeautifulSoup
from dateutil import parser

class UNCScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            "UNC Chapel Hill",
            "https://calendar.unc.edu/",
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

        # Localist cards
        for card in soup.select(".em-card"):
            title_tag = card.select_one("h3.em-card_title a")
            date_tags = card.select("p.em-card_event-text")
            loc_tag   = card.select_one("p.em-card_event-text a[href*='calendar.unc.edu']")

            if not title_tag or not date_tags:
                continue

            title    = title_tag.text.strip()
            date_str = date_tags[0].text.strip()
            url      = title_tag["href"]

            try:
                start = parser.parse(date_str, fuzzy=True)
                end   = start + timedelta(hours=1)
            except Exception as e:
                print(f"❌ UNC date parse error '{title}': {e}")
                continue

            events.append({
                "title":          title,
                "description":    "",
                "start_date":     start.isoformat(),
                "end_date":       end.isoformat(),
                "location_name":  loc_tag.text.strip() if loc_tag else "UNC Chapel Hill",
                "latitude":       35.9049,
                "longitude":     -79.0469,
                "organization_id": 2,
                "event_type":     "academic",
                "source_url":     url
            })

        print(f"✅ Found {len(events)} UNC events")
        return events

    def run_and_post(self):
        events = self.run()
        if events:
            stats = batch_post(events)
            print("UNC batch:", stats)
