import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from ics_scrapers import ICSUtils
from api_client import batch_post


class DurhamICSScraper:
    base_url = "https://www.durhamnc.gov/Calendar.aspx"
    org_id = 40
    org_name = "City of Durham"
    lat, lon = 35.9940, -78.8986
    event_type = "government"

    def discover_category_pages(self) -> list[str]:
        headers = {"User-Agent": "Mozilla/5.0"}
        category_links: list[str] = []

        # 1) Try root page for category links
        try:
            r = requests.get(self.base_url, headers=headers, timeout=15)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('a[href*="Calendar.aspx?CID="]'):
                href = a.get("href")
                if not href:
                    continue
                category_links.append(urljoin(self.base_url, href))
        except Exception as e:
            print(f"⚠️ Could not enumerate categories from root: {e}")

        # 2) Probe a small set of likely CivicPlus category IDs
        likely_cids = list(range(1, 21))
        for cid in likely_cids:
            url = f"{self.base_url}?CID={cid}"
            try:
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200 and "Calendar" in r.text:
                    category_links.append(url)
            except Exception:
                continue

        unique = list(dict.fromkeys(category_links))
        print(f"🔎 Found {len(unique)} Durham calendar category pages")
        return unique

    def discover_ics_links(self) -> list[str]:
        headers = {"User-Agent": "Mozilla/5.0"}
        ics_links: list[str] = []

        # Try to find any direct ICS link on the root page
        try:
            r = requests.get(self.base_url, headers=headers, timeout=15)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select('a[href*="/common/modules/iCalendar/export.aspx"]'):
                ics_links.append(urljoin(self.base_url, a.get("href")))
        except Exception:
            pass

        # Also visit each category page and look for an ICS export link or "Subscribe to iCalendar"
        for cat_url in self.discover_category_pages():
            try:
                r = requests.get(cat_url, headers=headers, timeout=15)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, "html.parser")
                # CivicPlus often hides ICS behind buttons with 'Subscribe to iCalendar' text
                for a in soup.find_all('a'):
                    href = a.get('href')
                    text = (a.get_text() or '').strip().lower()
                    if not href:
                        continue
                    if '/common/modules/iCalendar/export.aspx' in href or 'subscribe to icalendar' in text:
                        ics_links.append(urljoin(cat_url, href))
                # Also collect per-event ICS via event IDs present on the page
                for a in soup.select('a[href*="Calendar.aspx?EID="]'):
                    href = a.get('href')
                    if not href:
                        continue
                    try:
                        # Extract EID integer
                        q = urlparse(urljoin(cat_url, href))
                        params = parse_qs(q.query)
                        eid_vals = params.get('EID') or params.get('eid')
                        if not eid_vals:
                            # Fallback: parse from path if formatted like ...EID=1234
                            if 'EID=' in href:
                                eid_vals = [href.split('EID=')[1].split('&')[0]]
                        if not eid_vals:
                            continue
                        eid = eid_vals[0]
                        ics_links.append(f"https://www.durhamnc.gov/common/modules/iCalendar/export.aspx?feed=calendar&eventID={eid}")
                    except Exception:
                        continue
            except Exception:
                continue

        # Normalize and deduplicate
        dedup = list(dict.fromkeys(ics_links))
        print(f"🔗 Found {len(dedup)} Durham ICS export links")
        return dedup

    def run_and_post(self):
        all_events = []
        for ics_url in self.discover_ics_links():
            events = ICSUtils.parse_ics(
                ics_url,
                org_id=self.org_id,
                org_name=self.org_name,
                lat=self.lat,
                lon=self.lon,
                event_type=self.event_type,
            )
            all_events.extend(events)

        if all_events:
            print("Durham ICS batch:", batch_post(all_events))
        else:
            print("Durham ICS: no events parsed")


if __name__ == "__main__":
    DurhamICSScraper().run_and_post()

