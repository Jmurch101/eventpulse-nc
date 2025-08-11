import requests
from api_client import batch_post
from datetime import datetime, timedelta

class UNCJsonScraper:
    def __init__(self):
        self.name    = "UNC Chapel Hill (JSON)"
        self.url     = "https://events.unc.edu/events.json"
        self.org_id  = 2
        self.event_type = "academic"
        self.lat     = 35.9049
        self.lon     = -79.0469
        self.params  = {
            "start_date": datetime.utcnow().date().isoformat(),
            "end_date": (datetime.utcnow() + timedelta(days=90)).date().isoformat(),
            "per_page": 100
        }

    def run_and_post(self):
        print(f"🔎 Fetching JSON: {self.url}")
        try:
            res = requests.get(self.url, params=self.params, timeout=10)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            print(f"❌ UNC JSON fetch error: {e}")
            return

        events = data.get("events", [])
        print(f"✅ Received {len(events)} UNC JSON events")

        payloads = []
        for ev in events:
            title = ev.get("title")
            start = ev.get("start_date")  # ISO string
            end   = ev.get("end_date") or start
            url   = ev.get("url")
            loc   = ev.get("venue", {}).get("name", "UNC Chapel Hill")

            payloads.append({
                "title":         title,
                "description":   (ev.get("description") or "")[:500], 
                "start_date":    start,
                "end_date":      end,
                "location_name": loc,
                "latitude":      self.lat,
                "longitude":     self.lon,
                "organization_id": self.org_id,
                "event_type":    self.event_type,
                "source_url":    url
            })

        if payloads:
            stats = batch_post(payloads)
            print("UNC JSON batch:", stats)
