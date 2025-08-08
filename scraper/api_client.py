import requests

API_URL = "http://localhost:5050/api/events"

def post_event(event):
    try:
        res = requests.post(API_URL, json=event)
        if res.status_code == 201:
            print(f"✅ Event '{event['title']}' posted.")
        else:
            print(f"❌ Failed to post: {res.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
