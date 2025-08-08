#!/usr/bin/env python3
"""
Run calendar diagnostic directly
"""

from calendar_fix_agent import CalendarFixAgent

def main():
    agent = CalendarFixAgent()
    agent.run_diagnostic()

if __name__ == "__main__":
    main() 