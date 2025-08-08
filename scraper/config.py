# scraper/config.py

SOURCES = {
    "ncsu": {
        "url": "https://calendar.ncsu.edu/",
        "org_id": 1,
        "event_type": "academic"
    },

    "unc": {
        "url": "https://events.unc.edu",
        "org_id": 2,
        "event_type": "academic"
    },
    "duke": {
        "url": "https://calendar.duke.edu",
        "org_id": 3,
        "event_type": "academic"
    },
    "holidays": {
    "url": "https://www.timeanddate.com/holidays/us/",
    "org_id": 99,
    "event_type": "holiday"
    }
    # Add more schools here as needed
}

