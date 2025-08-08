#!/usr/bin/env python3
"""
Test Dashboard Import
Check if Dashboard component can be imported properly
"""

import os
import re

def test_dashboard_import():
    """Test if Dashboard component can be imported"""
    print("🔍 Testing Dashboard Component Import")
    print("=" * 50)
    
    dashboard_file = "frontend/src/components/Dashboard.tsx"
    
    if not os.path.exists(dashboard_file):
        print("❌ Dashboard.tsx not found")
        return False
    
    try:
        with open(dashboard_file, 'r') as f:
            content = f.read()
        
        # Check for basic React component structure
        if 'import React' in content:
            print("✅ React import found")
        else:
            print("❌ React import missing")
            return False
        
        # Check for component definition
        if 'const Dashboard: React.FC' in content:
            print("✅ Dashboard component definition found")
        else:
            print("❌ Dashboard component definition missing")
            return False
        
        # Check for export
        if 'export default Dashboard' in content:
            print("✅ Dashboard export found")
        else:
            print("❌ Dashboard export missing")
            return False
        
        # Check for categories array
        if 'const categories: CategoryBubble[]' in content:
            print("✅ Categories array found")
        else:
            print("❌ Categories array missing")
            return False
        
        # Check for CategoryBubble import
        if 'import { CategoryBubble }' in content:
            print("✅ CategoryBubble import found")
        else:
            print("❌ CategoryBubble import missing")
            return False
        
        # Check for syntax issues
        # Look for unmatched brackets
        open_brackets = content.count('{')
        close_brackets = content.count('}')
        if open_brackets == close_brackets:
            print("✅ Bracket matching looks good")
        else:
            print(f"❌ Bracket mismatch: {open_brackets} open, {close_brackets} close")
            return False
        
        # Check for unmatched parentheses
        open_parens = content.count('(')
        close_parens = content.count(')')
        if open_parens == close_parens:
            print("✅ Parentheses matching looks good")
        else:
            print(f"❌ Parentheses mismatch: {open_parens} open, {close_parens} close")
            return False
        
        # Check for common syntax errors
        syntax_errors = []
        
        # Check for missing semicolons after const declarations
        const_pattern = r'const\s+\w+\s*:\s*\w+\[\]\s*=\s*\[[^\]]*\]'
        const_matches = re.findall(const_pattern, content)
        for match in const_matches:
            if not match.endswith(';'):
                syntax_errors.append(f"Missing semicolon after: {match[:50]}...")
        
        # Check for missing closing brackets
        if content.count('[') != content.count(']'):
            syntax_errors.append("Unmatched square brackets")
        
        if syntax_errors:
            print("❌ Syntax errors found:")
            for error in syntax_errors:
                print(f"   - {error}")
            return False
        else:
            print("✅ No obvious syntax errors found")
        
        print("✅ Dashboard component looks syntactically correct")
        return True
        
    except Exception as e:
        print(f"❌ Error reading Dashboard.tsx: {e}")
        return False

def check_compilation_status():
    """Check if the frontend is compiling successfully"""
    print("\n🔍 Checking Compilation Status")
    print("=" * 40)
    
    try:
        import requests
        response = requests.get("http://localhost:3000", timeout=10)
        
        if response.status_code == 200:
            # Check if there's a compilation error message
            if "Module not found" in response.text or "SyntaxError" in response.text:
                print("❌ Compilation errors detected in HTML")
                return False
            else:
                print("✅ Frontend is serving HTML successfully")
                return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Cannot check frontend: {e}")
        return False

def main():
    """Main function"""
    print(f"Timestamp: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test Dashboard import
    dashboard_ok = test_dashboard_import()
    
    # Check compilation status
    compilation_ok = check_compilation_status()
    
    print("\n📋 SUMMARY:")
    print("=" * 40)
    if dashboard_ok and compilation_ok:
        print("✅ Dashboard component looks good")
        print("✅ Frontend is compiling successfully")
        print("🎯 The issue might be:")
        print("   • Browser caching old JavaScript")
        print("   • Runtime JavaScript errors")
        print("   • Missing dependencies")
    else:
        print("❌ Issues found with Dashboard component or compilation")
        print("🔧 Need to fix the identified issues first")
    
    print("\n💡 NEXT STEPS:")
    print("1. If Dashboard looks good, try browser cache clear")
    print("2. Check browser console for specific error messages")
    print("3. If errors persist, we may need to fix component issues")

if __name__ == "__main__":
    main() 