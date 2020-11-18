import pandas as pd
import os

class Data:
    master_df = None
    availibility_df = None
    demand_df = None
    num_applicants = 50
    applicants = None

    def __init__(self):
        pass

    @classmethod
    def _get_master_df(cls):
        if not cls.master_df:
            cls.master_df = pd.read_csv('data.csv', index_col=0)

            # Find number of applicants
            cls.master_df = cls.master_df.T
            cls.master_df = cls.master_df.set_index(['Dept', 'Day', 'Shift'])

            # Convert To Numeric
            cls.master_df.iloc[0:, 0:] = cls.master_df.apply(pd.to_numeric, errors='coerce')

    @classmethod
    def get_demand_df(cls):
        if cls.master_df.empty:
            cls._get_master_df()
        cls.demand_df = cls.master_df.iloc[0:,-1]
        return cls.demand_df

    @classmethod
    def get_availibility_df(cls):
        if cls.master_df.empty:
            cls._get_master_df()
        cls.availibility_df = cls.demand_df[0:,cls.num_applicants]
        return cls.availibility_df

    @classmethod
    def get_num_applicants(cls):
        if cls.master_df.empty:
            cls._get_master_df()
        cls.num_applicants = cls.demand_df[0:, cls.num_applicants]
        return cls.num_applicants

    @classmethod
    def get_applicants(cls):
        if not cls.master_df:
            cls._get_master_df()
        cls.applicants = list(cls.master_df.columns)
        return cls.applicants