from sklearn import base
import pandas as pd
import numpy as np

class ToSupervised(base.BaseEstimator, base.TransformerMixin):
	
    def __init__(self, col, groupCol, numLags, dropna=False):

        self.col = col
        self.groupCol = groupCol
        self.numLags = numLags
        self.dropna = dropna

    def fit(self, X, y=None):
        self.X = X
        return self

    def transform(self, X):
        tmp = self.X.copy()
        print('creating shift columns...')
        for i in range(1, self.numLags+1):
            tmp[str(i)+'_Time_Inc_Ago'+"_" +
                self.col] = tmp.groupby(self.groupCol)[self.col].shift(i)

        if self.dropna:
            tmp = tmp.dropna()
            tmp = tmp.reset_index(drop=True)

        return tmp