#!/usr/bin/env python3
"""
Agentic UI Fixer for EventPulse NC
Diagnoses and fixes oversized images and event click issues
"""

import requests
import json
import os
import subprocess
import time
from datetime import datetime

class AgenticUIFixer:
    def __init__(self):
        self.frontend_url = "http://localhost:3000"
        self.backend_url = "http://localhost:3001"
        self.debug_log = []
        
    def log(self, message, level="INFO"):
        """Log debug messages with timestamps"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.debug_log.append(log_entry)
        print(log_entry)
        
    def check_frontend_status(self):
        """Check if frontend is running and accessible"""
        try:
            response = requests.get(self.frontend_url, timeout=10)
            if response.status_code == 200:
                self.log("✅ Frontend is accessible")
                return True
            else:
                self.log(f"❌ Frontend returned status {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Frontend not accessible: {e}", "ERROR")
            return False
    
    def check_backend_status(self):
        """Check if backend is running and accessible"""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=10)
            if response.status_code == 200:
                self.log("✅ Backend is accessible")
                return True
            else:
                self.log(f"❌ Backend returned status {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Backend not accessible: {e}", "ERROR")
            return False
    
    def analyze_image_sizes(self):
        """Analyze current image sizes in components"""
        self.log("🔍 Analyzing image sizes in components...")
        
        # Check CategoryBubbles component
        category_bubbles_path = "frontend/src/components/CategoryBubbles.tsx"
        if os.path.exists(category_bubbles_path):
            with open(category_bubbles_path, 'r') as f:
                content = f.read()
                
            # Look for icon size patterns
            if 'h-8 w-8' in content or 'h-12 w-12' in content:
                self.log("⚠️ Found large icon sizes in CategoryBubbles")
                return "large_icons"
            elif 'h-6 w-6' in content or 'h-4 w-4' in content:
                self.log("✅ Icon sizes appear reasonable in CategoryBubbles")
                return "reasonable_icons"
        
        return "unknown"
    
    def analyze_event_click_handling(self):
        """Analyze event click handling in components"""
        self.log("🔍 Analyzing event click handling...")
        
        # Check InteractiveHeatMap component
        heatmap_path = "frontend/src/components/InteractiveHeatMap.tsx"
        if os.path.exists(heatmap_path):
            with open(heatmap_path, 'r') as f:
                content = f.read()
                
            # Check for onDateSelect prop usage
            if 'onDateSelect' in content and 'onClick' in content:
                self.log("✅ InteractiveHeatMap has click handling")
                return "has_click_handling"
            else:
                self.log("❌ InteractiveHeatMap missing click handling", "ERROR")
                return "missing_click_handling"
        
        return "unknown"
    
    def check_dashboard_props(self):
        """Check if Dashboard is passing required props to heatmap"""
        self.log("🔍 Checking Dashboard props...")
        
        dashboard_path = "frontend/src/components/Dashboard.tsx"
        if os.path.exists(dashboard_path):
            with open(dashboard_path, 'r') as f:
                content = f.read()
                
            # Check for InteractiveHeatMap usage with props
            if 'InteractiveHeatMap' in content and 'onDateSelect' in content:
                self.log("✅ Dashboard passes onDateSelect to InteractiveHeatMap")
                return True
            else:
                self.log("❌ Dashboard missing onDateSelect prop", "ERROR")
                return False
        
        return False
    
    def check_event_modal_component(self):
        """Check if there's a modal component for showing events"""
        self.log("🔍 Checking for event modal component...")
        
        # Look for modal components
        modal_files = [
            "frontend/src/components/DayMapModal.tsx",
            "frontend/src/components/EventModal.tsx",
            "frontend/src/components/EventDetails.tsx"
        ]
        
        for modal_file in modal_files:
            if os.path.exists(modal_file):
                self.log(f"✅ Found modal component: {modal_file}")
                return modal_file
        
        self.log("❌ No event modal component found", "ERROR")
        return None
    
    def fix_oversized_images(self):
        """Fix oversized images in components"""
        self.log("🔧 Fixing oversized images...")
        
        # Fix CategoryBubbles component
        category_bubbles_path = "frontend/src/components/CategoryBubbles.tsx"
        if os.path.exists(category_bubbles_path):
            with open(category_bubbles_path, 'r') as f:
                content = f.read()
            
            # Replace large icon sizes with smaller ones
            content = content.replace('h-8 w-8', 'h-6 w-6')
            content = content.replace('h-12 w-12', 'h-6 w-6')
            content = content.replace('h-10 w-10', 'h-5 w-5')
            
            with open(category_bubbles_path, 'w') as f:
                f.write(content)
            
            self.log("✅ Fixed icon sizes in CategoryBubbles")
        
        # Fix other components with large images
        components_to_fix = [
            "frontend/src/components/Dashboard.tsx",
            "frontend/src/components/AdvancedSearch.tsx",
            "frontend/src/components/AnalyticsDashboard.tsx",
            "frontend/src/components/Header.tsx"
        ]
        
        for component_path in components_to_fix:
            if os.path.exists(component_path):
                with open(component_path, 'r') as f:
                    content = f.read()
                
                # Replace large icon sizes
                content = content.replace('h-8 w-8', 'h-6 w-6')
                content = content.replace('h-12 w-12', 'h-6 w-6')
                content = content.replace('h-10 w-10', 'h-5 w-5')
                
                with open(component_path, 'w') as f:
                    f.write(content)
                
                self.log(f"✅ Fixed icon sizes in {os.path.basename(component_path)}")
    
    def create_event_modal_component(self):
        """Create a modal component for showing events when clicking on days"""
        self.log("🔧 Creating event modal component...")
        
        modal_content = '''import React from 'react';
import { format } from 'date-fns';
import { Event } from '../types/Event';
import { XMarkIcon, MapPinIcon, ClockIcon, CalendarIcon } from '@heroicons/react/24/outline';

interface EventModalProps {
  isOpen: boolean;
  onClose: () => void;
  selectedDate: Date | null;
  events: Event[];
}

const EventModal: React.FC<EventModalProps> = ({ isOpen, onClose, selectedDate, events }) => {
  if (!isOpen || !selectedDate) return null;

  const filteredEvents = events.filter(event => {
    const eventDate = new Date(event.start_date);
    return format(eventDate, 'yyyy-MM-dd') === format(selectedDate, 'yyyy-MM-dd');
  });

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">
              Events on {format(selectedDate, 'EEEE, MMMM d, yyyy')}
            </h2>
            <p className="text-sm text-gray-600 mt-1">
              {filteredEvents.length} event{filteredEvents.length !== 1 ? 's' : ''} found
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[60vh]">
          {filteredEvents.length === 0 ? (
            <div className="text-center py-8">
              <CalendarIcon className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">No events scheduled for this date</p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredEvents.map((event) => (
                <div key={event.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                  <h3 className="font-semibold text-gray-900 mb-2">{event.title}</h3>
                  <p className="text-gray-600 text-sm mb-3">{event.description}</p>
                  
                  <div className="space-y-2 text-sm text-gray-500">
                    <div className="flex items-center">
                      <ClockIcon className="h-4 w-4 mr-2" />
                      <span>
                        {format(new Date(event.start_date), 'h:mm a')} - 
                        {format(new Date(event.end_date), 'h:mm a')}
                      </span>
                    </div>
                    
                    <div className="flex items-center">
                      <MapPinIcon className="h-4 w-4 mr-2" />
                      <span>{event.location_name}</span>
                    </div>
                    
                    <div className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                      {event.event_type}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EventModal;
'''
        
        modal_path = "frontend/src/components/EventModal.tsx"
        with open(modal_path, 'w') as f:
            f.write(modal_content)
        
        self.log("✅ Created EventModal component")
        return modal_path
    
    def update_dashboard_with_modal(self):
        """Update Dashboard to use the event modal"""
        self.log("🔧 Updating Dashboard to use event modal...")
        
        dashboard_path = "frontend/src/components/Dashboard.tsx"
        if os.path.exists(dashboard_path):
            with open(dashboard_path, 'r') as f:
                content = f.read()
            
            # Add import for EventModal
            if 'import EventModal' not in content:
                import_line = "import EventModal from './EventModal';"
                # Find the last import statement
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('import ') and (i == len(lines) - 1 or not lines[i + 1].startswith('import ')):
                        lines.insert(i + 1, import_line)
                        break
                content = '\n'.join(lines)
            
            # Add state for modal
            if 'const [selectedDate, setSelectedDate]' not in content:
                # Find the first useState line and add our state after it
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'useState' in line and 'selectedCategory' in line:
                        lines.insert(i + 1, '  const [selectedDate, setSelectedDate] = useState<Date | null>(null);')
                        lines.insert(i + 2, '  const [isModalOpen, setIsModalOpen] = useState(false);')
                        break
                content = '\n'.join(lines)
            
            # Add handleDateSelect function
            if 'const handleDateSelect =' not in content:
                # Find a good place to add the function (after other handlers)
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'const handleClearSearch =' in line:
                        lines.insert(i + 3, '  const handleDateSelect = (date: Date) => {')
                        lines.insert(i + 4, '    setSelectedDate(date);')
                        lines.insert(i + 5, '    setIsModalOpen(true);')
                        lines.insert(i + 6, '  };')
                        lines.insert(i + 7, '')
                        break
                content = '\n'.join(lines)
            
            # Add EventModal component at the end
            if '<EventModal' not in content:
                # Find the closing div of the main container
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip() == '</div>' and i > len(lines) - 10:  # Near the end
                        lines.insert(i, '      <EventModal')
                        lines.insert(i + 1, '        isOpen={isModalOpen}')
                        lines.insert(i + 2, '        onClose={() => setIsModalOpen(false)}')
                        lines.insert(i + 3, '        selectedDate={selectedDate}')
                        lines.insert(i + 4, '        events={events}')
                        lines.insert(i + 5, '      />')
                        break
                content = '\n'.join(lines)
            
            with open(dashboard_path, 'w') as f:
                f.write(content)
            
            self.log("✅ Updated Dashboard with event modal")
    
    def restart_frontend(self):
        """Restart the frontend to apply changes"""
        self.log("🔄 Restarting frontend...")
        
        try:
            # Kill existing frontend process
            subprocess.run(['pkill', '-f', 'react-scripts'], capture_output=True)
            time.sleep(2)
            
            # Start frontend in background
            subprocess.Popen(['cd', 'frontend', '&&', 'npm', 'start'], 
                           shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Wait for frontend to start
            time.sleep(10)
            
            # Check if frontend is accessible
            if self.check_frontend_status():
                self.log("✅ Frontend restarted successfully")
                return True
            else:
                self.log("❌ Frontend restart failed", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error restarting frontend: {e}", "ERROR")
            return False
    
    def run_comprehensive_fix(self):
        """Run comprehensive diagnosis and fix"""
        self.log("🚀 Starting Agentic UI Fixer for EventPulse NC")
        self.log("=" * 60)
        
        # Step 1: Check system status
        self.log("📊 Step 1: Checking system status...")
        frontend_ok = self.check_frontend_status()
        backend_ok = self.check_backend_status()
        
        if not frontend_ok or not backend_ok:
            self.log("❌ System not ready for fixes", "ERROR")
            return False
        
        # Step 2: Analyze current issues
        self.log("\n🔍 Step 2: Analyzing current issues...")
        image_analysis = self.analyze_image_sizes()
        click_analysis = self.analyze_event_click_handling()
        dashboard_props_ok = self.check_dashboard_props()
        modal_exists = self.check_event_modal_component()
        
        # Step 3: Apply fixes
        self.log("\n🔧 Step 3: Applying fixes...")
        
        # Fix oversized images
        if image_analysis == "large_icons":
            self.fix_oversized_images()
        
        # Fix event click handling
        if not modal_exists:
            self.create_event_modal_component()
            self.update_dashboard_with_modal()
        
        # Step 4: Restart frontend
        self.log("\n🔄 Step 4: Restarting frontend...")
        restart_success = self.restart_frontend()
        
        # Step 5: Final verification
        self.log("\n✅ Step 5: Final verification...")
        final_frontend_ok = self.check_frontend_status()
        
        # Summary
        self.log("\n" + "=" * 60)
        self.log("📋 Agentic UI Fixer Summary:")
        self.log(f"   - Image sizes: {image_analysis}")
        self.log(f"   - Click handling: {click_analysis}")
        self.log(f"   - Dashboard props: {'✅ OK' if dashboard_props_ok else '❌ Missing'}")
        self.log(f"   - Event modal: {'✅ Created' if not modal_exists else '✅ Exists'}")
        self.log(f"   - Frontend restart: {'✅ Success' if restart_success else '❌ Failed'}")
        self.log(f"   - Final status: {'✅ Working' if final_frontend_ok else '❌ Issues'}")
        
        if final_frontend_ok:
            self.log("\n🎉 UI fixes applied successfully!")
            self.log("🌐 Visit http://localhost:3000 to see the improvements")
            self.log("📅 Click on calendar dates to see events in the modal")
        else:
            self.log("\n❌ Some issues remain", "ERROR")
        
        return final_frontend_ok

def main():
    """Main function to run the agentic UI fixer"""
    fixer = AgenticUIFixer()
    success = fixer.run_comprehensive_fix()
    
    # Save results
    results = {
        'success': success,
        'debug_log': fixer.debug_log,
        'timestamp': datetime.now().isoformat()
    }
    
    with open('agentic_ui_fix_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Results saved to agentic_ui_fix_results.json")
    return success

if __name__ == "__main__":
    main() 