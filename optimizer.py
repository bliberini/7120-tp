from pandas_datareader import data as web
import pandas as pd
import numpy as np

assets =  ['AAPL', 'GM', 'GE', 'FB', 'WMT']

df = pd.DataFrame()

for stock in assets:
    df[stock] = web.DataReader(stock, data_source='yahoo',start='2019-1-1' ,end='2019-10-1')['Adj Close']

# Simple daily returns with .pct_change() method  
d_returns = df.pct_change()

# Construct a covariance matrix for the portfolio's daily returns with the .cov() method
cov_matrix_d = d_returns.cov()

# Annualise the daily covariance matrix with the standard 250 trading days
cov_matrix_a = cov_matrix_d * 250
weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

# Calculate the variance with the formula
port_variance = np.dot(weights.T, np.dot(cov_matrix_a, weights))

# The standard deviation of a portfolio is just a square root of its variance
port_volatility = np.sqrt(port_variance)

#--------------

# Annualise daily returns. 250 trading days in a year
annual_returns = d_returns.mean() * 250

print("--- Returns ---")
print(annual_returns)

print("--- Volatility ---")
print(cov_matrix_a)

# Calculate the expected return of the portfolio
port_returns_expected = np.sum(weights * annual_returns)