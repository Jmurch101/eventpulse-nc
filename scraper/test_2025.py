#!/usr/bin/env python3
"""
Test script to generate 2025 events
"""

import requests
import random
from datetime import datetime, timedelta

API_URL = "http://localhost:3001/api/events"

def generate_test_events():
    """Generate a few test events for 2025"""
    events = []
    
    # Generate events for August 2025
    for day in range(1, 6):  # Just first 5 days
        for hour in [10, 14, 18]:  # 3 events per day
            start_time = datetime(2025, 8, day, hour, 0)
            end_time = start_time + timedelta(hours=2)
            
            event = {
                "title": f"Test Event {day}-{hour}",
                "description": f"This is a test event for August {day}, 2025 at {hour}:00",
                "start_date": start_time.isoformat(),
                "end_date": end_time.isoformat(),
                "location_name": "Test Location, Raleigh, NC",
                "latitude": 35.7796,
                "longitude": -78.6382,
                "organization_id": 1,
                "event_type": "academic",
                "source_url": f"https://test.com/events/{day}-{hour}"
            }
            events.append(event)
    
    return events

def post_event(event):
    """Post a single event to the API"""
    try:
        response = requests.post(API_URL, json=event)
        if response.status_code == 201:
            print(f"✅ Posted: {event['title']} - {event['start_date']}")
            return True
        elif response.status_code == 200:
            data = response.json()
            if data.get('duplicate'):
                print(f"⏭️  Skipped (duplicate): {event['title']}")
                return False
            else:
                print(f"✅ Posted: {event['title']} - {event['start_date']}")
                return True
        else:
            print(f"❌ Failed to post: {event['title']}, status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error posting event: {e}")
        return False

def main():
    print("🧪 Testing 2025 event generation...")
    
    events = generate_test_events()
    
    print(f"📅 Generated {len(events)} test events for 2025")
    print("📤 Posting events to API...")
    
    successful_posts = 0
    
    for event in events:
        if post_event(event):
            successful_posts += 1
    
    print(f"\n🎉 Test complete!")
    print(f"✅ Successfully posted: {successful_posts} events")

if __name__ == "__main__":
    main() 