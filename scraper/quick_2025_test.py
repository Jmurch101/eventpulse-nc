#!/usr/bin/env python3
"""
Quick test to create 2025 events
"""

import requests
from datetime import datetime, timedelta

API_URL = "http://localhost:3001/api/events"

def create_test_2025_events():
    """Create a few test events for 2025"""
    
    # Create 5 test events for August 2025
    test_events = [
        {
            "title": "Test Event 1 - August 2025",
            "description": "This is a test event for August 1, 2025",
            "start_date": "2025-08-01T10:00:00",
            "end_date": "2025-08-01T12:00:00",
            "location_name": "Test Location 1, Raleigh, NC",
            "latitude": 35.7796,
            "longitude": -78.6382,
            "organization_id": 1,
            "event_type": "academic",
            "source_url": "https://test.com/events/1"
        },
        {
            "title": "Test Event 2 - August 2025",
            "description": "This is a test event for August 2, 2025",
            "start_date": "2025-08-02T14:00:00",
            "end_date": "2025-08-02T16:00:00",
            "location_name": "Test Location 2, Durham, NC",
            "latitude": 35.9940,
            "longitude": -78.8986,
            "organization_id": 1,
            "event_type": "government",
            "source_url": "https://test.com/events/2"
        },
        {
            "title": "Test Event 3 - August 2025",
            "description": "This is a test event for August 3, 2025",
            "start_date": "2025-08-03T18:00:00",
            "end_date": "2025-08-03T20:00:00",
            "location_name": "Test Location 3, Chapel Hill, NC",
            "latitude": 35.9049,
            "longitude": -79.0469,
            "organization_id": 1,
            "event_type": "tech",
            "source_url": "https://test.com/events/3"
        }
    ]
    
    print("🧪 Creating test 2025 events...")
    
    for i, event in enumerate(test_events, 1):
        try:
            response = requests.post(API_URL, json=event)
            if response.status_code == 201:
                print(f"✅ Created: {event['title']} - {event['start_date']}")
            elif response.status_code == 200:
                data = response.json()
                if data.get('duplicate'):
                    print(f"⏭️  Skipped (duplicate): {event['title']}")
                else:
                    print(f"✅ Created: {event['title']} - {event['start_date']}")
            else:
                print(f"❌ Failed: {event['title']}, status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("🎉 Test complete!")

if __name__ == "__main__":
    create_test_2025_events() 