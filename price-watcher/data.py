import pandas as pd
import os

class Data():

    def __init__(self, new_data):
        self.new_data = new_data
        self.datafile = "tst_data/price_data.csv"
        self.prep_new_data()
        self.append_new_data()
        self.df = None
        self.load_all_data()
        self.get_unique_rows()
        print(self.df)

    def get_old_data(self):
        if os.path.exists(self.datafile):
            with open(self.datafile, "r") as f:
                self.df = pd.read_csv(f)
        else:
            self.pd = None

    def prep_new_data(self):
        self.new_df = pd.DataFrame(data={
            "name" : [i["name"] for i in self.new_data],
            "store" : [i["store"] for i in self.new_data],
            "date" : [i["date"] for i in self.new_data],
            "price" : [i["price"] for i in self.new_data],
        })

    def append_new_data(self):
        if not os.path.exists(self.datafile):
            with open(self.datafile, "w") as f:
                self.new_df.to_csv(f, index=False)
        else:
            with open(self.datafile, "a") as f:
                self.new_df.to_csv(f, header=False, index=False)

    def load_all_data(self):
        with open(self.datafile, "r") as f:
            self.df = pd.read_csv(f)

    def get_unique_rows(self):
        len_before = len(self.df)
        self.df = self.df.drop_duplicates()
        if len_before != len(self.df):
            with open(self.datafile, "w") as f:
                self.new_df.to_csv(f, index=False)