from base_scraper import BaseScraper
from post_event import post_event
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from dateutil import parser  # Requires: pip install python-dateutil

class NCSUScraper(BaseScraper):
    def __init__(self):
        super().__init__("NC State University", "https://calendar.ncsu.edu/")

    def parse_events(self, html):
        soup = BeautifulSoup(html, "html.parser")
        events = []

        event_cards = soup.select(".em-card")  # Matches top-level event blocks

        for card in event_cards:
            try:
                title_tag = card.select_one("h3.em-card_title a")
                date_tags = card.select("p.em-card_event-text")
                
                if not date_tags:
                    print("⚠️ No date info, skipping event.")
                    continue
                    
                date_str = date_tags[0].text.strip()  # First <p> with time
                location_tag = card.select_one("p.em-card_event-text a[href*='calendar.ncsu.edu']")

                if not title_tag:
                    continue

                title = title_tag.text.strip()

                try:
                    start_date = parser.parse(date_str, fuzzy=True)
                    # Default to 1-hour duration if no end specified
                    end_date = start_date + timedelta(hours=1)
                except Exception as e:
                    print(f"❌ Date parsing error for event '{title}': {e}")
                    continue

                event = {
                    "title": title,
                    "description": "",  # Optionally scrape detail page later
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "location_name": location_tag.text.strip() if location_tag else "NC State",
                    "latitude": 35.7847,
                    "longitude": -78.6821,
                    "organization_id": 1,
                    "event_type": "academic",
                    "source_url": title_tag.get("href")
                }

                events.append(event)

            except Exception as e:
                print(f"⚠️ Skipped malformed event: {e}")
                continue

        print(f"✅ Found {len(events)} events")
        return events

    def run_and_post(self):
        events = self.run()
        for event in events:
            post_event(event)
