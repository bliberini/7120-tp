import json

class Stock:
  def __init__(self, ticker, name):
    self.ticker = ticker
    self.name = name

  def serialize(self):
    return {
      'ticker': self.ticker,
      'name': self.name
    }