'''
import modules
'''
import argparse
import datetime as dt
import pandas as pd
import pandas_datareader as pdr
from matplotlib import pyplot as plt
from matplotlib import style


'''
getting historical stock price data
'''
class Simple_chart():
    def __init__(self, stock_code):
        self.stock_code = stock_code

    def ingest(self):
        style.use('ggplot')
        start = dt.datetime(2000, 1, 1)
        today = dt.date.today()
        end = dt.datetime(today.year,
                        today.month,
                        today.day)
        #getting stock price data from Yahoo Finance
        df = pdr.DataReader(self.stock_code,
                            'yahoo',
                            start,
                            end)
        self.df = df
        return df

    def set_ma(self, ma):
        self.df[str(ma) + 'ma'] = self.df['Adj Close'].rolling(window = int(ma)).mean()
        self.df.dropna(inplace = True)
        self.ma = ma
        self.df = self.df

        return self.df

    def visualize(self, df, options):
        #manage subplots
        ax1 = plt.subplot2grid((6,1),
                               (0,0),
                               rowspan = 5,
                               colspan = 1)
        ax2 = plt.subplot2grid((6,1),
                               (5,0),
                               rowspan = 1,
                               colspan = 1,
                               sharex = ax1)
        
        plt.title('Stock code: {} with moving average: {}'.format(self.stock_code, self.ma),
                  y = 7)
        
        for item in options:
            if options != 'Volume':
                ax1.plot(self.df.index, 
                        self.df[item])
        ax1.legend(options)
        ax2.bar(df.index,
                self.df['Volume'])
        ax2.legend(['Volume'])

        plt.show()    
    

