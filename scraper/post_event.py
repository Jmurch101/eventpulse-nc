# scraper/post_event.py

import requests

API_URL = "http://localhost:3001/api/events"

def post_event(event):
    try:
        response = requests.post(API_URL, json=event)
        if response.status_code == 201:
            print(f"✅ Posted: {event['title']}")
            return True
        elif response.status_code == 200:
            # This means the event was a duplicate
            data = response.json()
            if data.get('duplicate'):
                print(f"⏭️  Skipped (duplicate): {event['title']}")
                return False
            else:
                print(f"✅ Posted: {event['title']}")
                return True
        else:
            print(f"❌ Failed to post: {event['title']}, status: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Error posting event: {e}")
        return False
