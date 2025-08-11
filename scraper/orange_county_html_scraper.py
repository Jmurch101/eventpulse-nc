import requests
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta
from api_client import batch_post


class OrangeCountyHTMLScraper:
    base_url = "https://www.orangecountync.gov/calendar.aspx?CID=7"  # BOCC category; default
    org_id = 45
    org_name = "Orange County Government"
    lat, lon = 36.0607, -79.1097
    event_type = "government"

    def fetch(self, url: str) -> str:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return r.text

    def parse_list(self, html: str, source_url: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        events: list[dict] = []

        # CivicPlus calendar entries in list view
        for item in soup.select(".list div, .event, .ai1ec-event, li, article"):
            title_el = item.select_one("a, h2, h3, .title")
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            href = title_el.get("href") if title_el.name == "a" else None
            url = href if (href and href.startswith("http")) else (source_url if not href else requests.compat.urljoin(source_url, href))

            text = item.get_text(" ", strip=True)
            start = None
            for candidate in [text[:180], text]:
                try:
                    start = parser.parse(candidate, fuzzy=True)
                    break
                except Exception:
                    continue
            if not start:
                continue
            end = start + timedelta(hours=2)
            events.append({
                "title": title,
                "description": "",
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "location_name": self.org_name,
                "latitude": self.lat,
                "longitude": self.lon,
                "organization_id": self.org_id,
                "event_type": self.event_type,
                "source_url": url,
            })
        return events

    def discover_category_urls(self) -> list[str]:
        # Try multiple relevant categories: BOCC, Boards & Commissions, Main
        cids = [7, 9, 10, 11, 36]
        return [f"https://www.orangecountync.gov/calendar.aspx?CID={cid}" for cid in cids]

    def run_and_post(self):
        all_events: list[dict] = []
        for url in self.discover_category_urls():
            try:
                html = self.fetch(url)
            except Exception:
                continue
            all_events.extend(self.parse_list(html, url))
        print(f"✅ Orange County (HTML) parsed {len(all_events)} events across categories")
        if all_events:
            print("Orange County (HTML) batch:", batch_post(all_events))


if __name__ == "__main__":
    OrangeCountyHTMLScraper().run_and_post()

