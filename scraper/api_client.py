import os, requests

API_BASE = os.getenv('API_URL', 'http://localhost:3001')

def post_event(event):
    try:
        res = requests.post(f"{API_BASE}/api/events", json=event, timeout=15)
        if res.status_code in (200,201):
            return True
        print(f"❌ Failed to post: {res.status_code} {res.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    return False

def batch_post(events):
    try:
        res = requests.post(f"{API_BASE}/api/events/batch", json={'events': events}, timeout=30)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"❌ Batch error: {e}")
        return {"error": str(e)}
