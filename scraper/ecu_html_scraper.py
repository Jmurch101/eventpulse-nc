import requests
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta
from api_client import batch_post
from datetime import datetime


class ECUHTMLEventsScraper:
    base_url = "https://calendar.ecu.edu/"
    org_id = 51
    org_name = "East Carolina University"
    lat, lon = 35.6079, -77.3664
    event_type = "university"

    def fetch(self, url: str) -> str:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return r.text

    def parse_list(self, html: str, source_url: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        events: list[dict] = []
        for card in soup.select("article, .event, li"):
            title_el = card.find(["h2","h3","a"]) or None
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            text = card.get_text("\n", strip=True)
            dt = None
            for node in card.find_all(["time","span","div"]):
                s = (node.get("datetime") or node.get_text(" ", strip=True) or "").strip()
                if not s:
                    continue
                try:
                    dt = parser.parse(s, fuzzy=True)
                    break
                except Exception:
                    continue
            if not dt:
                try:
                    dt = parser.parse(text, fuzzy=True)
                except Exception:
                    dt = None
            if not dt:
                continue
            end_dt = dt + timedelta(hours=2)
            a = card.find("a")
            url = a.get("href") if a and a.get("href") else source_url
            if url and url.startswith("/"):
                url = self.base_url.rstrip("/") + url
            events.append({
                "title": title,
                "description": text[:600],
                "start_date": dt.isoformat(),
                "end_date": end_dt.isoformat(),
                "location_name": self.org_name,
                "latitude": self.lat,
                "longitude": self.lon,
                "organization_id": self.org_id,
                "event_type": self.event_type,
                "source_url": url,
            })
        return events

    def run_and_post(self):
        pages = [self.base_url]
        # Try Localist list view
        pages.append(self.base_url.rstrip('/') + '/event_list')
        # Try today and next 3 days day-view pages
        today = datetime.now()
        for i in range(0, 4):
            d = today.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=i)
            pages.append(self.base_url.rstrip('/') + f"/calendar/day/{d.year}/{d.month:02d}/{d.day:02d}")

        all_events: list[dict] = []
        for url in pages:
            try:
                html = self.fetch(url)
            except Exception:
                continue
            all_events.extend(self.parse_list(html, url))

        # De-dup by title+start
        seen = set()
        deduped = []
        for e in all_events:
            key = (e['title'], e['start_date'])
            if key in seen:
                continue
            seen.add(key)
            deduped.append(e)

        print(f"✅ ECU HTML parsed {len(deduped)} events across {len(pages)} pages")
        if deduped:
            print("ECU HTML batch:", batch_post(deduped))


if __name__ == "__main__":
    ECUHTMLEventsScraper().run_and_post()

