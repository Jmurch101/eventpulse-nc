import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ics_scrapers import ICSUtils
from api_client import batch_post


class ChathamCountyLegistarICSScraper:
    base_url = "https://chathamnc.legistar.com/Calendar.aspx"
    org_id = 47
    org_name = "Chatham County Government"
    lat, lon = 35.7267, -79.1647
    event_type = "government"

    def fetch_ics_links(self) -> list[str]:
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get(self.base_url, headers=headers, timeout=15)
            r.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch Chatham County Legistar calendar: {e}")
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for a in soup.select('a[href*="View.ashx?M=IC&"]'):
            href = a.get("href")
            if href:
                links.append(urljoin(self.base_url, href))
        # Follow year pages as well
        for a in soup.select('a[href*="Calendar.aspx?From=year"]'):
            yhref = a.get('href')
            if not yhref:
                continue
            yurl = urljoin(self.base_url, yhref)
            try:
                yr = requests.get(yurl, headers=headers, timeout=15)
                yr.raise_for_status()
            except Exception:
                continue
            ysoup = BeautifulSoup(yr.text, 'html.parser')
            for y in ysoup.select('a[href*="View.ashx?M=IC&"]'):
                href = y.get('href')
                if href:
                    links.append(urljoin(self.base_url, href))
        unique = list(dict.fromkeys(links))
        print(f"🔗 Found {len(unique)} Chatham County Legistar ICS links")
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
            print("Chatham County Legistar ICS batch:", batch_post(events))
        else:
            print("Chatham County Legistar ICS: no events parsed")


if __name__ == "__main__":
    ChathamCountyLegistarICSScraper().run_and_post()

