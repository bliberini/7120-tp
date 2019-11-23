from candidate import Candidate
import portfolioUtilities
import numpy as np
import random

class Random_Portfolio_Generator:
    def __init__(self, n, max_risk, returns, cov_matrix):
        self.num_solutions = n
        self.max_risk = max_risk
        self.returns = returns
        self.cov_matrix = cov_matrix

    def generate_solutions(self):
        solutions = []
        best_solution = []
        best_return = float("-inf")
        best_std = 0
        seed = 42
        counter = 0
        attempts = 0
        while counter < self.num_solutions and attempts < 1000:
            random.seed(seed)
            seed += 1
            weights = self.generate_random_weights()
            solution = Candidate(
                weights,
                portfolioUtilities.calculate_return(weights, self.returns),
                portfolioUtilities.calculate_std(weights, self.cov_matrix)
            )
            if (solution.std <= self.max_risk):
                attempts = 0
                counter +=1
                solutions.append(solution)
                if (solution.expected_return > best_return):
                    best_return = solution.expected_return
                    best_solution = solution
                    best_std = solution.std
            else:
                attempts += 1
        return solutions, best_solution, best_return, best_std
    
    def generate_random_weights(self):
        n = len(self.returns)
        arr = [0] * n
        indexes = list(range(n))
        sum = 0;
        for i in range(n - 1):
            rand = random.randint(0,1000 - sum)
            index = random.choice(indexes)
            indexes.remove(index)
            sum += rand
            arr[index] = rand
        arr[indexes[0]] = 1000 - sum
        return np.array([x / 1000 for x in arr])