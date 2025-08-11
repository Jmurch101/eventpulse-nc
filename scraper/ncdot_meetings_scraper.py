import requests
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta
from api_client import batch_post


class NCDOTMeetingsScraper:
    base_url = "https://www.ncdot.gov/news/public-meetings/Pages/default.aspx"
    org_id = 60
    org_name = "NC Department of Transportation"
    lat, lon = 35.7796, -78.6382
    event_type = "state"

    def fetch(self, url: str) -> str:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return r.text

    def parse_list(self, html: str, source_url: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        events: list[dict] = []
        # Cards typically under article/section with time & location
        for card in soup.select("article, .news-item, .event, .ms-rtestate-field"):
            text = card.get_text("\n", strip=True)
            if not text:
                continue
            title_el = card.find(["h2", "h3", "h4"]) or None
            title = (title_el.get_text(strip=True) if title_el else None) or "NCDOT Public Meeting"
            # Look for datetime patterns
            dt = None
            for time_el in card.find_all(["time", "span"]):
                t = (time_el.get("datetime") or time_el.get_text(" ", strip=True) or "").strip()
                if not t:
                    continue
                try:
                    dt = parser.parse(t, fuzzy=True)
                    break
                except Exception:
                    continue
            if not dt:
                # Fallback: try entire text
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
                url = "https://www.ncdot.gov" + url
            events.append({
                "title": title,
                "description": text[:600],
                "start_date": dt.isoformat(),
                "end_date": end_dt.isoformat(),
                "location_name": "NCDOT (see link)",
                "latitude": self.lat,
                "longitude": self.lon,
                "organization_id": self.org_id,
                "event_type": self.event_type,
                "source_url": url,
            })
        return events

    def run_and_post(self):
        try:
            html = self.fetch(self.base_url)
        except Exception as e:
            print(f"❌ NCDOT fetch error: {e}")
            return
        events = self.parse_list(html, self.base_url)
        print(f"✅ NCDOT parsed {len(events)} events")
        if events:
            print("NCDOT batch:", batch_post(events))


if __name__ == "__main__":
    NCDOTMeetingsScraper().run_and_post()

