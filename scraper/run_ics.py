# scraper/run_ics.py

from ics_scrapers import UNCICSScraper, DukeICSScraper, HolidayListScraper

if __name__ == "__main__":
    print("🔎 UNC ICS Events")
    UNCICSScraper().run_and_post()

    print("🔎 Duke ICS Events")
    DukeICSScraper().run_and_post()

    print("🔎 US Holidays")
    HolidayListScraper().run_and_post()
