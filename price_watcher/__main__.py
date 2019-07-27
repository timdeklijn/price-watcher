"""main
Scrape products listed in the config file. Update the data, create
graphs and send an email with updated graphs and additional pricing
info.
"""

__version__ = "0.0"
__author__ = "Tim de Klijn"

import json

from price_watcher.psn_scraper import PSNScraper
from price_watcher.PriceWatcher import PriceWatcher

def read_config():
    """
    Read the config file and return a dictionairy with
    the configuration.

        :returns: Config in dict form
    """
    config_location = "bucket/config.json"
    with open(config_location, "r") as f:
        config = json.load(f)
    return config

def get_price_data(config):
    """
    For products listed in config, get the matching webshop
    and scrape the price of the product. Place in a list and
    return the list.

        :param config: dictionairy containing info on products to look
            for the price of
        :type config: dict
        :returns: List with found prices, dates and product name in
            a dictionairy.
        :rtype: list(dict)
    """

    price_dict = []
    for product in config["products"]:
        if product["store"] == "psn":
            scraper = PSNScraper(product)
        if product["store"] == "bol.com":
            pass
        price_dict.append(scraper.get_product_info())
    return price_dict

def main():
    print("Price watcher")
    config = read_config()
    PriceWatcher(get_price_data(config))

if __name__ == "__main__":
    main()