# scraper/base_scraper.py

import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

class BaseScraper(ABC):
    """
    Abstract base class for all scrapers.
    Each scraper can optionally pass custom headers (e.g., User-Agent) to avoid request blocking.
    """
    def __init__(self, source_name, base_url, headers=None):
        self.source_name = source_name
        self.base_url = base_url
        self.headers = headers or {}  # Optional HTTP headers

    def fetch_html(self, url=None):
        """
        Fetch the HTML content of a webpage, using any provided headers.
        """
        try:
            response = requests.get(url or self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"❌ Failed to fetch {url or self.base_url}: {e}")
            return None

    def get_soup(self, html):
        """
        Returns a BeautifulSoup object from raw HTML.
        """
        return BeautifulSoup(html, "html.parser")

    @abstractmethod
    def parse_events(self, html):
        """
        Parse HTML and return a list of event dicts ready to POST to the API.
        Each event dict should match the backend API schema.
        """
        pass

    def run(self):
        """
        Full pipeline: fetch -> parse -> return events
        """
        print(f"🔎 Scraping: {self.source_name}")
        html = self.fetch_html(self.base_url)
        if html:
            events = self.parse_events(html)
            print(f"✅ Found {len(events)} events for {self.source_name}")
            return events
        return []
