import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ics_scrapers import ICSUtils
from api_client import batch_post


class UNCGEventsICSScraper:
    base_pages = [
        "https://research.uncg.edu/events/",
    ]
    org_id = 49
    org_name = "UNC Greensboro"
    lat, lon = 36.0726, -79.7920
    event_type = "university"

    def find_ics_links(self) -> list[str]:
        headers = {"User-Agent": "Mozilla/5.0"}
        links: list[str] = []
        for page in self.base_pages:
            try:
                r = requests.get(page, headers=headers, timeout=15)
                r.raise_for_status()
            except Exception as e:
                print(f"❌ UNCG events page fetch failed: {page} {e}")
                continue
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a"):
                href = (a.get("href") or "").strip()
                text = (a.get_text() or "").lower()
                if not href:
                    continue
                if href.endswith(".ics") or "?ical=1" in href or "export" in text and "ics" in text:
                    links.append(urljoin(page, href))
        return list(dict.fromkeys(links))

    def run_and_post(self):
        ics_links = self.find_ics_links()
        all_events: list[dict] = []
        for url in ics_links:
            events = ICSUtils.parse_ics(
                url,
                org_id=self.org_id,
                org_name=self.org_name,
                lat=self.lat,
                lon=self.lon,
                event_type=self.event_type,
            )
            all_events.extend(events)
        if all_events:
            print(f"UNCG ICS parsed {len(all_events)} events from {len(ics_links)} feeds")
            print("UNCG ICS batch:", batch_post(all_events))
        else:
            print("UNCG ICS: no events parsed")


if __name__ == "__main__":
    UNCGEventsICSScraper().run_and_post()

