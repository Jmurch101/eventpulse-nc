import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from io import BytesIO
from pdfminer.high_level import extract_text
from dateutil import parser
from datetime import timedelta
from api_client import batch_post


class NCCourtOfAppealsScraper:
    index_url = "https://appellate.nccourts.org/calendar.php?court=2"
    org_id = 68
    org_name = "NC Court of Appeals"
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
            if "getCal.php" in href and "court=2" in href:
                links.append(urljoin(self.index_url, href))
        # Dedup and limit to a few upcoming months
        deduped = list(dict.fromkeys(links))
        return deduped[:3]

    def parse_month(self, html: str, source_url: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        events: list[dict] = []
        # If the month page links to a PDF, attempt to parse text from it
        pdf_link = None
        for a in soup.find_all('a'):
            href = (a.get('href') or '').strip()
            if href.lower().endswith('.pdf'):
                pdf_link = urljoin(source_url, href)
                break
        if pdf_link:
            try:
                pdf_bytes = requests.get(pdf_link, timeout=15).content
                text = extract_text(BytesIO(pdf_bytes))
                # Heuristic: split by lines and look for date/time
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
                        'title': 'NC Court of Appeals Oral Arguments',
                        'description': s[:600],
                        'start_date': dt.isoformat(),
                        'end_date': end_dt.isoformat(),
                        'location_name': 'NC Court of Appeals (see PDF)',
                        'latitude': self.lat,
                        'longitude': self.lon,
                        'organization_id': self.org_id,
                        'event_type': self.event_type,
                        'source_url': pdf_link,
                    })
                # Return early if PDF parsed produced events
                if events:
                    return events
            except Exception:
                pass
        # Heuristic: each argument entry often contains a clear date/time string
        # Collect text blocks under list items or table rows
        blocks = soup.select("li, tr, .event, .calendar, p")
        if not blocks:
            blocks = [soup]

        for blk in blocks:
            text = blk.get_text(" \n", strip=True)
            if not text:
                continue
            if "Oral" not in text and "Argument" not in text and "Court of Appeals" not in text:
                # Still attempt parse since pages may be minimal
                pass
            dt = None
            for piece in text.split("\n"):
                s = piece.strip()
                if not s:
                    continue
                try:
                    dt = parser.parse(s, fuzzy=True)
                    break
                except Exception:
                    continue
            if not dt:
                try:
                    dt = parser.parse(text, fuzzy=True)
                except Exception:
                    dt = None
            if not dt:
                continue
            end_dt = dt + timedelta(hours=2)
            events.append({
                "title": "NC Court of Appeals Oral Arguments",
                "description": text[:600],
                "start_date": dt.isoformat(),
                "end_date": end_dt.isoformat(),
                "location_name": "NC Court of Appeals (see link)",
                "latitude": self.lat,
                "longitude": self.lon,
                "organization_id": self.org_id,
                "event_type": self.event_type,
                "source_url": source_url,
            })
        return events

    def run_and_post(self):
        try:
            idx_html = self.fetch(self.index_url)
        except Exception as e:
            print(f"❌ NC Courts (Appeals) index fetch error: {e}")
            return
        month_links = self.discover_month_links(idx_html)
        all_events: list[dict] = []
        for url in month_links:
            try:
                mhtml = self.fetch(url)
            except Exception:
                continue
            all_events.extend(self.parse_month(mhtml, url))

        # Dedup by title+start
        seen = set()
        deduped = []
        for e in all_events:
            key = (e['title'], e['start_date'])
            if key in seen:
                continue
            seen.add(key)
            deduped.append(e)

        print(f"✅ NC Courts (Appeals) parsed {len(deduped)} events")
        if deduped:
            print("NC Courts (Appeals) batch:", batch_post(deduped))


if __name__ == "__main__":
    NCCourtOfAppealsScraper().run_and_post()

