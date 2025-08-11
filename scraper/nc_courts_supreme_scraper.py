import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO
from pdfminer.high_level import extract_text
from dateutil import parser
from datetime import timedelta
from api_client import batch_post


class NCSupremeCourtScraper:
    index_url = "https://appellate.nccourts.org/calendar.php?court=1"
    org_id = 69
    org_name = "NC Supreme Court"
    lat, lon = 35.7796, -78.6382
    event_type = "state"

    def fetch(self, url: str) -> str:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return r.text

    def discover_month_links(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        links: list[str] = []
        for a in soup.find_all("a"):
            href = (a.get("href") or "").strip()
            if "getCal.php" in href and "court=1" in href:
                links.append(urljoin(self.index_url, href))
        return list(dict.fromkeys(links))[:3]

    def parse_month(self, url: str) -> list[dict]:
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            html = self.fetch(url)
        except Exception:
            return []
        soup = BeautifulSoup(html, "html.parser")
        events: list[dict] = []
        pdf_link = None
        for a in soup.find_all('a'):
            href = (a.get('href') or '').strip()
            if href.lower().endswith('.pdf'):
                pdf_link = urljoin(url, href)
                break
        if not pdf_link:
            return []
        try:
            pdf_bytes = requests.get(pdf_link, headers=headers, timeout=15).content
            text = extract_text(BytesIO(pdf_bytes))
        except Exception:
            return []
        for line in text.splitlines():
            s = line.strip()
            if not s:
                continue
            dt = None
            try:
                dt = parser.parse(s, fuzzy=True)
            except Exception:
                dt = None
            if not dt:
                continue
            end_dt = dt + timedelta(hours=2)
            events.append({
                'title': 'NC Supreme Court Oral Arguments',
                'description': s[:600],
                'start_date': dt.isoformat(),
                'end_date': end_dt.isoformat(),
                'location_name': 'NC Supreme Court (see PDF)',
                'latitude': self.lat,
                'longitude': self.lon,
                'organization_id': self.org_id,
                'event_type': self.event_type,
                'source_url': pdf_link,
            })
        return events

    def run_and_post(self):
        try:
            idx_html = self.fetch(self.index_url)
        except Exception as e:
            print(f"❌ NC Supreme index fetch error: {e}")
            return
        month_links = self.discover_month_links(idx_html)
        all_events: list[dict] = []
        for murl in month_links:
            all_events.extend(self.parse_month(murl))

        # Dedup
        seen = set()
        deduped = []
        for e in all_events:
            key = (e['title'], e['start_date'])
            if key in seen:
                continue
            seen.add(key)
            deduped.append(e)
        print(f"✅ NC Supreme parsed {len(deduped)} events")
        if deduped:
            print("NC Supreme batch:", batch_post(deduped))


if __name__ == "__main__":
    NCSupremeCourtScraper().run_and_post()

