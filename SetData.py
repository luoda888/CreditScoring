# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

class SetData(object):
    """
    Set raw dataset
    """

    def __init__(self, datapath, tr_output, test_output):
        self.df = pd.read_csv(datapath)
        self.__setdf()
        self.tr_output = tr_output # outputpath of training data
        self.test_output = test_output # outputpath of test data
        self.clm_drop = ['Currency', 'Name', 'Ratings', 'Filing Date', \
        'End of Next Annual Period','End of Period', 'Report Date'] # list of column names for drop
        self._trData = self.df.drop(self.clm_drop, 1)

    def __setdf(self):
        self.df.index = self.df['Ticker']
        self.df = self.df.T
        self.df = self.df.drop('Ticker')

    def main(self):
        # set training data & test data
        trData = self._trData[self._trData['Ratings #'].notnull()]
        testData = self._trData[self._trData['Ratings #'].isnull()]

        # save raw data
        trData.to_csv(self.tr_output, index = None)
        testData.to_csv(self.test_output, index = None)

class ConvertData(object):
    """
    Standardize data and add some converted dataset
    """

    def __init__(self, datapath, outputpath, ylabel):
        self.df = pd.read_csv(datapath)
        self.outputpath = outputpath
        self.ylabel = ylabel

    def standardize(self, data):
        res = {}
        for i, t in enumerate(list(data.columns)):
            if t == self.ylabel:
                res[t] = list(data[t])
            else:
                x = data[t]
                mu = x.mean()
                sigma = x.std()
                res[t] = x.subtract(mu).div(sigma)
        return pd.DataFrame(res)

#    def add_inverse(self, data):
#        res = data

    def main(self):
        self.df = self.standardize(self.df)
        return self.df

    def saveResult(self):
        self.df.to_csv(self.outputpath, index=None)

if __name__ == '__main__':
    datapath = 'Data_rev.csv'
    tr_output = 'TrainingData_raw_rev.csv'
    test_output = 'testData_raw_rev.csv'

    # set raw data
    sd = SetData(datapath, tr_output, test_output)
#    sd.main()

    # convert training data
    cd_tr = ConvertData('TrainingData_raw_rev.csv', 'TrainingData_rev.csv', 'Ratings #')
    df = cd_tr.main()
    df.ix[27:,:].to_csv('TrainingData_rev.csv', index=None)
    df.ix[:26,:].to_csv('testData_rev.csv', index=None)

    # convert test data
#    cd_test = ConvertData('testData.csv', 'testData.csv')
#    cd_test.main()
