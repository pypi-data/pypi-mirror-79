from itertools import chain
from sklearn import base
import pandas as pd
import numpy as np
import os
import glob
import datetime

class AddArticleInfo(base.BaseEstimator, base.TransformerMixin):
    def __init__(self, RAW_DATA_PATH, BASE_ARTICLE_FILENAME, CLASSIFICATION_ARTICLE_FILENAME, add_base_article=True, add_classification=True):
        self.RAW_DATA_PATH = RAW_DATA_PATH
        self.BASE_ARTICLE_FILENAME = BASE_ARTICLE_FILENAME
        self.CLASSIFICATION_ARTICLE_FILENAME = CLASSIFICATION_ARTICLE_FILENAME
        self.add_base_article = add_base_article
        self.add_classification = add_classification

    def fit(self, X):
        return self

    def transform(self, X):
        if self.add_base_article:
            base_article = pd.read_csv(os.path.join(self.RAW_DATA_PATH, self.BASE_ARTICLE_FILENAME), sep=';', usecols=[
                                       0, 9, 11], dtype={'CODE_ARTICLE': str, 'SUR_FAMILLE': str, 'FAMILLE': int})
            X = X.merge(base_article, on='CODE_ARTICLE', how='left')
        if self.add_classification:
            classification_article = pd.read_csv(os.path.join(self.RAW_DATA_PATH, self.CLASSIFICATION_ARTICLE_FILENAME), sep=';',  usecols=[
                                                 0, 4], dtype={'CODE_ARTICLE': str, 'CLASSE_ABC': 'int8'})
            X = X.merge(classification_article, on='CODE_ARTICLE', how='left')
            X['CLASSE_ABC'] = X['CLASSE_ABC'].fillna(5)
            X['CLASSE_ABC'] = X['CLASSE_ABC'].astype(np.int8)
        return X
