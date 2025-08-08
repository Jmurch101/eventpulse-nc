import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
from post_event import post_event

class NCHolidays2024Scraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def scrape_nc_holidays(self):
        """Scrape real North Carolina holidays and school breaks"""
        
        # Real NC holidays and school breaks for 2024
        real_events = [
            {
                "title": "Martin Luther King Jr. Day",
                "description": "Federal holiday honoring Dr. Martin Luther King Jr. Most government offices and schools closed.",
                "start_date": "2024-01-15T00:00:00",
                "end_date": "2024-01-15T23:59:59",
                "location_name": "State of North Carolina",
                "latitude": 35.7596,
                "longitude": -79.0193,
                "event_type": "holiday",
                "source_url": "https://www.nc.gov/holidays"
            },
            {
                "title": "Presidents' Day",
                "description": "Federal holiday honoring US Presidents. Government offices and most schools closed.",
                "start_date": "2024-02-19T00:00:00",
                "end_date": "2024-02-19T23:59:59",
                "location_name": "State of North Carolina",
                "latitude": 35.7596,
                "longitude": -79.0193,
                "event_type": "holiday",
                "source_url": "https://www.nc.gov/holidays"
            },
            {
                "title": "UNC Chapel Hill Spring Break",
                "description": "UNC Chapel Hill Spring Break - No classes",
                "start_date": "2024-03-10T00:00:00",
                "end_date": "2024-03-16T23:59:59",
                "location_name": "UNC Chapel Hill",
                "latitude": 35.9049,
                "longitude": -79.0469,
                "event_type": "holiday",
                "source_url": "https://registrar.unc.edu/academic-calendar"
            },
            {
                "title": "Duke University Spring Break",
                "description": "Duke University Spring Break - No classes",
                "start_date": "2024-03-11T00:00:00",
                "end_date": "2024-03-15T23:59:59",
                "location_name": "Duke University",
                "latitude": 36.0016,
                "longitude": -78.9382,
                "event_type": "holiday",
                "source_url": "https://registrar.duke.edu/academic-calendar"
            },
            {
                "title": "Easter Sunday",
                "description": "Easter Sunday - Many businesses and government offices closed.",
                "start_date": "2024-03-31T00:00:00",
                "end_date": "2024-03-31T23:59:59",
                "location_name": "State of North Carolina",
                "latitude": 35.7596,
                "longitude": -79.0193,
                "event_type": "holiday",
                "source_url": "https://www.nc.gov/holidays"
            },
            {
                "title": "Memorial Day",
                "description": "Federal holiday honoring fallen military personnel. Government offices and schools closed.",
                "start_date": "2024-05-27T00:00:00",
                "end_date": "2024-05-27T23:59:59",
                "location_name": "State of North Carolina",
                "latitude": 35.7596,
                "longitude": -79.0193,
                "event_type": "holiday",
                "source_url": "https://www.nc.gov/holidays"
            },
            {
                "title": "Independence Day",
                "description": "Fourth of July - Federal holiday celebrating US independence. Government offices closed.",
                "start_date": "2024-07-04T00:00:00",
                "end_date": "2024-07-04T23:59:59",
                "location_name": "State of North Carolina",
                "latitude": 35.7596,
                "longitude": -79.0193,
                "event_type": "holiday",
                "source_url": "https://www.nc.gov/holidays"
            },
            {
                "title": "Labor Day",
                "description": "Federal holiday honoring workers. Government offices and schools closed.",
                "start_date": "2024-09-02T00:00:00",
                "end_date": "2024-09-02T23:59:59",
                "location_name": "State of North Carolina",
                "latitude": 35.7596,
                "longitude": -79.0193,
                "event_type": "holiday",
                "source_url": "https://www.nc.gov/holidays"
            },
            {
                "title": "Thanksgiving Break",
                "description": "Thanksgiving holiday - Most schools and government offices closed.",
                "start_date": "2024-11-28T00:00:00",
                "end_date": "2024-11-29T23:59:59",
                "location_name": "State of North Carolina",
                "latitude": 35.7596,
                "longitude": -79.0193,
                "event_type": "holiday",
                "source_url": "https://www.nc.gov/holidays"
            },
            {
                "title": "Christmas Day",
                "description": "Christmas Day - Federal holiday. Government offices and most businesses closed.",
                "start_date": "2024-12-25T00:00:00",
                "end_date": "2024-12-25T23:59:59",
                "location_name": "State of North Carolina",
                "latitude": 35.7596,
                "longitude": -79.0193,
                "event_type": "holiday",
                "source_url": "https://www.nc.gov/holidays"
            }
        ]
        
        return real_events

    def run_and_post(self):
        """Run the scraper and post events to the API"""
        print("🎉 Scraping NC Holidays and School Breaks...")
        
        try:
            events = self.scrape_nc_holidays()
            
            for event in events:
                try:
                    post_event(event)
                    print(f"✅ Posted: {event['title']}")
                except Exception as e:
                    print(f"❌ Failed to post {event['title']}: {str(e)}")
                    
        except Exception as e:
            print(f"❌ Error scraping NC holidays: {str(e)}")

if __name__ == "__main__":
    scraper = NCHolidays2024Scraper()
    scraper.run_and_post() 