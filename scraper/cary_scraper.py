# scraper/cary_scraper.py

from base_scraper import BaseScraper
from post_event import post_event
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta

class CaryCityScraper(BaseScraper):
    """
    Scrapes Cary city events and meetings.
    """
    def __init__(self):
        super().__init__(
            "Cary City Events",
            "https://www.townofcary.org/",
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
        event_containers = soup.select(".event-item, .calendar-event, .meeting-item")

        for container in event_containers:
            try:
                title_tag = container.select_one("h3, h4, .title")
                date_tag = container.select_one(".date, .event-date, time")
                location_tag = container.select_one(".location, .venue")
                link_tag = container.select_one("a")

                if not title_tag:
                    continue

                title = title_tag.text.strip()
                date_str = date_tag.text.strip() if date_tag else ""
                location = location_tag.text.strip() if location_tag else "Cary, NC"
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
                    "description": f"Event in Cary, NC: {title}",
                    "start_date": start.isoformat(),
                    "end_date": end.isoformat(),
                    "location_name": location,
                    "latitude": 35.7915,
                    "longitude": -78.7811,
                    "organization_id": 1,
                    "event_type": "city",
                    "source_url": url if url.startswith("http") else f"https://www.townofcary.org{url}"
                }

                events.append(event_data)
                print(f"✅ Found Cary event: {title}")

            except Exception as e:
                print(f"❌ Error parsing Cary event: {e}")
                continue

        return events

    def run_and_post(self):
        events = self.run()
        for event in events:
            try:
                post_event(event)
                print(f"✅ Posted: {event['title']}")
            except Exception as e:
                print(f"❌ Failed to post Cary event: {e}") 