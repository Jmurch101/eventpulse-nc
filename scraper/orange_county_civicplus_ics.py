from urllib.parse import urljoin, urlencode
import requests
from bs4 import BeautifulSoup
from ics_scrapers import ICSUtils
from api_client import batch_post


class OrangeCountyCivicPlusICSScraper:
    base_url = "https://www.orangecountync.gov/calendar.aspx"
    org_id = 45
    org_name = "Orange County Government"
    lat, lon = 36.0607, -79.1097
    event_type = "government"

    def fetch_category_ics_links(self) -> list[str]:
        headers = {"User-Agent": "Mozilla/5.0"}
        ics_links: list[str] = []
        # Try a few known/likely category ids (BOCC and general boards)
        candidate_cids = [7, 36]
        for cid in candidate_cids:
            params = {"CID": str(cid)}
            try:
                r = requests.get(self.base_url, headers=headers, params=params, timeout=15)
                r.raise_for_status()
            except Exception as e:
                print(f"⚠️ Failed category page for CID={cid}: {e}")
                continue
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all('a'):
                href = a.get('href')
                text = (a.get_text() or '').lower()
                if not href:
                    continue
                if 'ical' in text or 'subscribe' in text or 'feed=calendar' in href or 'iCalendar' in href:
                    ics_links.append(urljoin(self.base_url, href))
        return list(dict.fromkeys(ics_links))

    def derive_ics_links_from_event_lists(self) -> list[str]:
        # Fallback: visit recent list views by days, scan for ICS
        headers = {"User-Agent": "Mozilla/5.0"}
        ics_links: list[str] = []
        for view in ["list", "week", "month"]:
            params = {"view": view}
            try:
                r = requests.get(self.base_url, headers=headers, params=params, timeout=15)
                r.raise_for_status()
            except Exception:
                continue
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all('a'):
                href = a.get('href')
                text = (a.get_text() or '').lower()
                if not href:
                    continue
                if 'ical' in text or 'subscribe' in text or 'ics' in href or 'feed=calendar' in href:
                    ics_links.append(urljoin(self.base_url, href))
        return list(dict.fromkeys(ics_links))

    def run_and_post(self):
        ics_urls = self.fetch_category_ics_links()
        if not ics_urls:
            ics_urls = self.derive_ics_links_from_event_lists()
        ics_urls = list(dict.fromkeys(ics_urls))
        print(f"🔗 Found {len(ics_urls)} Orange County CivicPlus ICS links")

        events = []
        for ics_url in ics_urls:
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
            print("Orange County CivicPlus ICS batch:", batch_post(events))
        else:
            print("Orange County CivicPlus ICS: no events parsed")


if __name__ == "__main__":
    OrangeCountyCivicPlusICSScraper().run_and_post()

