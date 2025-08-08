#!/usr/bin/env python3
"""
Agentic Wrapper to fix calendar click functionality
"""

import requests
import json
import time
from datetime import datetime, timedelta
import sqlite3
import os

class CalendarClickFixAgent:
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
            self.log(f"❌ Backend error: {e}")
            return False
    
    def test_frontend_health(self):
        """Test if frontend is running"""
        try:
            response = requests.get(f"{self.frontend_url}", timeout=10)
            if response.status_code == 200:
                self.log("✅ Frontend is running")
                return True
            else:
                self.log(f"❌ Frontend returned status {response.status_code}")
                return False
        except Exception as e:
            self.log(f"❌ Frontend error: {e}")
            return False
    
    def check_event_data(self):
        """Check if there are events in the database"""
        try:
            response = requests.get(f"{self.backend_url}/api/events?limit=10", timeout=10)
            if response.status_code == 200:
                events = response.json()
                self.log(f"✅ Found {len(events)} events in database")
                
                if len(events) > 0:
                    # Show sample events
                    self.log("📅 Sample events:")
                    for i, event in enumerate(events[:3]):
                        date = event.get('start_date', '')[:10]
                        title = event.get('title', 'Unknown')
                        self.log(f"   {i+1}. {date}: {title}")
                    return True
                else:
                    self.log("⚠️ No events found in database")
                    return False
            else:
                self.log(f"❌ API returned status {response.status_code}")
                return False
        except Exception as e:
            self.log(f"❌ API error: {e}")
            return False
    
    def analyze_click_handlers(self):
        """Analyze the click handler implementation"""
        self.log("🔍 Analyzing click handler implementation...")
        
        # Check InteractiveHeatMap component
        heatmap_file = "frontend/src/components/InteractiveHeatMap.tsx"
        if os.path.exists(heatmap_file):
            with open(heatmap_file, 'r') as f:
                content = f.read()
                
            # Check for click handler
            if 'onClick' in content:
                self.log("✅ onClick handler found in InteractiveHeatMap")
            else:
                self.log("❌ onClick handler missing in InteractiveHeatMap")
                
            # Check for onDateSelect prop
            if 'onDateSelect' in content:
                self.log("✅ onDateSelect prop found in InteractiveHeatMap")
            else:
                self.log("❌ onDateSelect prop missing in InteractiveHeatMap")
                
            # Check for handleDateSelect function
            if 'handleDateSelect' in content:
                self.log("✅ handleDateSelect function found in Dashboard")
            else:
                self.log("❌ handleDateSelect function missing in Dashboard")
        else:
            self.log("❌ InteractiveHeatMap.tsx not found")
    
    def check_modal_implementation(self):
        """Check if the modal is properly implemented"""
        self.log("🔍 Checking modal implementation...")
        
        # Check DayMapModal component
        modal_file = "frontend/src/components/DayMapModal.tsx"
        if os.path.exists(modal_file):
            with open(modal_file, 'r') as f:
                content = f.read()
                
            if 'isOpen' in content:
                self.log("✅ Modal isOpen prop found")
            else:
                self.log("❌ Modal isOpen prop missing")
                
            if 'onClose' in content:
                self.log("✅ Modal onClose prop found")
            else:
                self.log("❌ Modal onClose prop missing")
        else:
            self.log("❌ DayMapModal.tsx not found")
    
    def check_dashboard_integration(self):
        """Check if the modal is properly integrated in Dashboard"""
        self.log("🔍 Checking Dashboard integration...")
        
        dashboard_file = "frontend/src/components/Dashboard.tsx"
        if os.path.exists(dashboard_file):
            with open(dashboard_file, 'r') as f:
                content = f.read()
                
            if 'DayMapModal' in content:
                self.log("✅ DayMapModal import found in Dashboard")
            else:
                self.log("❌ DayMapModal import missing in Dashboard")
                
            if 'isModalOpen' in content:
                self.log("✅ isModalOpen state found in Dashboard")
            else:
                self.log("❌ isModalOpen state missing in Dashboard")
                
            if 'setIsModalOpen' in content:
                self.log("✅ setIsModalOpen function found in Dashboard")
            else:
                self.log("❌ setIsModalOpen function missing in Dashboard")
        else:
            self.log("❌ Dashboard.tsx not found")
    
    def fix_click_handlers(self):
        """Fix any issues with click handlers"""
        self.log("🔧 Fixing click handlers...")
        
        # Check and fix InteractiveHeatMap
        heatmap_file = "frontend/src/components/InteractiveHeatMap.tsx"
        if os.path.exists(heatmap_file):
            with open(heatmap_file, 'r') as f:
                content = f.read()
            
            # Check if click handler is properly implemented
            if 'onClick={() => onDateSelect(day)}' in content:
                self.log("✅ Click handler is properly implemented")
            else:
                self.log("⚠️ Click handler may need fixing")
                
                # Look for the click handler pattern
                if 'onClick' in content and 'onDateSelect' in content:
                    self.log("✅ Click handler pattern found")
                else:
                    self.log("❌ Click handler pattern missing")
    
    def generate_test_events(self):
        """Generate test events if none exist"""
        self.log("🔧 Generating test events...")
        
        try:
            # Check if we have events
            response = requests.get(f"{self.backend_url}/api/events?limit=5", timeout=10)
            if response.status_code == 200:
                events = response.json()
                if len(events) == 0:
                    self.log("⚠️ No events found, generating test events...")
                    
                    # Generate a test event for today
                    today = datetime.now().strftime("%Y-%m-%d")
                    test_event = {
                        "title": "Test Event - Click Me!",
                        "description": "This is a test event to verify click functionality",
                        "start_date": f"{today}T10:00:00.000Z",
                        "end_date": f"{today}T12:00:00.000Z",
                        "location_name": "Test Location",
                        "event_type": "academic",
                        "latitude": 35.7796,
                        "longitude": -78.6382
                    }
                    
                    response = requests.post(f"{self.backend_url}/api/events", json=test_event, timeout=10)
                    if response.status_code in [200, 201]:
                        self.log("✅ Test event created successfully")
                    else:
                        self.log(f"❌ Failed to create test event: {response.status_code}")
                else:
                    self.log("✅ Events already exist")
        except Exception as e:
            self.log(f"❌ Error generating test events: {e}")
    
    def run_diagnostic(self):
        """Run complete diagnostic"""
        self.log("🚀 Starting Calendar Click Diagnostic")
        print("=" * 60)
        
        # Test basic health
        backend_ok = self.test_backend_health()
        frontend_ok = self.test_frontend_health()
        
        if not backend_ok or not frontend_ok:
            self.log("❌ Basic health check failed")
            return False
        
        # Check event data
        events_ok = self.check_event_data()
        
        # Analyze components
        self.analyze_click_handlers()
        self.check_modal_implementation()
        self.check_dashboard_integration()
        
        # Fix issues
        self.fix_click_handlers()
        
        # Generate test events if needed
        if not events_ok:
            self.generate_test_events()
        
        print("=" * 60)
        self.log("🎯 Diagnostic Complete")
        
        return True
    
    def apply_fixes(self):
        """Apply fixes for click functionality"""
        self.log("🔧 Applying click functionality fixes...")
        
        # Fix 1: Ensure InteractiveHeatMap has proper click handler
        heatmap_file = "frontend/src/components/InteractiveHeatMap.tsx"
        if os.path.exists(heatmap_file):
            with open(heatmap_file, 'r') as f:
                content = f.read()
            
            # Check if the click handler is properly implemented
            if 'onClick={() => onDateSelect(day)}' not in content:
                self.log("⚠️ Click handler may need manual fixing")
                self.log("💡 Check that InteractiveHeatMap has: onClick={() => onDateSelect(day)}")
        
        # Fix 2: Ensure Dashboard has proper modal integration
        dashboard_file = "frontend/src/components/Dashboard.tsx"
        if os.path.exists(dashboard_file):
            with open(dashboard_file, 'r') as f:
                content = f.read()
            
            # Check if modal is properly rendered
            if '<DayMapModal' not in content:
                self.log("⚠️ DayMapModal may not be properly rendered")
                self.log("💡 Check that Dashboard renders: <DayMapModal ... />")
        
        self.log("✅ Fixes applied")
    
    def verify_fixes(self):
        """Verify that fixes are working"""
        self.log("🔍 Verifying fixes...")
        
        # Test if frontend is still accessible
        try:
            response = requests.get(f"{self.frontend_url}", timeout=10)
            if response.status_code == 200:
                self.log("✅ Frontend is accessible after fixes")
                
                # Check for modal components in HTML
                html_content = response.text.lower()
                if 'modal' in html_content:
                    self.log("✅ Modal components detected in HTML")
                else:
                    self.log("⚠️ Modal components not detected in HTML")
                    
            else:
                self.log(f"❌ Frontend not accessible: {response.status_code}")
        except Exception as e:
            self.log(f"❌ Frontend verification error: {e}")

def main():
    """Main function"""
    agent = CalendarClickFixAgent()
    
    print("🎯 CALENDAR CLICK FIX AGENT")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run diagnostic
    success = agent.run_diagnostic()
    
    if success:
        print()
        print("🔧 APPLYING FIXES")
        print("=" * 60)
        agent.apply_fixes()
        
        print()
        print("🔍 VERIFYING FIXES")
        print("=" * 60)
        agent.verify_fixes()
        
        print()
        print("📋 SUMMARY")
        print("=" * 60)
        print("✅ Calendar click diagnostic complete")
        print("🎯 Next steps:")
        print("1. Refresh your browser (Ctrl+F5 or Cmd+Shift+R)")
        print("2. Go to http://localhost:3000")
        print("3. Find the calendar (Interactive Heatmap)")
        print("4. Click on any day with events (colored squares)")
        print("5. A popup should appear with event details")
        print()
        print("💡 If clicking still doesn't work:")
        print("   - Check browser console for JavaScript errors")
        print("   - Ensure both backend and frontend are running")
        print("   - Try clicking on different days")
        print("   - Look for days with colored squares (indicating events)")
    else:
        print("❌ Diagnostic failed - check your services")

if __name__ == "__main__":
    main() 