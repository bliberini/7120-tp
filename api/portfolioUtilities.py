import numpy as np

def calculate_return(weights, returns):
    return (np.asarray(weights) * returns).sum()

def calculate_std(weights, cov_matrix):
    return np.dot(np.dot(np.asarray(weights), cov_matrix),np.asarray(weights).transpose())
