import requests
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta
from api_client import batch_post


class WakeForestEventsScraper:
    base_url = "https://events.wfu.edu/"
    org_id = 48
    org_name = "Wake Forest University"
    lat, lon = 36.1353, -80.2770
    event_type = "university"

    def fetch_day(self, yyyy: int, mm: int, dd: int) -> str:
        url = f"https://events.wfu.edu/calendar/day/{yyyy}/{mm:02d}/{dd:02d}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return r.text

    def parse_list(self, html: str, source_url: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        events = []
        for item in soup.select('[data-start], .event, article, li'):
            title_el = item.select_one('h3, h2, a')
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            href = title_el.get('href') or source_url
            url = href if href.startswith('http') else requests.compat.urljoin(source_url, href)
            # Try to read start time from attributes or surrounding text
            raw = item.get('data-start') or item.get_text(" ", strip=True)
            start = None
            for candidate in [raw[:200], raw]:
                try:
                    start = parser.parse(candidate, fuzzy=True)
                    break
                except Exception:
                    continue
            if not start:
                continue
            end = start + timedelta(hours=1)
            events.append({
                "title": title,
                "description": "",
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "location_name": self.org_name,
                "latitude": self.lat,
                "longitude": self.lon,
                "organization_id": self.org_id,
                "event_type": self.event_type,
                "source_url": url,
            })
        return events

    def run_and_post(self):
        # Scrape a small window (today +/- 7 days)
        from datetime import datetime, timedelta as td
        today = datetime.utcnow().date()
        all_events: list[dict] = []
        for delta in range(-2, 8):
            d = today + td(days=delta)
            try:
                html = self.fetch_day(d.year, d.month, d.day)
            except Exception:
                continue
            all_events.extend(self.parse_list(html, f"https://events.wfu.edu/calendar/day/{d.year}/{d.month:02d}/{d.day:02d}"))
        print(f"✅ Wake Forest Events parsed {len(all_events)} items")
        if all_events:
            print("Wake Forest Events batch:", batch_post(all_events))


if __name__ == "__main__":
    WakeForestEventsScraper().run_and_post()

