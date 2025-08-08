# scraper/ncdot_scraper.py

from base_scraper import BaseScraper
from post_event import post_event
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta

class NCDOTScraper(BaseScraper):
    """
    Scrapes NCDOT news & events page for public meetings/releases.
    """
    def __init__(self):
        super().__init__(
            "NCDOT Events",
            "https://www.ncdot.gov/news/Pages/default.aspx",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
        )
        self.org_id = 30
        self.lat, self.lon = 35.771, -78.638
        self.event_type = "government"

    def parse_events(self, html):
        soup = BeautifulSoup(html, "html.parser")
        events = []
        
        # Try different selectors for NCDOT news items
        selectors = [
            "article.release-card",
            ".news-item",
            ".news-release",
            ".ms-rteTable-1 tbody tr",  # Common SharePoint table structure
            ".ms-rtestate-field table tbody tr"
        ]
        
        for selector in selectors:
            items = soup.select(selector)
            if items:
                print(f"✅ Found {len(items)} items using selector: {selector}")
                break
        
        if not items:
            print("⚠️ No news items found with any selector")
            return events
            
        for item in items:
            # Try different title selectors
            title_tag = (
                item.select_one("h2.release-card__title a") or
                item.select_one("h3 a") or
                item.select_one("h2 a") or
                item.select_one("a[href*='news']") or
                item.select_one("td a")
            )
            
            # Try different date selectors
            date_tag = (
                item.select_one("time.release-card__date") or
                item.select_one("time") or
                item.select_one(".date") or
                item.select_one("span.date") or
                item.select_one("td:nth-child(2)")
            )
            
            if not (title_tag and date_tag):
                continue

            title = title_tag.text.strip()
            url = title_tag.get("href", "")
            if url and not url.startswith("http"):
                url = "https://www.ncdot.gov" + url
                
            date_str = date_tag.get("datetime") or date_tag.get("content") or date_tag.text.strip()
            
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
                "location_name": "Statewide, NC",
                "latitude": self.lat,
                "longitude": self.lon,
                "organization_id": self.org_id,
                "event_type": self.event_type,
                "source_url": url
            })
            
        print(f"✅ Found {len(events)} NCDOT items")
        return events

    def run_and_post(self):
        for e in self.run():
            post_event(e)
