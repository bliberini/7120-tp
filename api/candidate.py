import math

class Candidate:
    def __init__(self, weights, expected_return, std):
        self.weights = weights
        self.expected_return = expected_return
        self.std = math.sqrt(std)
        self.print = f"weights: {self.weights}, return = {self.expected_return}, std = {self.std}"