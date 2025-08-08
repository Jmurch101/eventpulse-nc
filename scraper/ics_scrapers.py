# scraper/ics_scrapers.py

import requests
from icalendar import Calendar
from datetime import datetime, timedelta
from post_event import post_event
import holidays

class ICSUtils:
    @staticmethod
    def parse_ics(url, org_id, org_name, lat, lon, event_type):
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch ICS feed {url}: {e}")
            return []

        cal = Calendar.from_ical(r.text)
        events = []
        for comp in cal.walk():
            if comp.name != "VEVENT":
                continue
            title = str(comp.get('summary'))
            dtstart = comp.decoded('dtstart')
            dtend = comp.decoded('dtend') if comp.get('dtend') else dtstart + timedelta(hours=1)
            location = str(comp.get('location')) or org_name

            events.append({
                "title": title,
                "description": "",
                "start_date": dtstart.isoformat(),
                "end_date": dtend.isoformat(),
                "location_name": location,
                "latitude": lat,
                "longitude": lon,
                "organization_id": org_id,
                "event_type": event_type,
                "source_url": url
            })
        print(f"✅ Parsed {len(events)} events from ICS feed {url}")
        return events

class UNCICSScraper:
    def run_and_post(self):
        url = "https://events.unc.edu/calendar.ics"
        events = ICSUtils.parse_ics(
            url, org_id=2, org_name="UNC Chapel Hill", lat=35.9049, lon=-79.0469, event_type="academic"
        )
        for e in events:
            post_event(e)

class DukeICSScraper:
    def run_and_post(self):
        url = "https://calendar.duke.edu/calendar.ics"
        events = ICSUtils.parse_ics(
            url, org_id=3, org_name="Duke University", lat=36.0014, lon=-78.9382, event_type="academic"
        )
        for e in events:
            post_event(e)

class HolidayListScraper:
    def run_and_post(self):
        us_holidays = holidays.US()  # Requires: pip install holidays
        count = 0
        for date_obj, name in us_holidays.items():
            event = {
                "title": name,
                "description": "Public holiday in the U.S.",
                "start_date": datetime.combine(date_obj, datetime.min.time()).isoformat(),
                "end_date": datetime.combine(date_obj, datetime.max.time()).isoformat(),
                "location_name": "North Carolina, USA",
                "latitude": 35.7596,
                "longitude": -79.0193,
                "organization_id": 99,
                "event_type": "holiday",
                "source_url": url  # Not applicable
            }
            post_event(event)
            count += 1
        print(f"✅ Posted {count} holidays")
