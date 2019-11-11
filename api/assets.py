import pandas as pd
import numpy as np

def parse_assets():
    assets =  ['AAPL', 'GM', 'MSFT', 'TSLA', 'SPOT', 'BOA', 'KO']
    df = pd.read_csv("assets.csv")
    returns = parse_returns(df)
    cov_matrix, variance = parse_covariance(df)
    return assets, returns, cov_matrix, variance

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