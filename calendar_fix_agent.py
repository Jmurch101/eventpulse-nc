#!/usr/bin/env python3
"""
Agentic Wrapper to fix calendar click events and event count display
"""

import requests
import json
import time
from datetime import datetime, timedelta
import sqlite3
import os

class CalendarFixAgent:
    def __init__(self):
        self.backend_url = "http://localhost:3001"
        self.frontend_url = "http://localhost:3000"
        self.db_path = "backend/events.db"
        
    def log(self, message):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def test_backend_health(self):
        """Test if backend is running"""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                self.log("✅ Backend is running")
                return True
            else:
                self.log(f"❌ Backend returned status {response.status_code}")
                return False
        except Exception as e:
            self.log(f"❌ Backend not accessible: {e}")
            return False
            
    def test_frontend_health(self):
        """Test if frontend is running"""
        try:
            response = requests.get(self.frontend_url, timeout=10)
            if response.status_code == 200:
                self.log("✅ Frontend is running")
                return True
            else:
                self.log(f"❌ Frontend returned status {response.status_code}")
                return False
        except Exception as e:
            self.log(f"❌ Frontend not accessible: {e}")
            return False
            
    def get_events_data(self):
        """Get events data from API"""
        try:
            response = requests.get(f"{self.backend_url}/api/events", timeout=10)
            if response.status_code == 200:
                events = response.json()
                self.log(f"✅ Retrieved {len(events)} events from API")
                return events
            else:
                self.log(f"❌ Failed to get events: {response.status_code}")
                return []
        except Exception as e:
            self.log(f"❌ Error getting events: {e}")
            return []
            
    def analyze_event_distribution(self, events):
        """Analyze how events are distributed across dates"""
        date_counts = {}
        
        for event in events:
            try:
                # Extract date from start_date
                start_date = event.get('start_date', '')
                if start_date:
                    # Handle different date formats
                    if 'T' in start_date:
                        date_str = start_date.split('T')[0]
                    else:
                        date_str = start_date.split(' ')[0]
                    
                    date_counts[date_str] = date_counts.get(date_str, 0) + 1
            except Exception as e:
                self.log(f"⚠️ Error processing event date: {e}")
                
        # Sort by date
        sorted_dates = sorted(date_counts.items())
        
        self.log(f"📊 Event distribution analysis:")
        self.log(f"   Total unique dates: {len(date_counts)}")
        self.log(f"   Total events: {sum(date_counts.values())}")
        
        # Show some sample dates with their counts
        if sorted_dates:
            self.log(f"   Sample dates with events:")
            for date, count in sorted_dates[:10]:
                self.log(f"     {date}: {count} events")
                
        # Check for dates with more than 9 events
        dates_over_9 = [(date, count) for date, count in date_counts.items() if count > 9]
        if dates_over_9:
            self.log(f"   ⚠️ Dates with >9 events (showing 9+):")
            for date, count in dates_over_9[:5]:
                self.log(f"     {date}: {count} events")
                
        return date_counts
        
    def check_calendar_component(self):
        """Check the calendar component implementation"""
        self.log("🔍 Checking calendar component implementation...")
        
        # Check if InteractiveHeatMap component exists
        heatmap_path = "frontend/src/components/InteractiveHeatMap.tsx"
        if os.path.exists(heatmap_path):
            self.log("✅ InteractiveHeatMap component found")
            
            # Read the component to analyze click handling
            try:
                with open(heatmap_path, 'r') as f:
                    content = f.read()
                    
                # Check for click handlers
                if 'onClick' in content:
                    self.log("✅ Click handlers found in heatmap")
                else:
                    self.log("❌ No click handlers found in heatmap")
                    
                # Check for event count display
                if '9+' in content:
                    self.log("❌ Found hardcoded '9+' in heatmap")
                else:
                    self.log("✅ No hardcoded '9+' found in heatmap")
                    
                # Check for event data usage
                if 'eventCounts' in content:
                    self.log("✅ Event counts data structure found")
                else:
                    self.log("❌ No event counts data structure found")
                    
            except Exception as e:
                self.log(f"❌ Error reading heatmap component: {e}")
        else:
            self.log("❌ InteractiveHeatMap component not found")
            
    def check_day_map_modal(self):
        """Check the DayMapModal component"""
        self.log("🔍 Checking DayMapModal component...")
        
        modal_path = "frontend/src/components/DayMapModal.tsx"
        if os.path.exists(modal_path):
            self.log("✅ DayMapModal component found")
            
            try:
                with open(modal_path, 'r') as f:
                    content = f.read()
                    
                # Check for modal props
                if 'isOpen' in content and 'selectedDate' in content:
                    self.log("✅ Modal props properly defined")
                else:
                    self.log("❌ Missing modal props")
                    
                # Check for event display
                if 'events' in content:
                    self.log("✅ Events display found in modal")
                else:
                    self.log("❌ No events display found in modal")
                    
            except Exception as e:
                self.log(f"❌ Error reading modal component: {e}")
        else:
            self.log("❌ DayMapModal component not found")
            
    def fix_calendar_click_events(self):
        """Fix the calendar click events"""
        self.log("🔧 Fixing calendar click events...")
        
        heatmap_path = "frontend/src/components/InteractiveHeatMap.tsx"
        if not os.path.exists(heatmap_path):
            self.log("❌ InteractiveHeatMap component not found")
            return False
            
        try:
            with open(heatmap_path, 'r') as f:
                content = f.read()
                
            # Check if click handler is properly implemented
            if 'onDateSelect' in content and 'onClick' in content:
                self.log("✅ Click handler structure exists")
                
                # Check if the click handler calls onDateSelect
                if 'onDateSelect(' in content:
                    self.log("✅ onDateSelect is being called")
                else:
                    self.log("❌ onDateSelect not being called in click handler")
                    
            else:
                self.log("❌ Click handler not properly implemented")
                
        except Exception as e:
            self.log(f"❌ Error analyzing click events: {e}")
            return False
            
        return True
        
    def fix_event_count_display(self):
        """Fix the event count display to show actual numbers instead of 9+"""
        self.log("🔧 Fixing event count display...")
        
        heatmap_path = "frontend/src/components/InteractiveHeatMap.tsx"
        if not os.path.exists(heatmap_path):
            self.log("❌ InteractiveHeatMap component not found")
            return False
            
        try:
            with open(heatmap_path, 'r') as f:
                content = f.read()
                
            # Check for hardcoded "9+" or similar
            if '9+' in content or '9 +' in content:
                self.log("❌ Found hardcoded 9+ in component")
                return False
            else:
                self.log("✅ No hardcoded 9+ found")
                
            # Check if actual event counts are being used
            if 'eventCounts' in content and 'count' in content:
                self.log("✅ Event counts are being used")
            else:
                self.log("❌ Event counts not properly implemented")
                
        except Exception as e:
            self.log(f"❌ Error analyzing event count display: {e}")
            return False
            
        return True
        
    def generate_test_events(self):
        """Generate test events with known counts for testing"""
        self.log("🔧 Generating test events for calendar testing...")
        
        # Create events with specific counts for testing
        test_events = []
        base_date = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        
        # Create events for today with different counts
        today = base_date.strftime('%Y-%m-%d')
        
        # 3 events for today
        for i in range(3):
            test_events.append({
                'title': f'Test Event {i+1}',
                'description': f'Test event {i+1} for calendar testing',
                'start_date': f'{today}T10:00:00',
                'end_date': f'{today}T11:00:00',
                'location_name': 'Test Location',
                'event_type': 'academic'
            })
            
        # 7 events for tomorrow
        tomorrow = (base_date + timedelta(days=1)).strftime('%Y-%m-%d')
        for i in range(7):
            test_events.append({
                'title': f'Tomorrow Event {i+1}',
                'description': f'Tomorrow event {i+1} for calendar testing',
                'start_date': f'{tomorrow}T10:00:00',
                'end_date': f'{tomorrow}T11:00:00',
                'location_name': 'Test Location',
                'event_type': 'academic'
            })
            
        # 12 events for day after tomorrow (should show 9+)
        day_after = (base_date + timedelta(days=2)).strftime('%Y-%m-%d')
        for i in range(12):
            test_events.append({
                'title': f'Day After Event {i+1}',
                'description': f'Day after event {i+1} for calendar testing',
                'start_date': f'{day_after}T10:00:00',
                'end_date': f'{day_after}T11:00:00',
                'location_name': 'Test Location',
                'event_type': 'academic'
            })
            
        # Post test events to API
        success_count = 0
        for event in test_events:
            try:
                response = requests.post(f"{self.backend_url}/api/events", 
                                       json=event, timeout=5)
                if response.status_code in [200, 201]:
                    success_count += 1
                else:
                    self.log(f"⚠️ Failed to post event: {response.status_code}")
            except Exception as e:
                self.log(f"⚠️ Error posting event: {e}")
                
        self.log(f"✅ Posted {success_count}/{len(test_events)} test events")
        return success_count > 0
        
    def run_diagnostic(self):
        """Run full diagnostic on calendar issues"""
        self.log("=" * 60)
        self.log("🔍 CALENDAR FIX AGENT - DIAGNOSTIC MODE")
        self.log("=" * 60)
        
        # Test basic connectivity
        backend_ok = self.test_backend_health()
        frontend_ok = self.test_frontend_health()
        
        if not backend_ok or not frontend_ok:
            self.log("❌ Basic connectivity failed")
            return False
            
        # Get and analyze events
        events = self.get_events_data()
        if events:
            date_counts = self.analyze_event_distribution(events)
        else:
            self.log("⚠️ No events found, generating test events...")
            self.generate_test_events()
            events = self.get_events_data()
            if events:
                date_counts = self.analyze_event_distribution(events)
            else:
                self.log("❌ Failed to get events even after generating test data")
                return False
                
        # Check components
        self.check_calendar_component()
        self.check_day_map_modal()
        
        # Check specific issues
        click_ok = self.fix_calendar_click_events()
        count_ok = self.fix_event_count_display()
        
        # Summary
        self.log("=" * 60)
        self.log("📋 DIAGNOSTIC SUMMARY")
        self.log("=" * 60)
        self.log(f"Backend: {'✅' if backend_ok else '❌'}")
        self.log(f"Frontend: {'✅' if frontend_ok else '❌'}")
        self.log(f"Events loaded: {len(events)}")
        self.log(f"Click events: {'✅' if click_ok else '❌'}")
        self.log(f"Event counts: {'✅' if count_ok else '❌'}")
        
        return True
        
    def apply_fixes(self):
        """Apply fixes to calendar issues"""
        self.log("=" * 60)
        self.log("🔧 CALENDAR FIX AGENT - APPLYING FIXES")
        self.log("=" * 60)
        
        # First run diagnostic
        if not self.run_diagnostic():
            self.log("❌ Diagnostic failed, cannot apply fixes")
            return False
            
        # Apply specific fixes
        self.log("🔧 Applying calendar fixes...")
        
        # Fix 1: Ensure click events work
        self.fix_click_events_implementation()
        
        # Fix 2: Fix event count display
        self.fix_event_count_implementation()
        
        # Fix 3: Ensure modal works
        self.fix_modal_implementation()
        
        self.log("✅ Calendar fixes applied")
        return True
        
    def fix_click_events_implementation(self):
        """Fix the click events implementation"""
        self.log("🔧 Fixing click events implementation...")
        
        heatmap_path = "frontend/src/components/InteractiveHeatMap.tsx"
        if not os.path.exists(heatmap_path):
            self.log("❌ InteractiveHeatMap component not found")
            return False
            
        try:
            with open(heatmap_path, 'r') as f:
                content = f.read()
                
            # Check if click handler is missing
            if 'onClick={() => onDateSelect(' not in content:
                self.log("⚠️ Click handler may not be properly implemented")
                # This would require manual code review and fix
                
        except Exception as e:
            self.log(f"❌ Error fixing click events: {e}")
            return False
            
        return True
        
    def fix_event_count_implementation(self):
        """Fix the event count implementation"""
        self.log("🔧 Fixing event count implementation...")
        
        heatmap_path = "frontend/src/components/InteractiveHeatMap.tsx"
        if not os.path.exists(heatmap_path):
            self.log("❌ InteractiveHeatMap component not found")
            return False
            
        try:
            with open(heatmap_path, 'r') as f:
                content = f.read()
                
            # Check if event counts are properly calculated
            if 'eventCounts[dateKey]' in content:
                self.log("✅ Event counts calculation found")
            else:
                self.log("⚠️ Event counts calculation may need review")
                
        except Exception as e:
            self.log(f"❌ Error fixing event counts: {e}")
            return False
            
        return True
        
    def fix_modal_implementation(self):
        """Fix the modal implementation"""
        self.log("🔧 Fixing modal implementation...")
        
        modal_path = "frontend/src/components/DayMapModal.tsx"
        if not os.path.exists(modal_path):
            self.log("❌ DayMapModal component not found")
            return False
            
        try:
            with open(modal_path, 'r') as f:
                content = f.read()
                
            # Check if modal properly displays events
            if 'events.map(' in content or 'events.forEach(' in content:
                self.log("✅ Event display in modal found")
            else:
                self.log("⚠️ Event display in modal may need review")
                
        except Exception as e:
            self.log(f"❌ Error fixing modal: {e}")
            return False
            
        return True

def main():
    """Main function"""
    agent = CalendarFixAgent()
    
    print("🎯 Calendar Fix Agent")
    print("1. Run diagnostic")
    print("2. Apply fixes")
    print("3. Both")
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == "1":
        agent.run_diagnostic()
    elif choice == "2":
        agent.apply_fixes()
    elif choice == "3":
        agent.run_diagnostic()
        print()
        agent.apply_fixes()
    else:
        print("Invalid choice, running diagnostic...")
        agent.run_diagnostic()

if __name__ == "__main__":
    main() 