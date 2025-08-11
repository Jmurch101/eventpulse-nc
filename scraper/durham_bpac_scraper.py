import re
from datetime import datetime, timedelta
from dateutil import parser
import requests
from bs4 import BeautifulSoup
from api_client import batch_post


class DurhamBPACScraper:
    url = "https://www.durhamnc.gov/3851/Durham-Bicycle-and-Pedestrian-Advisory-C"
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
        text = soup.get_text("\n")

        # Meeting time: third Tuesday monthly, stated as 7 p.m. to 9 p.m.
        default_start_time = "7:00 pm"
        default_end_time = "9:00 pm"

        events = []

        # Try to detect a section like "BPAC Meeting Dates for 2025" with month abbreviations
        # Capture patterns like "Jan 21", "Feb 18", etc. Assume the header year nearby (2025)
        year_candidates = re.findall(r"BPAC\s+Meeting\s+Dates\s+for\s+(\d{4})", text, flags=re.I)
        year = int(year_candidates[0]) if year_candidates else datetime.utcnow().year

        # Find month-day tokens
        for m, d in re.findall(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})\b", text):
            datestr = f"{m} {d}, {year} {default_start_time}"
            try:
                start = parser.parse(datestr)
                end = parser.parse(f"{m} {d}, {year} {default_end_time}")
            except Exception:
                continue
            # Drop past events older than 60 days
            if start < datetime.utcnow() - timedelta(days=60):
                continue
            events.append({
                "title": "Durham BPAC Meeting",
                "description": "Monthly Bicycle & Pedestrian Advisory Commission meeting.",
                "start_date": start.isoformat(),
                "end_date": end.isoformat(),
                "location_name": "Durham City Hall (or Zoom)",
                "latitude": self.lat,
                "longitude": self.lon,
                "organization_id": self.org_id,
                "event_type": self.event_type,
                "source_url": self.url,
            })

        return events

    def run_and_post(self):
        events = self.parse()
        print(f"✅ Durham BPAC parsed {len(events)} events")
        if events:
            print("Durham BPAC batch:", batch_post(events))


if __name__ == "__main__":
    DurhamBPACScraper().run_and_post()

