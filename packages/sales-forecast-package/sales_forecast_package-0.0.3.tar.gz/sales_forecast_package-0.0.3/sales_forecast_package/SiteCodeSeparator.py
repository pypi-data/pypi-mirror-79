from sklearn import base
import pandas as pd
import numpy as np

class SiteCodeSeparator(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, remove_source=True):
        self.remove_source = remove_source

    def fit(self, X):
        self.X = X
        return self

    def transform(self, X):
        dataset = self.X.copy()
        dataset['SITE'], dataset['CODE_ARTICLE'] = dataset['SITE_CODE'].apply(
            lambda x: int(x.split('_')[0])), dataset['SITE_CODE'].apply(
            lambda x: x.split('_')[1])
        if self.remove_source:
            dataset = dataset.drop(['SITE_CODE'], axis=1)
        return dataset

