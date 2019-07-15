from price_scraper import PriceScraper
import requests
from bs4 import BeautifulSoup

class PSNScraper(PriceScraper):
    """
    Inherits from PriceScrapter. A specific class to scrape game prices from
    the playstation network.

    Attributes
    ----------
        product : dict
            dictionairy containing info to scrape product
        date : str
            string formatted current date

    Methods
    -------
        get_price()
            Scrape the PSN for the price of a playstation game 
    """

    def __init__(self, product):
        """
        Parameters
        ----------
            product : dict
                dictionairy containing product info used to scrape 
                webpage.
        """
        super().__init__()
        self.product = product
        self.get_price()

    def get_price(self):
        """
        Scrape psn link to find current game price. returns the current 
        price as a float.

        Parameters
        ----------
            l : str
                Link to webpage to scrape

        Returns
        -------
            float
                price scraped form webpage
        """

        p = requests.get(self.product["link"])
        soup = BeautifulSoup(p.content, "html.parser")
        el = "h3"
        search = {"class": "price-display__price"}
        self.price = float(soup.findAll(el, search)[0].get_text()[1:].replace(",","."))