import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
from datetime import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

class Plot():
    """
    Base class used to scrape product prices from webpages. Will be
    inherited by webshop specific scraper classes

    Attributes
    ----------
        df: pandas dataframe
            contains scraped + historical data
        plot_file : string
            file name + location of plot to create

    Methods
    -------
        prep_data()
            Transform data to be plotted
        create_plot()
            plot the data
    """

    def __init__(self, df):
        """
        Parameters
        ----------
            df: pandas dataframe
                contains scraped + historical data
        """
        self.df = df
        self.prep_data()
        self.plot_file = "bucket/tmp.png"
        self.create_plot()

    def prep_data(self):
        """
        Modify dataframe containing all scraped data to
        a format that can be plotted

        Parameters
        ----------
            None
        """

        self.plot_df = self.df.drop("store", axis=1)
        self.plot_df = self.plot_df.pivot(index="date", columns="name")
        self.plot_df.columns = self.plot_df.columns.droplevel()
        self.plot_df["date"] = self.plot_df.index
        self.plot_df["date"] = pd.to_datetime(self.plot_df["date"])
        self.plot_df.index = range(len(self.plot_df))

    def create_plot(self):
        """
        Create a plot of the transformed data and save to file
        """

        plt.ioff()
        fig = plt.figure()
        for n in self.plot_df.columns:
            if n != "date":
                plt.plot(self.plot_df.date, self.plot_df[n], label=n, linestyle='-', marker='o')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        x_tick_labels = self.plot_df.date.map(lambda t: t.strftime('%Y-%m-%d'))
        plt.xticks(self.plot_df.date, x_tick_labels, rotation='vertical')
        plt.title("Prices of products over time")
        plt.xlabel("Date")
        plt.ylabel("Price (EUR)")
        fig.savefig(self.plot_file, bbox_inches='tight')

    