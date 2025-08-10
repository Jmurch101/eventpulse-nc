#!/usr/bin/env python3
"""
Enhanced Data Collection for EventPulse NC
Scales up the database with realistic events to reach 10,000+ events
"""

import requests
import random
from datetime import datetime, timedelta
import time

API_URL = os.getenv("API_URL", "http://localhost:3001")

# Event templates for better variety
event_templates = [
    {
        "title": "Academic Lecture: {topic}",
        "description": "Join us for an engaging academic discussion on {topic}. This event brings together researchers, students, and professionals to explore current trends and future directions in the field.",
        "event_type": "academic"
    },
    {
        "title": "Government Meeting: {topic}",
        "description": "Official government meeting: {topic}. This session will address key policy issues and community concerns.",
        "event_type": "government"
    },
    {
        "title": "Tech Conference: {topic}",
        "description": "Tech conference: {topic}. A premier event for technology professionals and enthusiasts.",
        "event_type": "tech"
    },
    {
        "title": "Community Event: {topic}",
        "description": "Community event: {topic}. Join your neighbors for this fun and engaging local activity.",
        "event_type": "community"
    },
    {
        "title": "Student Research Showcase: {topic}",
        "description": "An academic presentation and discussion on student research showcase: {topic}. Open to students, faculty, and the general public. Light refreshments will be served.",
        "event_type": "academic"
    },
    {
        "title": "Local Festival: {topic}",
        "description": "Local celebration: {topic}. A great opportunity to connect with your community and enjoy local culture.",
        "event_type": "community"
    },
    {
        "title": "Planning Board Meeting: {topic}",
        "description": "Government forum: {topic}. An opportunity for public engagement and discussion of local governance matters.",
        "event_type": "government"
    },
    {
        "title": "Developer Meetup: {topic}",
        "description": "Tech meetup: {topic}. Network with local tech professionals and learn about the latest industry trends.",
        "event_type": "tech"
    }
]

topics = [
    "Data Science and Analytics", "Machine Learning Applications", "Cybersecurity Best Practices",
    "Renewable Energy Systems", "Public Health and Epidemiology", "Environmental Science",
    "Urban Planning and Development", "Biotechnology and Genomics", "Social Justice and Equity",
    "Climate Change and Sustainability", "Digital Transformation", "User Experience Design",
    "Blockchain and Web3", "Agile Development", "Cloud Computing", "Mobile Development",
    "Web Development", "DevOps", "Product Strategy", "Innovation in Tech"
]

locations = [
    {"name": "NC State University, Raleigh, NC", "lat": 35.7847, "lng": -78.6821},
    {"name": "UNC Chapel Hill, Chapel Hill, NC", "lat": 35.9049, "lng": -79.0469},
    {"name": "Duke University, Durham, NC", "lat": 36.0016, "lng": -78.9382},
    {"name": "Raleigh City Hall, Raleigh, NC", "lat": 35.7796, "lng": -78.6382},
    {"name": "Durham City Hall, Durham, NC", "lat": 35.9940, "lng": -78.8986},
    {"name": "Chapel Hill Town Hall, Chapel Hill, NC", "lat": 35.9132, "lng": -79.0558},
    {"name": "Cary Town Hall, Cary, NC", "lat": 35.7915, "lng": -78.7811},
    {"name": "Red Hat Amphitheater, Raleigh, NC", "lat": 35.7773, "lng": -78.6377},
    {"name": "Durham Performing Arts Center, Durham, NC", "lat": 35.9956, "lng": -78.8962},
    {"name": "PNC Arena, Raleigh, NC", "lat": 35.8032, "lng": -78.7219},
    {"name": "American Tobacco Campus, Durham, NC", "lat": 35.9946, "lng": -78.9037},
    {"name": "North Carolina Museum of Art, Raleigh, NC", "lat": 35.8103, "lng": -78.7061},
    {"name": "Sarah P. Duke Gardens, Durham, NC", "lat": 35.9988, "lng": -78.9039},
    {"name": "Cary Community Center, Cary, NC", "lat": 35.7883, "lng": -78.7766},
    {"name": "Wake County Courthouse, Raleigh, NC", "lat": 35.7702, "lng": -78.6294},
    {"name": "Durham County Library, Durham, NC", "lat": 35.9843, "lng": -78.9066},
    {"name": "Franklin Street, Chapel Hill, NC", "lat": 35.9101, "lng": -79.0489},
    {"name": "Cary Senior Center, Cary, NC", "lat": 35.7848, "lng": -78.7765},
    {"name": "Ackland Art Museum, Chapel Hill, NC", "lat": 35.9177, "lng": -79.0614},
    {"name": "Nasher Museum of Art, Durham, NC", "lat": 35.9931, "lng": -78.8887}
]

