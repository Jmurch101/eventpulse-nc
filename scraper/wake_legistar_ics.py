import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ics_scrapers import ICSUtils
from api_client import batch_post


class WakeCountyLegistarICSScraper:
    base_url = "https://wake.legistar.com/Calendar.aspx"
    org_id = 42
    org_name = "Wake County Government"
    lat, lon = 35.7796, -78.6382
    event_type = "government"

    def fetch_ics_links(self) -> list[str]:
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get(self.base_url, headers=headers, timeout=15)
            r.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch Wake County Legistar calendar: {e}")
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for a in soup.select('a[href*="View.ashx?M=IC&"]'):
            href = a.get("href")
            if not href:
                continue
            links.append(urljoin(self.base_url, href))
        unique = list(dict.fromkeys(links))
        print(f"🔗 Found {len(unique)} Wake County ICS links")
        return unique

    def run_and_post(self):
        events = []
        for ics_url in self.fetch_ics_links():
            events.extend(
                ICSUtils.parse_ics(
                    ics_url,
                    org_id=self.org_id,
                    org_name=self.org_name,
                    lat=self.lat,
                    lon=self.lon,
                    event_type=self.event_type,
                )
            )

        if events:
            stats = batch_post(events)
            print("Wake County Legistar ICS batch:", stats)
        else:
            print("Wake County Legistar ICS: no events parsed")


if __name__ == "__main__":
    WakeCountyLegistarICSScraper().run_and_post()

