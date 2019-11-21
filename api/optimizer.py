from pandas_datareader import data as web
from assets import parse_assets
from randomPortfolioGenerator import Random_Portfolio_Generator
from geneticAlgorithmPortfolioGenerator import Genetic_Algorithm_Portfolio

class Optimizer:
    def __init__(self, max_risk):
        self.max_risk = max_risk
        self.assets, self.returns, self.cov_matrix, self.variance = parse_assets()

    def generate_random_portfolio(self):
        generator = Random_Portfolio_Generator(1000, self.max_risk, self.returns, self.cov_matrix)
        solutions, best_solution, best_return, best_std = generator.generate_solutions()
        return solutions, best_solution, best_return, best_std
    
    def generate_genetic_algorithm_portfolio(self):
        generator = Genetic_Algorithm_Portfolio(self.max_risk, 50, self.returns, self.cov_matrix)
        return generator.generate_portfolio()