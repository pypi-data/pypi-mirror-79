from itertools import chain
from sklearn import base
import pandas as pd
import numpy as np
import os
import glob
import datetime

class ToWeeklySalesDataset(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, DATETYPE_COLUMNS_LIST, DTYPE_DICT, COLS_TO_KEEP, INPUT_FILE_PREFIX, DEBUT_DATE):
        self.DATETYPE_COLUMNS_LIST = DATETYPE_COLUMNS_LIST
        self.DTYPE_DICT = DTYPE_DICT
        self.COLS_TO_KEEP = COLS_TO_KEEP
        self.INPUT_FILE_PREFIX = INPUT_FILE_PREFIX

        self.DEBUT_DATE = DEBUT_DATE

    def fit(self, X):
        self.X = X
        return self

    def transform(self, X):

        X = self.X
        print('###########################')
        print('  WEEKLY SALES RETRIEVAL   ')
        print('###########################\n')
        # initiating returned object
        dataset = X.copy()
        dataset['SITE_CODE'] = dataset['SITE_VENTE'].astype(
            str) + "_" + dataset['CODE_ARTICLE'].astype(str)
        # remove lines with empty date
        dataset = dataset[dataset.DATE_COMMANDE.notna()]
        # remove lines with date prior to debut date
        print('Removing lines with dates prior to debut date of SalesDataset object..')
        dataset = dataset[dataset.DATE_COMMANDE >= self.DEBUT_DATE]

        # sum per DATE and SITE_CODE
        dataset = dataset.groupby(
            ['DATE_COMMANDE', 'SITE_CODE']).sum().reset_index()

        # Expanding time serie for first SITE_CODE in order to have the entire date range (needed for the KFold algorithm afterwards)
        idx = pd.date_range(self.DEBUT_DATE, max(dataset['DATE_COMMANDE']))
        first_site_code = list(dataset.SITE_CODE.unique())[0]
        tmp = dataset[dataset.SITE_CODE == first_site_code].drop(
            ['SITE_CODE'], axis=1).set_index('DATE_COMMANDE')
        tmp = tmp.reindex(idx, fill_value=0).reset_index().rename(
            columns={"index": "DATE_COMMANDE"})
        tmp['SITE_CODE'] = first_site_code
        dataset = pd.concat(
            [dataset[dataset.SITE_CODE != first_site_code], tmp])

        # Coverting dates to integer (date = 0 is the first day of the sample ==> DEBUT_DATE)
        print('Converting date to week number...')
        dataset.DATE_COMMANDE = dataset.DATE_COMMANDE.apply(
            lambda dt_time: (dt_time.date() - datetime.datetime.strptime(self.DEBUT_DATE, "%m-%d-%Y").date()).days//7)
        dataset = dataset.groupby(
            ['DATE_COMMANDE', 'SITE_CODE']).sum().reset_index()
        print('Unstacking dataset...\n')
        dataset = dataset.groupby(['DATE_COMMANDE', 'SITE_CODE']).sum().unstack(
            fill_value=0).stack().reset_index()
        print('###########################')
        print('WEEKLY SALES RETRIEVAL DONE')
        print('###########################')

        return dataset
