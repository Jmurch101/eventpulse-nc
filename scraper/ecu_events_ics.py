import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ics_scrapers import ICSUtils
from api_client import batch_post


class ECUEventsICSScraper:
    base_pages = [
        "https://calendar.ecu.edu/",
    ]
    org_id = 51
    org_name = "East Carolina University"
    lat, lon = 35.6079, -77.3664
    event_type = "university"

    def find_ics_links(self) -> list[str]:
        headers = {"User-Agent": "Mozilla/5.0"}
        links: list[str] = []
        for page in self.base_pages:
            try:
                r = requests.get(page, headers=headers, timeout=15)
                r.raise_for_status()
            except Exception as e:
                print(f"❌ ECU page fetch failed: {page} {e}")
                continue
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a"):
                href = (a.get("href") or "").strip()
                text = (a.get_text() or "").lower()
                if not href:
                    continue
                if href.endswith(".ics") or "?ical" in href or ("calendar" in href and "ics" in href):
                    links.append(urljoin(page, href))
        links.append("https://calendar.ecu.edu/events.ics")
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
            print(f"ECU ICS parsed {len(all_events)} events from {len(ics_links)} feeds")
            print("ECU ICS batch:", batch_post(all_events))
        else:
            print("ECU ICS: no events parsed")


if __name__ == "__main__":
    ECUEventsICSScraper().run_and_post()

