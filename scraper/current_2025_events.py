#!/usr/bin/env python3
"""
Current 2025 Events for EventPulse NC
Generates events for the next 3 months from today (2025)
"""

import requests
import random
from datetime import datetime, timedelta
import time

API_URL = "http://localhost:3001/api/events"

# Event templates for current events
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
        "description": "An academic presentation and discussion on student research showcase: {topic}. Open to students, faculty, and the general public.",
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
    {"name": "PNC Arena, Raleigh, NC", "lat": 35.8032, "lng": -78.7219}
]

def generate_events_for_date_range(start_date, end_date, events_per_day=3):
    """Generate events for a specific date range"""
    events = []
    current_date = start_date
    
    while current_date <= end_date:
        # Generate 2-4 events per day (more on weekdays)
        weekday = current_date.weekday()
        if weekday < 5:  # Monday to Friday
            daily_events = random.randint(2, 4)
        else:  # Weekend
            daily_events = random.randint(1, 3)
        
        for _ in range(daily_events):
            # Generate random time between 9 AM and 9 PM
            hour = random.randint(9, 21)
            minute = random.choice([0, 15, 30, 45])
            
            start_time = datetime(current_date.year, current_date.month, current_date.day, hour, minute)
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
                "source_url": f"https://eventpulse-nc.com/events/{random.randint(1, 1000)}"
            }
            events.append(event)
        
        current_date += timedelta(days=1)
    
    return events

def post_event(event):
    """Post a single event to the API"""
    try:
        response = requests.post(API_URL, json=event)
        if response.status_code == 201:
            print(f"✅ Posted: {event['title']} - {event['start_date'][:10]}")
            return True
        elif response.status_code == 200:
            data = response.json()
            if data.get('duplicate'):
                print(f"⏭️  Skipped (duplicate): {event['title']}")
                return False
            else:
                print(f"✅ Posted: {event['title']} - {event['start_date'][:10]}")
                return True
        else:
            print(f"❌ Failed to post: {event['title']}, status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error posting event: {e}")
        return False

def cleanup_old_events():
    """Remove events older than 3 months"""
    try:
        response = requests.post(f"{API_URL.replace('/events', '/events/cleanup-old')}")
        if response.status_code == 200:
            print("🧹 Cleaned up old events")
        else:
            print("⚠️  Could not cleanup old events")
    except Exception as e:
        print(f"⚠️  Cleanup error: {e}")

def main():
    print("🚀 Creating current 2025 events for EventPulse NC...")
    
    # Calculate date range: next 3 months from today
    today = datetime.now()
    start_date = today + timedelta(days=1)  # Start from tomorrow
    end_date = today + timedelta(days=90)   # 3 months from today
    
    print(f"📅 Generating events from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    # Generate events for the 3-month period
    events = generate_events_for_date_range(start_date, end_date)
    
    print(f"📅 Generated {len(events)} events for the next 3 months")
    print("📤 Posting events to API...")
    
    successful_posts = 0
    skipped_posts = 0
    
    for i, event in enumerate(events, 1):
        if post_event(event):
            successful_posts += 1
        else:
            skipped_posts += 1
        
        # Add a small delay to avoid overwhelming the API
        if i % 10 == 0:
            time.sleep(0.1)
    
    print(f"\n🎉 Current 2025 events creation complete!")
    print(f"✅ Successfully posted: {successful_posts} events")
    print(f"⏭️  Skipped (duplicates): {skipped_posts} events")
    print(f"📊 Total current events in database: {successful_posts}")
    print(f"🗓️  Events now available for the next 3 months!")
    print(f"🔄 Next update recommended in 15 days")

if __name__ == "__main__":
    main() 