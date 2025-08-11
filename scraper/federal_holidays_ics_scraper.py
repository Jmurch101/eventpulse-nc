from ics_scrapers import ICSUtils
from api_client import batch_post


class FederalHolidaysICSScraper:
    # Public ICS feed for US Federal Holidays
    url = "https://www.calendarlabs.com/ical-calendar/ics/76/US_Holidays.ics"
    org_id = 99
    org_name = "United States Federal Holidays"
    lat, lon = 38.9072, -77.0369
    event_type = "holiday"

    def run_and_post(self):
        events = ICSUtils.parse_ics(
            self.url,
            org_id=self.org_id,
            org_name=self.org_name,
            lat=self.lat,
            lon=self.lon,
            event_type=self.event_type,
        )
        if events:
            print("Federal Holidays ICS batch:", batch_post(events))
        else:
            print("Federal Holidays ICS: no events parsed")


if __name__ == "__main__":
    FederalHolidaysICSScraper().run_and_post()

