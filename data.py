import pandas as pd
import os

class Data():
    """
    Add newly scraped data to historical data, check for duplicates
    and return all requested data as a pandas dataframe

    Attributes
    ----------
        new_data : list[dict]
            List of dicts containing scraped data
        datafile : str
            File location of historical data
        df : pandas dataframe
            Contains historic and new data
    
    Methods
    -------
        load_data()
            If a (csv) file exists at self.datafile, load the file
            else create a new dataframe with the required columns
        prep_new_data()
            Convert the newly scraped data to a pandas dataframe
        append_new_data()
            Write the new data to the datafile
        load_all_data()
            Load all data from the datafile
        get_unique_rows()
            Check if there are duplicate rows in the dataframe
    """

    def __init__(self, new_data):
        """
        Parameters
        ----------
            new_data : list(dict)
                List containing dicts with new data
        """

        self.new_data = new_data
        self.datafile = "tst_data/price_data.csv"
        self.df = None
        self.prep_new_data()
        self.load_data()
        self.concat_dfs()
        self.get_unique_rows()
        self.write_data()

    def load_data(self):
        """
        Check if datafile exists, if not, create a new dataframe with
        the required columns

        Parameters:
            self.datafile : str
                File location of historical data
            self.df : pandas dataframe
                dataframe that will contain all data
        """

        if os.path.exists(self.datafile):
            with open(self.datafile, "r") as f:
                self.df = pd.read_csv(f)
        else:
            self.df = pd.DataFrame(
                columns = ["name", "store", "date", "price"])

    def write_data(self):
        """
        Write self.df to a csv file at self.datafile

        Parameters
        ----------
            self.datafile : str
                File location of historical data
            self.df : pandas dataframe
                dataframe that containing all data
        """

        with open(self.datafile, "w") as f:
            self.df.to_csv(f, index=False)

    def prep_new_data(self):
        """
        Convert newly scraped data to a pandas dataframe

        Parameters
        ----------
            self.new_df : pandas dataframe
                Will contain newly scraped data
            self.new_data : list(dicts)
                List containing dicts with new data
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

        Parameters
        ----------
            self.df : pandas dataframe
                dataframe that containing all data
            self.new_df : pandas dataframe
                dataframe containing newly scraped data
        """

        self.df = pd.concat([self.df, self.new_df])

    def get_unique_rows(self):
        """
        Remove duplicates from the data, duplicates will
        appear when a price is scraped twice on the same day

        Parameters
        ----------
            self.df : pandas dataframe
                dataframe that containing all data
        """

        self.df = self.df.drop_duplicates()