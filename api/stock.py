import json

class Stock:
  def __init__(self, ticker, name, roi, std):
    self.ticker = ticker
    self.name = name
    self.roi = roi
    self.std = std

  def serialize(self):
    return {
      'ticker': self.ticker,
      'name': self.name,
      'roi': self.roi,
      'std': self.std
    }