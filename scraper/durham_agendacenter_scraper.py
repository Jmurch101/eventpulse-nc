import requests
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import timedelta
from api_client import batch_post


class DurhamAgendaCenterScraper:
    boards = [
        ("City Council", "https://www.durhamnc.gov/AgendaCenter/City-Council-4"),
        ("Planning Commission", "https://www.durhamnc.gov/AgendaCenter/Planning-Commission-15"),
        ("Board of Adjustment", "https://www.durhamnc.gov/AgendaCenter/Board-of-Adjustment-BOA-10"),
        ("Historic Preservation Commission", "https://www.durhamnc.gov/AgendaCenter/Historic-Preservation-Commission-8"),
        ("Environmental Affairs Board", "https://www.durhamnc.gov/AgendaCenter/Environmental-Affairs-Board-12"),
        ("Recreation Advisory Commission", "https://www.durhamnc.gov/AgendaCenter/Recreation-Advisory-Commission-23"),
        ("Bicycle and Pedestrian Advisory Commission", "https://www.durhamnc.gov/AgendaCenter/Durham-Bicycle-and-Pedestrian-Advisory-Comm-18"),
        ("Cultural Advisory Board", "https://www.durhamnc.gov/AgendaCenter/Cultural-Advisory-Board-39"),
        ("Open Space & Trails Commission (DOST)", "https://www.durhamnc.gov/AgendaCenter/Durham-Open-Space-and-Trails-Commission-21"),
        ("Public Art Committee", "https://www.durhamnc.gov/AgendaCenter/Public-Art-Committee-37"),
        ("Human Relations Commission", "https://www.durhamnc.gov/AgendaCenter/Human-Relations-Commission-19"),
        ("Housing Appeals Board", "https://www.durhamnc.gov/AgendaCenter/Housing-Appeals-Board-11"),
        ("Joint City-County Planning Committee (JCCPC)", "https://www.durhamnc.gov/AgendaCenter/Joint-City-County-Planning-Committee-14"),
    ]

    org_id = 40
    org_name = "City of Durham"
    lat, lon = 35.9940, -78.8986
    event_type = "government"

    def fetch(self, url: str) -> str:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return r.text

    def parse_board(self, name: str, url: str):
        html = self.fetch(url)
        soup = BeautifulSoup(html, "html.parser")
        events = []
        # Table rows often under a listing; extract all agenda rows
        for row in soup.select("table tr"):
            cols = row.find_all(["td", "th"])  # include th for header-like first row
            if not cols:
                continue
            text = row.get_text(" ", strip=True)
            if not text:
                continue
            # Find a date in the row text
            try:
                dt = parser.parse(text, fuzzy=True)
            except Exception:
                continue
            title = f"{name} Meeting"
            # Prefer the agenda link as source URL
            link = row.find("a")
            href = link.get("href") if link else None
            if href and href.startswith("/"):
                source_url = f"https://www.durhamnc.gov{href}"
            else:
                source_url = href or url

            events.append({
                "title": title,
                "description": "",
                "start_date": dt.isoformat(),
                "end_date": (dt + timedelta(hours=2)).isoformat(),
                "location_name": "Durham, NC",
                "latitude": self.lat,
                "longitude": self.lon,
                "organization_id": self.org_id,
                "event_type": self.event_type,
                "source_url": source_url,
            })
        return events

    def run_and_post(self):
        all_events = []
        for name, url in self.boards:
            try:
                all_events.extend(self.parse_board(name, url))
            except Exception as e:
                print(f"❌ Error scraping {name}: {e}")
        print(f"✅ Durham Agenda Center parsed {len(all_events)} events")
        if all_events:
            print("Durham Agenda Center batch:", batch_post(all_events))


if __name__ == "__main__":
    DurhamAgendaCenterScraper().run_and_post()

