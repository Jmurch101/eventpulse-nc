import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ics_scrapers import ICSUtils
from api_client import batch_post


class CaryIQM2ICSScraper:
    base_url = "https://carync.iqm2.com/citizens/Calendar.aspx"
    org_id = 43
    org_name = "Town of Cary"
    lat, lon = 35.7915, -78.7811
    event_type = "government"

    def fetch_ics_links(self) -> list[str]:
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get(self.base_url, headers=headers, timeout=15)
            r.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch Cary IQM2 calendar: {e}")
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        # Look for agenda rows with iCal links; some IQM2 use Type=134 for ICS
        for a in soup.find_all('a'):
            href = a.get('href')
            text = (a.get_text() or '').lower()
            if not href:
                continue
            if 'viewfile.aspx' in href and ('type=134' in href or 'type=14' in href or 'ical' in text):
                ics_href = href.replace("Type=14", "Type=134")
                links.append(urljoin(self.base_url, ics_href))

        # Fallback: follow meeting detail links then extract ICS from detail pages
        detail_links = []
        for a in soup.select('a[href*="Meeting?ID="]'):
            href = a.get('href')
            if href:
                detail_links.append(urljoin(self.base_url, href))
        for durl in list(dict.fromkeys(detail_links)):
            try:
                dr = requests.get(durl, headers=headers, timeout=15)
                dr.raise_for_status()
            except Exception:
                continue
            dsoup = BeautifulSoup(dr.text, 'html.parser')
            for a in dsoup.find_all('a'):
                href = a.get('href')
                text = (a.get_text() or '').lower()
                if not href:
                    continue
                if 'viewfile.aspx' in href and ('type=134' in href or 'type=14' in href or 'ical' in text):
                    ics_href = href.replace("Type=14", "Type=134")
                    links.append(urljoin(durl, ics_href))
        unique = list(dict.fromkeys(links))
        print(f"🔗 Found {len(unique)} Cary ICS links (IQM2)")
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
            print("Cary IQM2 ICS batch:", batch_post(events))
        else:
            print("Cary IQM2 ICS: no events parsed")


if __name__ == "__main__":
    CaryIQM2ICSScraper().run_and_post()

