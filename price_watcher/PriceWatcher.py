

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
from datetime import datetime
import numpy as np
import os
import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

matplotlib.use('Agg')
plt.style.use('ggplot')
register_matplotlib_converters()

class PriceWatcher():
    """ 
    Handles the data, plotting and sending of the plots
    """

    def __init__(self, new_data, config):
        """
            :param new_data: scraped price data
            :type new_data: pandas dataframe
            :param config: run config
            :type config: dict
        """

        self.new_data = new_data
        self.data_file = "bucket/price_data.csv"
        self.plot_file = "bucket/tmp.png"
        self.df = None
        self.plot_df = None
        self.email_to = "timdeklijn@gmail.com"
        self.email_from = "tim.sends.info@gmail.com"
        self.username = "tim.sends.info"
        self.password = "test1234!"
        self.run()

    def run(self):
        """
        Run the pricewatcher class
        """

        self.prep_new_data()
        self.load_data()
        self.concat_dfs()
        self.get_unique_rows()
        self.write_data()
        self.prep_data()
        self.create_plot()
        self.send_mail()

    def load_data(self):
        """
        Check if data_file exists, if not, create a new dataframe with
        the required columns
        """

        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.df = pd.read_csv(f)
        else:
            self.df = pd.DataFrame(
                columns = ["name", "store", "date", "price"])

    def write_data(self):
        """
        Write self.df to a csv file at self.data_file
        """

        with open(self.data_file, "w") as f:
            self.df.to_csv(f, index=False)

    def prep_new_data(self):
        """
        Convert newly scraped data to a pandas dataframe
        """

        self.new_df = pd.DataFrame(data={
            "name" : [i["name"] for i in self.new_data],
            "store" : [i["store"] for i in self.new_data],
            "date" : [i["date"] for i in self.new_data],
            "price" : [i["price"] for i in self.new_data],
        })

    def concat_dfs(self):
        """
        Append the new data to the historic data
        """

        self.df = pd.concat([self.df, self.new_df])

    def get_unique_rows(self):
        """
        Remove duplicates from the data, duplicates will
        appear when a price is scraped twice on the same day
        """

        self.df = self.df.drop_duplicates()

    def prep_data(self):
        """
        Modify dataframe containing all scraped data to
        a format that can be plotted
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

    def send_mail(self):
        
        subject = f"[{datetime.datetime.now().strftime('%Y-%m-%d')}] Pricewatch"
        text = "Info on averages"

        msg = MIMEMultipart()
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        img_data = open(self.plot_file, 'rb').read()
        image = MIMEImage(img_data, name=os.path.basename(self.plot_file))
        msg.attach(image)

        smtp = smtplib.SMTP(host="smtp.gmail.com", port= 587) 
        smtp.starttls()
        smtp.login(self.username, self.password)
        smtp.sendmail(self.email_from, self.email_to, msg.as_string())
        smtp.close()