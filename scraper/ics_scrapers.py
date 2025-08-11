"""
ICS helpers with resilient parsing. Tries `ics` first; falls back to `icalendar` for
feeds with malformed events. Ensures end >= start and pads default duration.
"""

import requests
from datetime import timedelta, datetime
from api_client import batch_post


class ICSUtils:
    @staticmethod
    def parse_ics(url, org_id, org_name, lat, lon, event_type):
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/calendar, text/plain, */*",
            "Referer": url,
        }
        try:
            r = requests.get(url, headers=headers, timeout=15)
            r.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch ICS feed {url}: {e}")
            return []

        # Some endpoints return HTML when blocked or mis-parameterized
        ctype = r.headers.get("Content-Type", "").lower()
        if "text/html" in ctype and not r.text.strip().startswith("BEGIN:VEVENT") and not r.text.strip().startswith("BEGIN:VCALENDAR"):
            print(f"⚠️  Non-ICS content received from {url} (Content-Type: {ctype}). Skipping.")
            return []

        # Strategy 1: try `ics` library
        try:
            from ics import Calendar as ICSCalendar  # type: ignore
            cal = ICSCalendar(r.text)
            events = []
            for comp in cal.events:
                title = (getattr(comp, "name", None) or "Untitled").strip()
                dtstart = comp.begin.datetime if getattr(comp, "begin", None) else None
                dtend = comp.end.datetime if getattr(comp, "end", None) else None
                if dtstart and not dtend:
                    dtend = dtstart + timedelta(hours=1)
                location = (getattr(comp, "location", None) or org_name).strip()

                if not dtstart:
                    continue
                if dtend and dtend < dtstart:
                    # Fix inverted intervals
                    dtstart, dtend = dtend, dtstart
                if not dtend:
                    dtend = dtstart + timedelta(hours=1)

                events.append({
                    "title": title,
                    "description": (getattr(comp, "description", None) or "").strip()[:500],
                    "start_date": dtstart.isoformat(),
                    "end_date": dtend.isoformat(),
                    "location_name": location,
                    "latitude": lat,
                    "longitude": lon,
                    "organization_id": org_id,
                    "event_type": event_type,
                    "source_url": url,
                })
            print(f"✅ Parsed {len(events)} events from ICS feed {url}")
            return events
        except Exception as primary_error:
            print(f"⚠️  ICS parse issue with `ics` library: {primary_error}. Falling back to `icalendar`.")

        # Strategy 2: fallback to `icalendar` library
        try:
            from icalendar import Calendar as ICalCalendar  # type: ignore
        except Exception as e:
            print("❌ Fallback parser unavailable: please install `icalendar`.", e)
            return []

        try:
            cal = ICalCalendar.from_ical(r.text)
        except Exception as e:
            print(f"❌ Failed to parse ICS with icalendar: {e}")
            return []

        events = []
        for comp in cal.walk():
            if comp.name != "VEVENT":
                continue
            title = str(comp.get("summary") or "Untitled")
            raw_start = comp.get("dtstart")
            raw_end = comp.get("dtend")
            location = str(comp.get("location") or org_name)
            description = str(comp.get("description") or "")

            # Extract datetime objects (icalendar wraps in vDDD types)
            dtstart = getattr(raw_start, "dt", None)
            dtend = getattr(raw_end, "dt", None)
            if isinstance(dtstart, datetime) is False and dtstart is not None:
                # Convert date to datetime at midnight
                dtstart = datetime.combine(dtstart, datetime.min.time())
            if isinstance(dtend, datetime) is False and dtend is not None:
                dtend = datetime.combine(dtend, datetime.min.time())

            if dtstart is None:
                continue
            if dtend is None:
                dtend = dtstart + timedelta(hours=1)
            if dtend < dtstart:
                # Swap or pad when calendars are malformed
                dtstart, dtend = dtend, dtstart
                if dtend < dtstart:
                    dtend = dtstart + timedelta(hours=1)

            events.append({
                "title": title.strip(),
                "description": description.strip()[:500],
                "start_date": dtstart.isoformat(),
                "end_date": dtend.isoformat(),
                "location_name": location.strip() or org_name,
                "latitude": lat,
                "longitude": lon,
                "organization_id": org_id,
                "event_type": event_type,
                "source_url": url,
            })
        print(f"✅ Parsed {len(events)} events from ICS feed {url} (fallback)")
        return events


class UNCICSScraper:
    def run_and_post(self):
        url = "https://events.unc.edu/calendar.ics"
        events = ICSUtils.parse_ics(
            url, org_id=2, org_name="UNC Chapel Hill", lat=35.9049, lon=-79.0469, event_type="academic"
        )
        if events:
            print("UNC ICS batch:", batch_post(events))


class DukeICSScraper:
    def run_and_post(self):
        url = "https://calendar.duke.edu/calendar.ics"
        events = ICSUtils.parse_ics(
            url, org_id=3, org_name="Duke University", lat=36.0014, lon=-78.9382, event_type="academic"
        )
        if events:
            print("Duke ICS batch:", batch_post(events))


class HolidayListScraper:
    def run_and_post(self):
        # Minimal example using fixed US holidays; not used by default runner.
        # Requires 'holidays' package if enabled.
        try:
            import holidays  # type: ignore
        except Exception:
            print("⚠️ 'holidays' package not installed; skipping HolidayListScraper")
            return
        us_holidays = holidays.US()
        events = []
        for date_obj, name in us_holidays.items():
            start_dt = datetime.combine(date_obj, datetime.min.time())
            end_dt = datetime.combine(date_obj, datetime.max.time())
            events.append({
                "title": str(name),
                "description": "Public holiday in the U.S.",
                "start_date": start_dt.isoformat(),
                "end_date": end_dt.isoformat(),
                "location_name": "North Carolina, USA",
                "latitude": 35.7596,
                "longitude": -79.0193,
                "organization_id": 99,
                "event_type": "holiday",
                "source_url": "https://www.opm.gov/policy-data-oversight/snow-dismissal-procedures/federal-holidays/"
            })
        if events:
            print("US Holidays batch:", batch_post(events))
