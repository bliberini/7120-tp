import pandas as pd
import numpy as np
import csv
import time
from pandas_datareader import data as web
from stock import Stock

def get_assets():
    assets = []
    with open('stocks.csv') as stocks:
      stocks_reader = csv.reader(stocks, delimiter=',')
      line = 0
      for row in stocks_reader:
        if line != 0:
          assets.append(Stock(row[0], row[1], row[3], row[2]))
        line += 1  
    return assets

def parse_assets(assets):
    df = get_assets_information(assets)
    t0 = time.time()
    returns = parse_returns(df)
    cov_matrix, variance = parse_covariance(df)
    t1 = time.time()
    print("Time to calculate data: " + str(int(t1 - t0)) + " seconds")
    return returns, cov_matrix, variance

def get_assets_information(assets):
    t0 = time.time()
    df = pd.DataFrame()
    for stock in assets:
      df[stock] = web.DataReader(stock, data_source='yahoo',start='2018-01-01' ,end='2018-12-31')['Adj Close']
    t1 = time.time()
    print("Time to fetch data: " + str(int(t1 - t0)) + " seconds")
    return df

def parse_returns(df):
    d_returns = df.pct_change()
    annual_returns = d_returns.mean() * 250
    return np.asarray(annual_returns)

def parse_covariance(df):
    d_returns = df.pct_change()
    cov_matrix_a = d_returns.cov()
    variance = pd.DataFrame(data=np.diag(cov_matrix_a), columns=['variance'], index=cov_matrix_a.index)
    cov_matrix = np.asmatrix(cov_matrix_a)
    return cov_matrix, variance