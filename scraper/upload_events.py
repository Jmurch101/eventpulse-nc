import requests
from datetime import datetime

# API endpoint
API_URL = "http://localhost:5050/api/events"

# Sample event (this will be dynamic later from your scraper)
event = {
    "title": "Sample Event from Python",
    "description": "Posted using Python script",
    "start_date": "2025-07-24T09:00:00Z",
    "end_date": "2025-07-24T12:00:00Z",
    "location_name": "Chapel Hill",
    "latitude": 35.9132,
    "longitude": -79.0558,
    "organization_id": 2,
    "event_type": "workshop",
    "source_url": "https://example.edu/events/sample"
}

# Send event to API
try:
    response = requests.post(API_URL, json=event)
    if response.status_code == 201:
        print("✅ Event posted successfully!")
        print(response.json())
    else:
        print(f"❌ Failed to post event: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Error sending request: {e}")
