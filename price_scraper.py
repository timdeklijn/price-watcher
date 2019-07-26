import datetime

class PriceScraper():
    """
    Base class used to scrape product prices from webpages. Will be
    inherited by webshop specific scraper classes

    Attributes
    ----------
        date : str
            string formatted current date

    Methods
    -------
        get_product_info()
            Based on scraped info create a dict with info on product.
    """

    def __init__(self):
        """
        Parameters
        ----------
            None
        """
        self.date = self._get_current_date()

    def _get_current_date(self):
        """
        Returns a formatted string containing current date.
        String is formatted: YYYY-MM-DD

        Parameters
        ----------
            None

        Returns
        -------
            string
                a formatted string of current date
        """
        return datetime.datetime.now().strftime("%Y-%m-%d")

    def get_product_info(self):
        """
        Create an output dict containing the product name, date and price

        Parameters
        ----------
            None

        Returns
        -------
            dict
                Product info
        """
        return {
            "name" : self.product["name"], 
            "store" : self.product["store"], 
            "date" : self.date, 
            "price" : self.price}