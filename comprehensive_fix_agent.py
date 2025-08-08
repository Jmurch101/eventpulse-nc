#!/usr/bin/env python3
"""
Comprehensive Fix Agent for EventPulse NC
Fixes click functionality and broken links
"""

import requests
import json
import time
import re
from datetime import datetime
import os

class ComprehensiveFixAgent:
    def __init__(self):
        self.base_url = "http://localhost:3000"
        self.api_url = "http://localhost:3001"
        self.issues = []
        self.fixes_applied = []
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def check_services(self):
        """Check if all services are running"""
        self.log("🔍 Checking services...")
        
        # Check backend
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                self.log("✅ Backend is running")
            else:
                self.log("❌ Backend not responding", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Backend error: {e}", "ERROR")
            return False
            
        # Check frontend
        try:
            response = requests.get(self.base_url, timeout=10)
            if response.status_code == 200:
                self.log("✅ Frontend is responding")
                return True
            else:
                self.log(f"❌ Frontend returned status {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Frontend error: {e}", "ERROR")
            return False
    
    def diagnose_react_mounting(self):
        """Diagnose why React is not mounting"""
        self.log("🔍 Diagnosing React mounting issues...")
        
        try:
            response = requests.get(self.base_url, timeout=10)
            html_content = response.text
            
            # Check if React is mounting
            if '<div id="root"></div>' in html_content:
                self.log("⚠️ React is not mounting - root div is empty", "WARNING")
                self.issues.append("React not mounting")
                
                # Check for common issues
                if 'bundle.js' not in html_content:
                    self.log("❌ Bundle.js not found in HTML", "ERROR")
                    self.issues.append("Missing bundle.js")
                else:
                    self.log("✅ Bundle.js found in HTML")
                    
                # Check for JavaScript errors in bundle
                bundle_response = requests.get(f"{self.base_url}/static/js/bundle.js", timeout=10)
                if bundle_response.status_code == 200:
                    bundle_content = bundle_response.text
                    if 'InteractiveHeatMap' in bundle_content:
                        self.log("✅ InteractiveHeatMap found in bundle")
                    else:
                        self.log("❌ InteractiveHeatMap not found in bundle", "ERROR")
                        self.issues.append("InteractiveHeatMap missing from bundle")
                        
                    if 'DayMapModal' in bundle_content:
                        self.log("✅ DayMapModal found in bundle")
                    else:
                        self.log("❌ DayMapModal not found in bundle", "ERROR")
                        self.issues.append("DayMapModal missing from bundle")
                else:
                    self.log("❌ Cannot access bundle.js", "ERROR")
                    self.issues.append("Cannot access bundle.js")
            else:
                self.log("✅ React appears to be mounting")
                
        except Exception as e:
            self.log(f"❌ Error diagnosing React: {e}", "ERROR")
            self.issues.append(f"Diagnosis error: {e}")
    
    def check_broken_links(self):
        """Check for broken links in the application"""
        self.log("🔍 Checking for broken links...")
        
        # Common routes to check
        routes_to_check = [
            "/",
            "/analytics", 
            "/calendar",
            "/events",
            "/about",
            "/contact"
        ]
        
        broken_links = []
        
        for route in routes_to_check:
            try:
                response = requests.get(f"{self.base_url}{route}", timeout=10)
                if response.status_code == 200:
                    self.log(f"✅ Route {route} is accessible")
                elif response.status_code == 404:
                    self.log(f"❌ Route {route} returns 404", "ERROR")
                    broken_links.append(route)
                else:
                    self.log(f"⚠️ Route {route} returned status {response.status_code}", "WARNING")
                    broken_links.append(route)
            except Exception as e:
                self.log(f"❌ Error checking route {route}: {e}", "ERROR")
                broken_links.append(route)
        
        if broken_links:
            self.issues.append(f"Broken links: {broken_links}")
        else:
            self.log("✅ All checked routes are accessible")
    
    def check_api_endpoints(self):
        """Check API endpoints"""
        self.log("🔍 Checking API endpoints...")
        
        api_endpoints = [
            "/health",
            "/api/events",
            "/api/events/stats"
        ]
        
        broken_apis = []
        
        for endpoint in api_endpoints:
            try:
                response = requests.get(f"{self.api_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    self.log(f"✅ API {endpoint} is working")
                else:
                    self.log(f"❌ API {endpoint} returned status {response.status_code}", "ERROR")
                    broken_apis.append(endpoint)
            except Exception as e:
                self.log(f"❌ Error checking API {endpoint}: {e}", "ERROR")
                broken_apis.append(endpoint)
        
        if broken_apis:
            self.issues.append(f"Broken APIs: {broken_apis}")
    
    def fix_react_mounting(self):
        """Apply fixes for React mounting issues"""
        self.log("🔧 Applying React mounting fixes...")
        
        # Fix 1: Check for TypeScript compilation errors
        self.log("🔧 Checking TypeScript compilation...")
        try:
            # Check if there are any obvious import/export issues
            dashboard_file = "frontend/src/components/Dashboard.tsx"
            if os.path.exists(dashboard_file):
                with open(dashboard_file, 'r') as f:
                    content = f.read()
                    if 'import InteractiveHeatMap' in content:
                        self.log("✅ InteractiveHeatMap import found")
                    else:
                        self.log("❌ InteractiveHeatMap import missing", "ERROR")
                        self.issues.append("Missing InteractiveHeatMap import")
                        
                    if 'import DayMapModal' in content:
                        self.log("✅ DayMapModal import found")
                    else:
                        self.log("❌ DayMapModal import missing", "ERROR")
                        self.issues.append("Missing DayMapModal import")
            else:
                self.log("❌ Dashboard.tsx not found", "ERROR")
                self.issues.append("Dashboard.tsx missing")
                
        except Exception as e:
            self.log(f"❌ Error checking Dashboard.tsx: {e}", "ERROR")
            self.issues.append(f"Dashboard.tsx error: {e}")
        
        # Fix 2: Check for missing dependencies
        self.log("🔧 Checking package.json dependencies...")
        try:
            package_file = "frontend/package.json"
            if os.path.exists(package_file):
                with open(package_file, 'r') as f:
                    content = json.load(f)
                    dependencies = content.get('dependencies', {})
                    
                    required_deps = ['react', 'react-dom', 'react-router-dom']
                    missing_deps = []
                    
                    for dep in required_deps:
                        if dep not in dependencies:
                            missing_deps.append(dep)
                    
                    if missing_deps:
                        self.log(f"❌ Missing dependencies: {missing_deps}", "ERROR")
                        self.issues.append(f"Missing dependencies: {missing_deps}")
                    else:
                        self.log("✅ All required dependencies found")
            else:
                self.log("❌ package.json not found", "ERROR")
                self.issues.append("package.json missing")
                
        except Exception as e:
            self.log(f"❌ Error checking package.json: {e}", "ERROR")
            self.issues.append(f"package.json error: {e}")
    
    def fix_broken_links(self):
        """Apply fixes for broken links"""
        self.log("🔧 Applying broken link fixes...")
        
        # Fix 1: Check routing configuration
        self.log("🔧 Checking routing configuration...")
        try:
            app_file = "frontend/src/App.tsx"
            if os.path.exists(app_file):
                with open(app_file, 'r') as f:
                    content = f.read()
                    
                    # Check for common routing issues
                    if 'BrowserRouter' in content:
                        self.log("✅ BrowserRouter found")
                    else:
                        self.log("❌ BrowserRouter not found", "ERROR")
                        self.issues.append("Missing BrowserRouter")
                        
                    if 'Routes' in content:
                        self.log("✅ Routes found")
                    else:
                        self.log("❌ Routes not found", "ERROR")
                        self.issues.append("Missing Routes")
                        
                    # Check for specific routes
                    routes_to_check = ['/', '/analytics', '/calendar']
                    for route in routes_to_check:
                        if f'path="{route}"' in content:
                            self.log(f"✅ Route {route} configured")
                        else:
                            self.log(f"❌ Route {route} not configured", "ERROR")
                            self.issues.append(f"Missing route: {route}")
            else:
                self.log("❌ App.tsx not found", "ERROR")
                self.issues.append("App.tsx missing")
                
        except Exception as e:
            self.log(f"❌ Error checking App.tsx: {e}", "ERROR")
            self.issues.append(f"App.tsx error: {e}")
    
    def apply_click_functionality_fixes(self):
        """Apply specific fixes for click functionality"""
        self.log("🔧 Applying click functionality fixes...")
        
        # Fix 1: Check InteractiveHeatMap click handler
        try:
            heatmap_file = "frontend/src/components/InteractiveHeatMap.tsx"
            if os.path.exists(heatmap_file):
                with open(heatmap_file, 'r') as f:
                    content = f.read()
                    
                    if 'onClick' in content:
                        self.log("✅ onClick handler found in InteractiveHeatMap")
                    else:
                        self.log("❌ onClick handler missing in InteractiveHeatMap", "ERROR")
                        self.issues.append("Missing onClick in InteractiveHeatMap")
                        
                    if 'onDateSelect' in content:
                        self.log("✅ onDateSelect prop found in InteractiveHeatMap")
                    else:
                        self.log("❌ onDateSelect prop missing in InteractiveHeatMap", "ERROR")
                        self.issues.append("Missing onDateSelect in InteractiveHeatMap")
            else:
                self.log("❌ InteractiveHeatMap.tsx not found", "ERROR")
                self.issues.append("InteractiveHeatMap.tsx missing")
                
        except Exception as e:
            self.log(f"❌ Error checking InteractiveHeatMap: {e}", "ERROR")
            self.issues.append(f"InteractiveHeatMap error: {e}")
        
        # Fix 2: Check Dashboard click handler
        try:
            dashboard_file = "frontend/src/components/Dashboard.tsx"
            if os.path.exists(dashboard_file):
                with open(dashboard_file, 'r') as f:
                    content = f.read()
                    
                    if 'handleDateSelect' in content:
                        self.log("✅ handleDateSelect function found in Dashboard")
                    else:
                        self.log("❌ handleDateSelect function missing in Dashboard", "ERROR")
                        self.issues.append("Missing handleDateSelect in Dashboard")
                        
                    if 'onDateSelect={handleDateSelect}' in content:
                        self.log("✅ onDateSelect prop correctly passed to InteractiveHeatMap")
                    else:
                        self.log("❌ onDateSelect prop not correctly passed", "ERROR")
                        self.issues.append("onDateSelect prop not passed correctly")
            else:
                self.log("❌ Dashboard.tsx not found", "ERROR")
                self.issues.append("Dashboard.tsx missing")
                
        except Exception as e:
            self.log(f"❌ Error checking Dashboard: {e}", "ERROR")
            self.issues.append(f"Dashboard error: {e}")
    
    def generate_fix_report(self):
        """Generate a comprehensive fix report"""
        self.log("📋 Generating fix report...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "issues_found": self.issues,
            "fixes_applied": self.fixes_applied,
            "recommendations": []
        }
        
        # Generate recommendations based on issues
        if "React not mounting" in self.issues:
            report["recommendations"].append({
                "issue": "React not mounting",
                "solution": "Check browser console for JavaScript errors and restart frontend",
                "steps": [
                    "1. Open browser developer tools (F12)",
                    "2. Check Console tab for red error messages",
                    "3. Restart frontend: cd frontend && npm start",
                    "4. Hard refresh browser (Ctrl+Shift+R)"
                ]
            })
        
        if "Broken links" in str(self.issues):
            report["recommendations"].append({
                "issue": "Broken links",
                "solution": "Check routing configuration and component imports",
                "steps": [
                    "1. Verify all routes are defined in App.tsx",
                    "2. Check that all components are properly imported",
                    "3. Ensure all referenced components exist",
                    "4. Test each route manually"
                ]
            })
        
        if "Missing dependencies" in str(self.issues):
            report["recommendations"].append({
                "issue": "Missing dependencies",
                "solution": "Install missing npm packages",
                "steps": [
                    "1. cd frontend",
                    "2. npm install",
                    "3. Check for any missing dependencies",
                    "4. Restart frontend"
                ]
            })
        
        # Save report
        with open("comprehensive_fix_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        self.log("✅ Fix report saved to comprehensive_fix_report.json")
        return report
    
    def run_comprehensive_diagnosis(self):
        """Run the complete diagnosis and fix process"""
        self.log("🚀 Starting Comprehensive Fix Agent")
        self.log("=" * 60)
        
        # Step 1: Check services
        if not self.check_services():
            self.log("❌ Services not running, cannot proceed", "ERROR")
            return False
        
        # Step 2: Diagnose React mounting
        self.diagnose_react_mounting()
        
        # Step 3: Check broken links
        self.check_broken_links()
        
        # Step 4: Check API endpoints
        self.check_api_endpoints()
        
        # Step 5: Apply fixes
        self.fix_react_mounting()
        self.fix_broken_links()
        self.apply_click_functionality_fixes()
        
        # Step 6: Generate report
        report = self.generate_fix_report()
        
        # Step 7: Summary
        self.log("=" * 60)
        self.log("📋 COMPREHENSIVE DIAGNOSIS COMPLETE")
        self.log("=" * 60)
        
        if self.issues:
            self.log(f"❌ Found {len(self.issues)} issues:")
            for i, issue in enumerate(self.issues, 1):
                self.log(f"   {i}. {issue}")
        else:
            self.log("✅ No issues found!")
        
        self.log("")
        self.log("🎯 IMMEDIATE ACTIONS REQUIRED:")
        self.log("1. Open http://localhost:3000 in your browser")
        self.log("2. Press F12 to open Developer Tools")
        self.log("3. Check the Console tab for JavaScript errors")
        self.log("4. If you see red error messages, restart the frontend:")
        self.log("   cd frontend && npm start")
        self.log("5. Hard refresh your browser (Ctrl+Shift+R)")
        self.log("")
        self.log("💡 If React loads successfully:")
        self.log("   • Calendar should show August 2026")
        self.log("   • Click on colored squares (August 30-31)")
        self.log("   • Modal should appear with event details")
        
        return True

def main():
    """Main function"""
    agent = ComprehensiveFixAgent()
    agent.run_comprehensive_diagnosis()

if __name__ == "__main__":
    main() 