import requests
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta
from api_client import batch_post


class UNCCHTMLEventsScraper:
    base_url = "https://calendar.charlotte.edu/"
    org_id = 50
    org_name = "UNC Charlotte"
    lat, lon = 35.3076, -80.7337
    event_type = "university"

    def fetch(self, url: str) -> str:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return r.text

    def parse_list(self, html: str, source_url: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        events: list[dict] = []
        # Localist templates commonly use article or li with time/date spans
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
        try:
            html = self.fetch(self.base_url)
        except Exception as e:
            print(f"❌ UNCC HTML fetch error: {e}")
            return
        events = self.parse_list(html, self.base_url)
        print(f"✅ UNCC HTML parsed {len(events)} events")
        if events:
            print("UNCC HTML batch:", batch_post(events))


if __name__ == "__main__":
    UNCCHTMLEventsScraper().run_and_post()