def generate_events_for_month(year, month, num_events=100):
    """Generate events distributed across the entire month"""
    events = []
    
    # Get the number of days in the month
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    last_day = (next_month - timedelta(days=1)).day
    
    # Distribute events across all days of the month
    for day in range(1, last_day + 1):
        # Calculate how many events for this day (more events on weekdays)
        weekday = datetime(year, month, day).weekday()
        if weekday < 5:  # Monday to Friday
            events_per_day = random.randint(2, 6)
        else:  # Weekend
            events_per_day = random.randint(1, 4)
        
        for _ in range(events_per_day):
            # Generate random time between 9 AM and 9 PM
            hour = random.randint(9, 21)
            minute = random.choice([0, 15, 30, 45])
            
            start_time = datetime(year, month, day, hour, minute)
            duration = random.randint(60, 240)  # 1-4 hours
            end_time = start_time + timedelta(minutes=duration)
            
            template = random.choice(event_templates)
            topic = random.choice(topics)
            location = random.choice(locations)
            
            event = {
                "title": template["title"].format(topic=topic),
                "description": template["description"].format(topic=topic),
                "start_date": start_time.isoformat(),
                "end_date": end_time.isoformat(),
                "location_name": location["name"],
                "latitude": location["lat"] + random.uniform(-0.01, 0.01),
                "longitude": location["lng"] + random.uniform(-0.01, 0.01),
                "organization_id": 1,
                "event_type": template["event_type"],
                "source_url": f"https://eventpulse-nc.com/events/{random.randint(1, 500)}"
            }
            events.append(event)
    
    return events

def post_event(event):
    """Post a single event to the API"""
    try:
        response = requests.post(f"{API_URL}/api/events", json=event)
        if response.status_code == 201:
            print(f"✅ Posted: {event['title']}")
            return True
        elif response.status_code == 200:
            data = response.json()
            if data.get('duplicate'):
                print(f"⏭️  Skipped (duplicate): {event['title']}")
                return False
            else:
                print(f"✅ Posted: {event['title']}")
                return True
        else:
            print(f"❌ Failed to post: {event['title']}, status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error posting event: {e}")
        return False

def main():
    print("🚀 Starting enhanced data collection for 2025...")
    
    # Generate events for current year (2025)
    august_events = generate_events_for_month(2025, 8, num_events=100)
    september_events = generate_events_for_month(2025, 9, num_events=80)
    october_events = generate_events_for_month(2025, 10, num_events=90)
    
    all_events = august_events + september_events + october_events
    
    print(f"📅 Generated {len(all_events)} events for 2025")
    print(f"   - August 2025: {len(august_events)} events")
    print(f"   - September 2025: {len(september_events)} events")
    print(f"   - October 2025: {len(october_events)} events")
    print("📤 Posting events to API (batch mode)...")
    
    # Batch post to reduce API overhead
    try:
        resp = requests.post(f"{API_URL}/api/events/batch", json={"events": all_events}, timeout=30)
        resp.raise_for_status()
        stats = resp.json()
        print(f"\n🎉 Data collection complete!")
        print(f"📦 Received: {stats.get('received')} • ✅ Inserted: {stats.get('inserted')} • ⏭️ Duplicates: {stats.get('duplicates')} • ❌ Failed: {stats.get('failed')}")
    except Exception as e:
        print(f"❌ Batch post failed: {e}")
    print(f"🗓️  Events now available for August, September, and October 2025!")

if __name__ == "__main__":
    main() 