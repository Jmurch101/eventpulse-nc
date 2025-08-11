# scraper/durham_scraper.py

from base_scraper import BaseScraper
from api_client import batch_post
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta
import requests
from urllib.parse import urljoin, urlparse, parse_qs


class DurhamCityScraper(BaseScraper):
    """
    Scrapes Durham City public meetings by discovering category pages, collecting
    event detail links (EID), and parsing each event detail page for title/date/location.
    """
    def __init__(self):
        super().__init__(
            "Durham City Meetings",
            "https://durhamnc.gov/Calendar.aspx",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        self.org_id = 40
        self.lat, self.lon = 35.9940, -78.8986
        self.event_type = "government"

    def discover_category_pages(self):
        # Probe a wider range of category IDs
        pages = [self.base_url]
        for cid in range(1, 201):
            pages.append(f"{self.base_url}?CID={cid}")
        return pages

    def extract_event_links(self, html, page_url):
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for a in soup.select('a[href*="Calendar.aspx?EID="]'):
            href = a.get("href")
            if not href:
                continue
            links.append(urljoin(page_url, href))
        return list(dict.fromkeys(links))

    def parse_event_detail(self, html, url):
        soup = BeautifulSoup(html, "html.parser")
        # Title: h1 or document title
        title_tag = soup.select_one("h1, .page-title, #PageTitle")
        title = (title_tag.get_text(strip=True) if title_tag else (soup.title.get_text(strip=True) if soup.title else "Durham Event"))

        # Try to find date/time via <time> elements
        start = None
        time_tags = soup.find_all("time")
        for t in time_tags:
            dt = t.get("datetime") or t.get_text(strip=True)
            if not dt:
                continue
            try:
                start = parser.parse(dt, fuzzy=True)
                break
            except Exception:
                continue
        if not start:
            # Fallback: regex-like fuzzy parse across the page text
            try:
                start = parser.parse(soup.get_text(" ", strip=True), fuzzy=True)
            except Exception:
                return None
        end = start + timedelta(hours=1)

        # Location: look for label or common classes
        location = "Durham, NC"
        cand = soup.find(string=lambda s: isinstance(s, str) and "Location" in s)
        if cand and cand.parent:
            # Try sibling text
            sibling_text = cand.parent.get_text(" ", strip=True)
            if ":" in sibling_text:
                loc = sibling_text.split(":", 1)[1].strip()
                if loc:
                    location = loc

        return {
            "title": title,
            "description": "",
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "location_name": location,
            "latitude": self.lat,
            "longitude": self.lon,
            "organization_id": self.org_id,
            "event_type": self.event_type,
            "source_url": url,
        }

    def run(self):
        headers = self.headers
        session = requests.Session()
        session.headers.update(headers)
        all_event_links = []
        # Collect event links from root and category pages
        for cat_url in self.discover_category_pages():
            try:
                r = session.get(cat_url, timeout=12)
                if r.status_code != 200:
                    continue
                all_event_links.extend(self.extract_event_links(r.text, cat_url))
            except Exception:
                continue
        all_event_links = list(dict.fromkeys(all_event_links))[:200]

        events = []
        for ev_url in all_event_links:
            try:
                r = session.get(ev_url, timeout=12)
                if r.status_code != 200:
                    continue
                parsed = self.parse_event_detail(r.text, ev_url)
                if parsed:
                    events.append(parsed)
            except Exception:
                continue
        print(f"✅ Found {len(events)} Durham meetings (HTML)")
        return events

    def run_and_post(self):
        events = self.run()
        if events:
            stats = batch_post(events)
            print("Durham HTML batch:", stats)

    # Implement abstract method to satisfy BaseScraper, not used in this subclass
    def parse_events(self, html):
        return []


if __name__ == "__main__":
    DurhamCityScraper().run_and_post()