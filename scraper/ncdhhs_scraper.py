# scraper/ncdhhs_scraper.py

from base_scraper import BaseScraper
from post_event import post_event
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta

class NCDHHSScraper(BaseScraper):
    """
    Scrapes NC DHHS events and public meetings page.
    """
    def __init__(self):
        super().__init__(
            "NC DHHS Events",
            "https://www.ncdhhs.gov/news",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
        )
        self.org_id = 31
        self.lat, self.lon = 35.904, -78.940
        self.event_type = "government"

    def parse_events(self, html):
        soup = BeautifulSoup(html, "html.parser")
        events = []
        
        # Try different selectors for DHHS news/events
        selectors = [
            "div.view-events div.views-row",
            ".news-item",
            ".event-item",
            ".views-row",
            "article",
            ".content-item"
        ]
        
        for selector in selectors:
            items = soup.select(selector)
            if items:
                print(f"✅ Found {len(items)} items using selector: {selector}")
                break
        
        if not items:
            print("⚠️ No news/event items found with any selector")
            return events
            
        for item in items:
            # Try different title selectors
            title_tag = (
                item.select_one("h3 a") or
                item.select_one("h2 a") or
                item.select_one("h4 a") or
                item.select_one("a[href*='news']") or
                item.select_one("a[href*='event']") or
                item.select_one(".title a") or
                item.select_one("a")
            )
            
            # Skip if title contains navigation text
            if title_tag:
                title = title_tag.text.strip()
                if any(nav_text in title.lower() for nav_text in ['press releases', 'news', 'home', 'about', 'contact']):
                    continue
                
            # Try different date selectors
            date_tag = (
                item.select_one("span.date-display-single") or
                item.select_one("time") or
                item.select_one(".date") or
                item.select_one("span.date") or
                item.select_one(".published") or
                item.select_one(".meta")
            )
            
            if not (title_tag and date_tag):
                continue

            url = title_tag.get("href", "")
            if url and not url.startswith("http"):
                url = "https://www.ncdhhs.gov" + url
                
            date_str = date_tag.get("content") or date_tag.get("datetime") or date_tag.text.strip()
            
            try:
                start = parser.parse(date_str, fuzzy=True)
                end = start + timedelta(hours=1)
            except Exception as e:
                print(f"❌ Date parse error for '{title}': {e}")
                continue

            events.append({
                "title": title,
                "description": "",
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "location_name": "NC DHHS",
                "latitude": self.lat,
                "longitude": self.lon,
                "organization_id": self.org_id,
                "event_type": self.event_type,
                "source_url": url
            })
            
        print(f"✅ Found {len(events)} DHHS events")
        return events

    def run_and_post(self):
        for e in self.run():
            post_event(e)
