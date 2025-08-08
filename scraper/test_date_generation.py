#!/usr/bin/env python3
"""
Test date generation for 2025 events
"""

from datetime import datetime, timedelta

def test_date_generation():
    """Test the date generation logic"""
    
    print("🧪 Testing date generation...")
    
    # Test current date
    today = datetime.now()
    print(f"Today: {today}")
    print(f"Today year: {today.year}")
    
    # Test start date calculation
    start_date = today + timedelta(days=1)
    print(f"Start date: {start_date}")
    print(f"Start date year: {start_date.year}")
    
    # Test a few sample dates
    for i in range(5):
        test_date = start_date + timedelta(days=i)
        print(f"Test date {i}: {test_date} (year: {test_date.year})")
        
        # Test event time generation
        hour = 10
        minute = 0
        start_time = datetime(test_date.year, test_date.month, test_date.day, hour, minute)
        print(f"  Event time: {start_time} (year: {start_time.year})")
        print(f"  ISO format: {start_time.isoformat()}")

if __name__ == "__main__":
    test_date_generation() 