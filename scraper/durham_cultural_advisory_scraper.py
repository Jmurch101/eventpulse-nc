from datetime import timedelta
from dateutil import parser
import requests
from bs4 import BeautifulSoup
from api_client import batch_post


class DurhamCulturalAdvisoryScraper:
    url = "https://www.durhamnc.gov/452/Durham-Cultural-Advisory-Board"
    org_id = 40
    org_name = "City of Durham"
    lat, lon = 35.9940, -78.8986
    event_type = "government"

    def fetch(self) -> str:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(self.url, headers=headers, timeout=15)
        r.raise_for_status()
        return r.text

    def parse(self):
        html = self.fetch()
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text("\n", strip=True)

        events = []
        # Look for explicit meeting date lines under NEXT MEETING / Meeting Schedule
        for li in soup.find_all(['li', 'p']):
            t = li.get_text(" ", strip=True)
            if not t:
                continue
            if any(k in t for k in ["2025", "2026", "Wednesday", "pm", "AM", "September", "October", "November", "December", "January", "February", "March", "April", "May", "June"]):
                try:
                    dt = parser.parse(t, fuzzy=True)
                except Exception:
                    continue
                end = dt + timedelta(hours=2)
                events.append({
                    "title": "Durham Cultural Advisory Board Meeting",
                    "description": "Monthly DCAB meeting.",
                    "start_date": dt.isoformat(),
                    "end_date": end.isoformat(),
                    "location_name": "General Services Dept or Zoom",
                    "latitude": self.lat,
                    "longitude": self.lon,
                    "organization_id": self.org_id,
                    "event_type": self.event_type,
                    "source_url": self.url,
                })
        return events

    def run_and_post(self):
        events = self.parse()
        print(f"✅ Durham Cultural Advisory parsed {len(events)} events")
        if events:
            print("Durham Cultural Advisory batch:", batch_post(events))


if __name__ == "__main__":
    DurhamCulturalAdvisoryScraper().run_and_post()

