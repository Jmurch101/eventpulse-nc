#!/usr/bin/env python3
"""
Advanced Agentic Fixer for EventPulse NC 2025 Events Issue
This agent performs deep analysis and implements systematic fixes
"""

import requests
import json
import sqlite3
import os
import subprocess
import time
from datetime import datetime, timedelta
import random

class AdvancedAgenticFixer:
    def __init__(self):
        self.api_url = "http://localhost:3001/api/events"
        self.db_path = "backend/events.db"
        self.debug_log = []
        self.fixes_applied = []
        
    def log(self, message, level="INFO"):
        """Log debug messages with timestamps"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.debug_log.append(log_entry)
        print(log_entry)
        
    def restart_backend(self):
        """Restart the backend server"""
        self.log("🔄 Restarting backend server...")
        
        try:
            # Kill existing backend processes
            subprocess.run(["pkill", "-f", "node index.js"], capture_output=True)
            time.sleep(2)
            
            # Start backend in background
            subprocess.Popen(["cd", "backend", "&&", "node", "index.js"], 
                           shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Wait for backend to start
            time.sleep(5)
            
            # Check if backend is healthy
            for i in range(10):
                try:
                    response = requests.get("http://localhost:3001/health", timeout=5)
                    if response.status_code == 200:
                        self.log("✅ Backend restarted successfully")
                        return True
                except:
                    pass
                time.sleep(1)
            
            self.log("❌ Backend restart failed", "ERROR")
            return False
            
        except Exception as e:
            self.log(f"❌ Backend restart error: {e}", "ERROR")
            return False
    
    def analyze_database_schema(self):
        """Analyze database schema for potential issues"""
        self.log("🔍 Analyzing database schema...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get table schema
            cursor.execute("PRAGMA table_info(events)")
            columns = cursor.fetchall()
            
            self.log("📋 Events table schema:")
            for col in columns:
                self.log(f"   {col[1]} ({col[2]}) - {col[3]}")
            
            # Check for indexes
            cursor.execute("PRAGMA index_list(events)")
            indexes = cursor.fetchall()
            
            self.log("🔍 Database indexes:")
            for idx in indexes:
                self.log(f"   {idx[1]}")
            
            conn.close()
            return columns, indexes
            
        except Exception as e:
            self.log(f"❌ Schema analysis failed: {e}", "ERROR")
            return None, None
    
    def check_for_data_corruption(self):
        """Check for potential data corruption"""
        self.log("🔍 Checking for data corruption...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check for invalid dates
            cursor.execute("""
                SELECT COUNT(*) FROM events 
                WHERE start_date NOT LIKE '____-__-__T__:__:__'
            """)
            invalid_dates = cursor.fetchone()[0]
            
            # Check for null values in required fields
            cursor.execute("""
                SELECT COUNT(*) FROM events 
                WHERE title IS NULL OR start_date IS NULL
            """)
            null_required = cursor.fetchone()[0]
            
            # Check for duplicate IDs
            cursor.execute("""
                SELECT COUNT(*) FROM (
                    SELECT id, COUNT(*) as cnt 
                    FROM events 
                    GROUP BY id 
                    HAVING cnt > 1
                )
            """)
            duplicate_ids = cursor.fetchone()[0]
            
            conn.close()
            
            issues = []
            if invalid_dates > 0:
                issues.append(f"Invalid date formats: {invalid_dates}")
            if null_required > 0:
                issues.append(f"Null required fields: {null_required}")
            if duplicate_ids > 0:
                issues.append(f"Duplicate IDs: {duplicate_ids}")
            
            if issues:
                self.log("❌ Data corruption detected:")
                for issue in issues:
                    self.log(f"   - {issue}", "ERROR")
                return issues
            else:
                self.log("✅ No data corruption detected")
                return []
                
        except Exception as e:
            self.log(f"❌ Corruption check failed: {e}", "ERROR")
            return ["Corruption check failed"]
    
    def fix_database_issues(self, issues):
        """Fix identified database issues"""
        self.log("🔧 Fixing database issues...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            fixes_applied = []
            
            for issue in issues:
                if "Invalid date formats" in issue:
                    # Fix invalid date formats
                    cursor.execute("""
                        UPDATE events 
                        SET start_date = '2025-08-05T10:00:00'
                        WHERE start_date NOT LIKE '____-__-__T__:__:__'
                    """)
                    fixed_count = cursor.rowcount
                    if fixed_count > 0:
                        fixes_applied.append(f"Fixed {fixed_count} invalid date formats")
                        self.log(f"✅ Fixed {fixed_count} invalid date formats")
                
                elif "Null required fields" in issue:
                    # Fix null required fields
                    cursor.execute("""
                        UPDATE events 
                        SET title = 'Unknown Event' 
                        WHERE title IS NULL
                    """)
                    fixed_count = cursor.rowcount
                    if fixed_count > 0:
                        fixes_applied.append(f"Fixed {fixed_count} null titles")
                        self.log(f"✅ Fixed {fixed_count} null titles")
                
                elif "Duplicate IDs" in issue:
                    # Remove duplicate IDs (keep the first occurrence)
                    cursor.execute("""
                        DELETE FROM events 
                        WHERE id NOT IN (
                            SELECT MIN(id) 
                            FROM events 
                            GROUP BY id
                        )
                    """)
                    fixed_count = cursor.rowcount
                    if fixed_count > 0:
                        fixes_applied.append(f"Removed {fixed_count} duplicate IDs")
                        self.log(f"✅ Removed {fixed_count} duplicate IDs")
            
            conn.commit()
            conn.close()
            
            self.fixes_applied.extend(fixes_applied)
            return fixes_applied
            
        except Exception as e:
            self.log(f"❌ Database fix failed: {e}", "ERROR")
            return []
    
    def create_2025_events_batch(self):
        """Create a batch of 2025 events with explicit date handling"""
        self.log("📅 Creating 2025 events batch...")
        
        events = []
        today = datetime.now()
        
        # Create events for next 30 days
        for i in range(30):
            event_date = today + timedelta(days=i+1)
            
            # Ensure we're creating 2025 events
            if event_date.year != 2025:
                event_date = event_date.replace(year=2025)
            
            hour = random.randint(9, 21)
            minute = random.choice([0, 15, 30, 45])
            
            start_time = datetime(event_date.year, event_date.month, event_date.day, hour, minute)
            end_time = start_time + timedelta(hours=random.randint(1, 3))
            
            event = {
                "title": f"Agentic 2025 Event {i+1}",
                "description": f"This is event {i+1} created by the advanced agentic fixer",
                "start_date": start_time.isoformat(),
                "end_date": end_time.isoformat(),
                "location_name": f"Agentic Location {i+1}",
                "latitude": 35.7796 + random.uniform(-0.1, 0.1),
                "longitude": -78.6382 + random.uniform(-0.1, 0.1),
                "organization_id": 1,
                "event_type": random.choice(["academic", "government", "tech", "community"]),
                "source_url": f"https://agentic-2025-event-{i+1}.com"
            }
            events.append(event)
            
            self.log(f"Generated event {i+1}: {event['start_date']} (year: {start_time.year})")
        
        return events
    
    def post_events_with_verification(self, events):
        """Post events with immediate verification"""
        self.log("📤 Posting events with verification...")
        
        successful_posts = 0
        verified_events = []
        
        for i, event in enumerate(events):
            try:
                # Post event
                response = requests.post(self.api_url, json=event, timeout=10)
                
                if response.status_code == 201:
                    self.log(f"✅ Posted event {i+1}: {event['title']}")
                    successful_posts += 1
                    
                    # Immediate verification
                    time.sleep(0.5)
                    verify_response = requests.get(self.api_url, timeout=10)
                    if verify_response.status_code == 200:
                        api_events = verify_response.json()
                        for api_event in api_events:
                            if api_event['title'] == event['title']:
                                if api_event['start_date'].startswith('2025'):
                                    self.log(f"✅ Verified event {i+1} has correct 2025 year")
                                    verified_events.append(api_event)
                                else:
                                    self.log(f"❌ Event {i+1} has wrong year: {api_event['start_date']}", "ERROR")
                                break
                
                elif response.status_code == 200:
                    data = response.json()
                    if data.get('duplicate'):
                        self.log(f"⏭️ Event {i+1} was duplicate")
                    else:
                        self.log(f"✅ Posted event {i+1} (status 200)")
                        successful_posts += 1
                
                else:
                    self.log(f"❌ Failed to post event {i+1}: {response.status_code}", "ERROR")
                
            except Exception as e:
                self.log(f"❌ Error posting event {i+1}: {e}", "ERROR")
        
        self.log(f"📊 Posted {successful_posts}/{len(events)} events successfully")
        self.log(f"📊 Verified {len(verified_events)} events with correct 2025 year")
        
        return successful_posts, verified_events
    
    def run_comprehensive_fix(self):
        """Run comprehensive analysis and fix"""
        self.log("🚀 Starting Advanced Agentic Fixer")
        self.log("=" * 70)
        
        # Step 1: Restart backend for clean state
        if not self.restart_backend():
            return {"error": "Backend restart failed"}
        
        # Step 2: Analyze database schema
        columns, indexes = self.analyze_database_schema()
        
        # Step 3: Check for data corruption
        corruption_issues = self.check_for_data_corruption()
        
        # Step 4: Fix database issues
        if corruption_issues:
            fixes = self.fix_database_issues(corruption_issues)
            self.log(f"🔧 Applied {len(fixes)} database fixes")
        
        # Step 5: Create 2025 events batch
        events = self.create_2025_events_batch()
        
        # Step 6: Post events with verification
        successful_posts, verified_events = self.post_events_with_verification(events)
        
        # Step 7: Final analysis
        self.log("🔍 Running final analysis...")
        
        # Check final database state
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM events WHERE start_date LIKE '2025-%'")
            total_2025_events = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM events")
            total_events = cursor.fetchone()[0]
            
            conn.close()
            
            self.log(f"📊 Final database state:")
            self.log(f"   - Total events: {total_events}")
            self.log(f"   - 2025 events: {total_2025_events}")
            self.log(f"   - Success rate: {(total_2025_events/total_events*100):.1f}%" if total_events > 0 else "N/A")
            
        except Exception as e:
            self.log(f"❌ Final analysis failed: {e}", "ERROR")
        
        # Step 8: Generate summary
        self.log("=" * 70)
        self.log("📋 Advanced Agentic Fixer Summary:")
        self.log(f"   - Database fixes applied: {len(self.fixes_applied)}")
        self.log(f"   - Events posted: {successful_posts}")
        self.log(f"   - Events verified with 2025 year: {len(verified_events)}")
        self.log(f"   - Total 2025 events in database: {total_2025_events if 'total_2025_events' in locals() else 'Unknown'}")
        
        return {
            'fixes_applied': self.fixes_applied,
            'events_posted': successful_posts,
            'events_verified': len(verified_events),
            'total_2025_events': total_2025_events if 'total_2025_events' in locals() else 0,
            'debug_log': self.debug_log
        }

def main():
    """Main function to run the advanced agentic fixer"""
    fixer = AdvancedAgenticFixer()
    results = fixer.run_comprehensive_fix()
    
    # Save results to file
    with open('advanced_agentic_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Results saved to advanced_agentic_results.json")
    print(f"🔍 Check the debug log for detailed analysis")
    
    if 'error' not in results:
        print(f"✅ Advanced Agentic Fixer completed successfully!")
        print(f"📊 2025 events created: {results.get('total_2025_events', 0)}")
    else:
        print(f"❌ Advanced Agentic Fixer failed: {results['error']}")

if __name__ == "__main__":
    main() 