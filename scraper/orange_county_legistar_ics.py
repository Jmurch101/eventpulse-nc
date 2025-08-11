import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ics_scrapers import ICSUtils
from api_client import batch_post


class OrangeCountyLegistarICSScraper:
    base_url = "https://orangecountync.legistar.com/Calendar.aspx"
    org_id = 45
    org_name = "Orange County Government"
    lat, lon = 36.0607, -79.1097
    event_type = "government"

    def fetch_ics_links(self) -> list[str]:
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get(self.base_url, headers=headers, timeout=15)
            r.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch Orange County Legistar calendar: {e}")
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        # Primary iCal export links
        for a in soup.select('a[href*="View.ashx?M=IC&"]'):
            href = a.get("href")
            if not href:
                continue
            links.append(urljoin(self.base_url, href))
        # Also follow year pages and collect per-meeting iCal links
        for a in soup.select('a[href*="Calendar.aspx?From=year"]'):
            year_href = a.get('href')
            if not year_href:
                continue
            year_url = urljoin(self.base_url, year_href)
            try:
                yr = requests.get(year_url, headers=headers, timeout=15)
                yr.raise_for_status()
            except Exception:
                continue
            ysoup = BeautifulSoup(yr.text, 'html.parser')
            for y in ysoup.select('a[href*="View.ashx?M=IC&"]'):
                href = y.get('href')
                if href:
                    links.append(urljoin(self.base_url, href))
        unique = list(dict.fromkeys(links))
        print(f"🔗 Found {len(unique)} Orange County (NC) Legistar ICS links")
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
            print("Orange County Legistar ICS batch:", stats)
        else:
            print("Orange County Legistar ICS: no events parsed")


if __name__ == "__main__":
    OrangeCountyLegistarICSScraper().run_and_post()

