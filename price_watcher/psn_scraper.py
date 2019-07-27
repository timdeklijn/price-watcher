import requests
from bs4 import BeautifulSoup

from price_watcher.price_scraper import PriceScraper

class PSNScraper(PriceScraper):
    """
    Inherits from PriceScrapter. A specific class to scrape game
    prices from the playstation network.
    """

    def __init__(self, product):
        """
            :param product: dictionairy containing product info used
                to scrape webpage.
            :type product: dict
        """

        super().__init__()
        self.product = product
        self.get_price()

    def get_price(self):
        """
        Scrape psn link to find current game price. returns the current
        price as a float.
        """

        p = requests.get(self.product["link"])
        soup = BeautifulSoup(p.content, "html.parser")
        el = "h3"
        search = {"class": "price-display__price"}
        self.price = float(soup.findAll(el, search)[0].get_text()[1:].replace(",","."))