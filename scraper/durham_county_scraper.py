import requests
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta
from api_client import batch_post


class DurhamCountyScraper:
    base_url = "https://www.dconc.gov/residents/event-calendar"
    org_id = 44
    org_name = "Durham County Government"
    lat, lon = 35.9940, -78.8986
    event_type = "government"

    def fetch(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return r.text

    def parse_events(self, html):
        soup = BeautifulSoup(html, "html.parser")
        events = []

        # Strategy 1: schema.org Event blocks
        for block in soup.select('[itemtype*="schema.org/Event"]'):
            title_el = block.select_one('[itemprop="name"]') or block.select_one(".event-title, h2, h3")
            start_el = block.select_one('[itemprop="startDate"]')
            end_el = block.select_one('[itemprop="endDate"]')
            loc_el = block.select_one('[itemprop="location"]')
            if not (title_el and start_el):
                continue
            title = title_el.get_text(strip=True)
            raw_start = start_el.get("content") or start_el.get_text(strip=True)
            raw_end = (end_el.get("content") if end_el else None) or (end_el.get_text(strip=True) if end_el else None)
            try:
                start = parser.parse(raw_start, fuzzy=True)
                end = parser.parse(raw_end, fuzzy=True) if raw_end else (start + timedelta(hours=1))
            except Exception:
                continue
            location = loc_el.get_text(strip=True) if loc_el else self.org_name
            events.append({
                "title": title,
                "description": "",
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "location_name": location,
                "latitude": self.lat,
                "longitude": self.lon,
                "organization_id": self.org_id,
                "event_type": self.event_type,
                "source_url": self.base_url,
            })

        # Strategy 2: fallback by scanning common listing containers
        if not events:
            for item in soup.select(".event, .event-item, .eventItem, li, article")[:200]:
                title_el = item.select_one("h2, h3, .title, .event-title, a")
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                text = item.get_text(" ", strip=True)
                # Heuristic: look for date-time in block text
                start = None
                for candidate in [text[:200], text]:
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
                    "source_url": self.base_url,
                })

        return events

    def run_and_post(self):
        try:
            html = self.fetch(self.base_url)
        except Exception as e:
            print(f"❌ Durham County fetch error: {e}")
            return
        events = self.parse_events(html)
        print(f"✅ Durham County parsed {len(events)} events")
        if events:
            print("Durham County batch:", batch_post(events))


if __name__ == "__main__":
    DurhamCountyScraper().run_and_post()

