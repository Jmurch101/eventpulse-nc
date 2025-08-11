# scraper/raleigh_scraper.py

from base_scraper import BaseScraper
from api_client import batch_post
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta

class RaleighCityScraper(BaseScraper):
    """
    Scrapes Raleigh city events from their website.
    """
    def __init__(self):
        super().__init__(
            "Raleigh City Events",
            "https://raleighnc.gov/",
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

        # Look for event containers
        event_containers = soup.select(".event-item, .calendar-event, .meeting-item, .news-item")

        for container in event_containers:
            try:
                title_tag = container.select_one("h3, h4, .title, .event-title")
                date_tag = container.select_one(".date, .event-date, time, .published-date")
                location_tag = container.select_one(".location, .venue, .address")
                link_tag = container.select_one("a")

                if not title_tag:
                    continue

                title = title_tag.text.strip()
                date_str = date_tag.text.strip() if date_tag else ""
                location = location_tag.text.strip() if location_tag else "Raleigh, NC"
                url = link_tag.get("href") if link_tag else ""

                if not date_str:
                    continue

                try:
                    start = parser.parse(date_str, fuzzy=True)
                    end = start + timedelta(hours=1)
                except Exception as e:
                    print(f"❌ Date parse error for '{title}': {e}")
                    continue

                event_data = {
                    "title": title,
                    "description": f"Event in Raleigh, NC: {title}",
                    "start_date": start.isoformat(),
                    "end_date": end.isoformat(),
                    "location_name": location,
                    "latitude": 35.7796,
                    "longitude": -78.6382,
                    "organization_id": 1,
                    "event_type": "city",
                    "source_url": url if url.startswith("http") else f"https://raleighnc.gov{url}"
                }

                events.append(event_data)
                print(f"✅ Found Raleigh event: {title}")

            except Exception as e:
                print(f"❌ Error parsing Raleigh event: {e}")
                continue

        return events

    def run_and_post(self):
        events = self.run()
        if events:
            stats = batch_post(events)
            print("Raleigh batch:", stats)