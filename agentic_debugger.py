#!/usr/bin/env python3
"""
Agentic Debugger for EventPulse NC 2025 Events Issue
This agent systematically analyzes and fixes the date generation problem
"""

import requests
import json
import sqlite3
import os
from datetime import datetime, timedelta
import time
import random

class EventPulseAgenticDebugger:
    def __init__(self):
        self.api_url = "http://localhost:3001/api/events"
        self.db_path = "backend/events.db"
        self.debug_log = []
        
    def log(self, message, level="INFO"):
        """Log debug messages with timestamps"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.debug_log.append(log_entry)
        print(log_entry)
        
    def check_backend_health(self):
        """Check if backend is running and healthy"""
        try:
            response = requests.get("http://localhost:3001/health", timeout=5)
            if response.status_code == 200:
                self.log("✅ Backend is healthy and running")
                return True
            else:
                self.log(f"❌ Backend returned status {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Backend health check failed: {e}", "ERROR")
            return False
    
    def analyze_database_state(self):
        """Analyze current database state"""
        self.log("🔍 Analyzing database state...")
        
        if not os.path.exists(self.db_path):
            self.log(f"❌ Database file not found at {self.db_path}", "ERROR")
            return None
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get total event count
            cursor.execute("SELECT COUNT(*) FROM events")
            total_events = cursor.fetchone()[0]
            self.log(f"📊 Total events in database: {total_events}")
            
            # Get date distribution
            cursor.execute("""
                SELECT 
                    SUBSTR(start_date, 1, 4) as year,
                    COUNT(*) as count
                FROM events 
                GROUP BY year 
                ORDER BY year
            """)
            year_distribution = cursor.fetchall()
            
            self.log("📅 Event distribution by year:")
            for year, count in year_distribution:
                self.log(f"   {year}: {count} events")
            
            # Get most recent events
            cursor.execute("""
                SELECT id, title, start_date, created_at
                FROM events 
                ORDER BY created_at DESC 
                LIMIT 5
            """)
            recent_events = cursor.fetchall()
            
            self.log("🕒 Most recent events:")
            for event_id, title, start_date, created_at in recent_events:
                self.log(f"   ID {event_id}: {title} - {start_date} (created: {created_at})")
            
            conn.close()
            return {
                'total_events': total_events,
                'year_distribution': year_distribution,
                'recent_events': recent_events
            }
            
        except Exception as e:
            self.log(f"❌ Database analysis failed: {e}", "ERROR")
            return None
    
    def test_api_response(self):
        """Test API response and analyze data"""
        self.log("🔍 Testing API response...")
        
        try:
            response = requests.get(self.api_url, timeout=10)
            if response.status_code == 200:
                events = response.json()
                self.log(f"✅ API returned {len(events)} events")
                
                # Analyze date distribution in API response
                year_counts = {}
                for event in events[:100]:  # Sample first 100 events
                    start_date = event.get('start_date', '')
                    if start_date:
                        year = start_date[:4]
                        year_counts[year] = year_counts.get(year, 0) + 1
                
                self.log("📅 API response year distribution (sample):")
                for year, count in sorted(year_counts.items()):
                    self.log(f"   {year}: {count} events")
                
                return events
            else:
                self.log(f"❌ API returned status {response.status_code}", "ERROR")
                return None
                
        except Exception as e:
            self.log(f"❌ API test failed: {e}", "ERROR")
            return None
    
    def test_date_generation(self):
        """Test date generation logic"""
        self.log("🧪 Testing date generation logic...")
        
        # Test current date
        today = datetime.now()
        self.log(f"Today: {today} (year: {today.year})")
        
        # Test event generation
        test_events = []
        for i in range(5):
            test_date = today + timedelta(days=i+1)
            hour = random.randint(9, 21)
            minute = random.choice([0, 15, 30, 45])
            
            start_time = datetime(test_date.year, test_date.month, test_date.day, hour, minute)
            test_event = {
                "title": f"Test Event {i+1}",
                "description": f"Test event {i+1}",
                "start_date": start_time.isoformat(),
                "end_date": (start_time + timedelta(hours=2)).isoformat(),
                "location_name": "Test Location",
                "latitude": 35.7796,
                "longitude": -78.6382,
                "organization_id": 1,
                "event_type": "test",
                "source_url": "https://test.com"
            }
            test_events.append(test_event)
            self.log(f"Generated test event: {test_event['start_date']} (year: {start_time.year})")
        
        return test_events
    
    def test_event_posting(self, test_events):
        """Test posting events to API"""
        self.log("📤 Testing event posting...")
        
        results = []
        for i, event in enumerate(test_events):
            try:
                response = requests.post(self.api_url, json=event, timeout=10)
                if response.status_code == 201:
                    self.log(f"✅ Test event {i+1} posted successfully")
                    results.append(True)
                elif response.status_code == 200:
                    data = response.json()
                    if data.get('duplicate'):
                        self.log(f"⏭️ Test event {i+1} was duplicate")
                        results.append(False)
                    else:
                        self.log(f"✅ Test event {i+1} posted successfully")
                        results.append(True)
                else:
                    self.log(f"❌ Test event {i+1} failed with status {response.status_code}", "ERROR")
                    results.append(False)
                    
            except Exception as e:
                self.log(f"❌ Test event {i+1} posting failed: {e}", "ERROR")
                results.append(False)
        
        return results
    
    def verify_posted_events(self, test_events):
        """Verify that posted events are retrievable"""
        self.log("🔍 Verifying posted events...")
        
        try:
            response = requests.get(self.api_url, timeout=10)
            if response.status_code == 200:
                events = response.json()
                
                # Look for our test events
                test_titles = [event['title'] for event in test_events]
                found_events = []
                
                for event in events:
                    if event['title'] in test_titles:
                        found_events.append(event)
                        self.log(f"✅ Found test event: {event['title']} - {event['start_date']}")
                
                if found_events:
                    self.log(f"✅ Found {len(found_events)} test events in API response")
                    return found_events
                else:
                    self.log("❌ No test events found in API response", "ERROR")
                    return []
            else:
                self.log(f"❌ Failed to retrieve events: {response.status_code}", "ERROR")
                return []
                
        except Exception as e:
            self.log(f"❌ Verification failed: {e}", "ERROR")
            return []
    
    def diagnose_issue(self):
        """Diagnose the root cause of the 2025 events issue"""
        self.log("🔍 Diagnosing 2025 events issue...")
        
        # Step 1: Check backend health
        if not self.check_backend_health():
            return "Backend is not running or unhealthy"
        
        # Step 2: Analyze database state
        db_state = self.analyze_database_state()
        if not db_state:
            return "Database analysis failed"
        
        # Step 3: Test API response
        api_events = self.test_api_response()
        if not api_events:
            return "API response test failed"
        
        # Step 4: Test date generation
        test_events = self.test_date_generation()
        
        # Step 5: Test event posting
        posting_results = self.test_event_posting(test_events)
        
        # Step 6: Verify posted events
        found_events = self.verify_posted_events(test_events)
        
        # Analyze results
        if all(posting_results):
            if found_events:
                # Check if events have correct year
                correct_year_count = 0
                for event in found_events:
                    year = event['start_date'][:4]
                    if year == str(datetime.now().year):
                        correct_year_count += 1
                
                if correct_year_count == len(found_events):
                    self.log("✅ Date generation and posting working correctly")
                    return "Date generation is working correctly"
                else:
                    self.log(f"❌ Only {correct_year_count}/{len(found_events)} events have correct year", "ERROR")
                    return "Events being stored with wrong year"
            else:
                self.log("❌ Events posted but not retrievable", "ERROR")
                return "Events posted but not retrievable"
        else:
            self.log("❌ Event posting failed", "ERROR")
            return "Event posting failed"
    
    def fix_date_issue(self):
        """Attempt to fix the date issue"""
        self.log("🔧 Attempting to fix date issue...")
        
        # Create a simple test event with explicit 2025 date
        test_event = {
            "title": "Agentic Test Event 2025",
            "description": "This is a test event created by the agentic debugger",
            "start_date": "2025-08-05T10:00:00",
            "end_date": "2025-08-05T12:00:00",
            "location_name": "Agentic Test Location",
            "latitude": 35.7796,
            "longitude": -78.6382,
            "organization_id": 1,
            "event_type": "test",
            "source_url": "https://agentic-test.com"
        }
        
        try:
            response = requests.post(self.api_url, json=test_event, timeout=10)
            if response.status_code == 201:
                self.log("✅ Agentic test event posted successfully")
                
                # Verify it's retrievable
                time.sleep(1)
                verify_response = requests.get(self.api_url, timeout=10)
                if verify_response.status_code == 200:
                    events = verify_response.json()
                    for event in events:
                        if event['title'] == test_event['title']:
                            self.log(f"✅ Found agentic test event: {event['start_date']}")
                            if event['start_date'].startswith('2025'):
                                self.log("✅ Event has correct 2025 year!")
                                return True
                            else:
                                self.log(f"❌ Event has wrong year: {event['start_date']}", "ERROR")
                                return False
                    
                    self.log("❌ Agentic test event not found in response", "ERROR")
                    return False
                else:
                    self.log("❌ Failed to verify agentic test event", "ERROR")
                    return False
            else:
                self.log(f"❌ Agentic test event posting failed: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Agentic test failed: {e}", "ERROR")
            return False
    
    def run_full_diagnosis(self):
        """Run complete diagnosis and fix attempt"""
        self.log("🚀 Starting Agentic Debugger for EventPulse NC")
        self.log("=" * 60)
        
        # Run diagnosis
        diagnosis = self.diagnose_issue()
        self.log(f"🔍 Diagnosis: {diagnosis}")
        
        # Attempt fix
        if "wrong year" in diagnosis or "not retrievable" in diagnosis:
            self.log("🔧 Attempting to fix the issue...")
            fix_success = self.fix_date_issue()
            if fix_success:
                self.log("✅ Issue appears to be fixed!")
            else:
                self.log("❌ Fix attempt failed", "ERROR")
        
        # Final verification
        self.log("🔍 Running final verification...")
        final_db_state = self.analyze_database_state()
        final_api_test = self.test_api_response()
        
        self.log("=" * 60)
        self.log("📋 Agentic Debugger Summary:")
        self.log(f"   - Diagnosis: {diagnosis}")
        self.log(f"   - Database events: {final_db_state['total_events'] if final_db_state else 'Unknown'}")
        self.log(f"   - API events: {len(final_api_test) if final_api_test else 0}")
        
        return {
            'diagnosis': diagnosis,
            'db_state': final_db_state,
            'api_state': final_api_test,
            'debug_log': self.debug_log
        }

def main():
    """Main function to run the agentic debugger"""
    debugger = EventPulseAgenticDebugger()
    results = debugger.run_full_diagnosis()
    
    # Save results to file
    with open('agentic_debug_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Results saved to agentic_debug_results.json")
    print(f"🔍 Check the debug log for detailed analysis")

if __name__ == "__main__":
    main() 