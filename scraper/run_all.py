from ncsu_scraper import NCSUScraper
# from unc_scraper import UNCScraper
from api_client import post_event

scrapers = [NCSUScraper()]
for scraper in scrapers:
    events = scraper.scrape()
    for event in events:
        post_event(event)
