from candidate import Candidate
from randomPortfolioGenerator import Random_Portfolio_Generator
import portfolioUtilities
import numpy as np
import random
import time

class Genetic_Algorithm_Portfolio:
    def __init__(self, max_risk, generations, returns, cov_matrix):
        '''
        Creates a genetic algorithm portfolio generator

        - population: list of Candidate objects
        - max_risk: risk constraint the portfolio must meet
        - generations: number of generations the algorithm will run to create a better solution
        '''
        
        self.max_risk = max_risk
        self.generations = generations
        self.returns = returns
        self.cov_matrix = cov_matrix

    def generate_portfolio(self):
        #print("Generating portfolio")
        # Map solutions so that the Candidate objects also have normalized fitness value and cummulative sum
        t0 = time.time()
        random_generator = Random_Portfolio_Generator(5000, self.max_risk, self.returns, self.cov_matrix)
        t1 = time.time()
        print("Time to generate random set: " + str(int(t1 - t0)) + " seconds")
        self.initial_population = random_generator.generate_solutions()[0]
        if len(self.initial_population) == 0:
            return None
        self.map_solutions()
        current_generation = self.initial_population
        initial_weight = [0]*len(self.initial_population[0].weights)
        best_solution = Candidate(
            initial_weight,
            portfolioUtilities.calculate_return(initial_weight, self.returns),
            portfolioUtilities.calculate_std(initial_weight, self.cov_matrix)
        )

        # With this initial population, run 100 generations
        improvements = 100
        for i in range(self.generations):
            t_g0 = time.time()
            if improvements == 0:
                print("No improvements after 100 generations")
                break

            # Next generation will be those selected by the selection method + the 10 best by expected return from the current generation
            t_s0 = time.time()
            next_gen_selected = self.next_generation(current_generation)
            current_generation.sort(key=lambda x: x.expected_return, reverse=True)
            next_gen_selected = next_gen_selected + current_generation[:10]
            t_s1 = time.time()
            print(f"Next generation selection: {str(int(t_s1 - t_s0))} seconds")

            # Pair parents
            t_p0 = time.time()
            parents = self.pair(next_gen_selected)
            t_p1 = time.time()
            print(f"Parents selection: {str(int(t_p1 - t_p0))} seconds")
            
            # Cross them and create the next gen
            next_gen = []
            t_c0 = time.time()
            for j in range(len(parents)):
                next_gen = next_gen + self.cross(parents[j])

            # Check if you found a better solution
            next_gen.sort(key=lambda x: x.expected_return, reverse=True)
            t_c1 = time.time()
            print(f"Cross: {str(int(t_c1 - t_c0))} seconds")
            if len(next_gen) == 0:
                continue

            next_gen_best_solution = next_gen[0]
            if (best_solution.expected_return < next_gen_best_solution.expected_return):
                best_solution = next_gen_best_solution
                improvements = 100
            else:
                improvements -= 1
            
            # Next generation is now current generation
            current_generation = next_gen
            t_g1 = time.time()
            print(f">>> Generation {i} time: {str(int(t_g1 - t_g0))} seconds")
        #print("Done!")
        return best_solution
        
    def judge_candidates(self, candidates):
        return list(filter(lambda x: x.std <= self.max_risk and all(i >= 0 for i in x.weights), candidates))

    def mutate(self, candidate):
        if (random.randint(0, 100) <= 2):
            gene_one = random.randint(0, len(candidate) - 1)
            gene_two = random.randint(0, len(candidate) - 1)
            deviation = random.gauss(0, 0.001)
            candidate[gene_one] += deviation
            candidate[gene_two] -= deviation
        return candidate

    def cross(self, parents):
        x1 = parents[0].weights
        x2 = parents[1].weights
        d = (x1 - x2) / 3
        x3 = self.mutate(x1 + d)
        x4 = self.mutate(x1 - d)
        x5 = self.mutate(x2 + d)
        x6 = self.mutate(x2 - d)

        return sorted(self.judge_candidates([
            parents[0],
            parents[1],
            Candidate(
                x3,
                portfolioUtilities.calculate_return(x3, self.returns),
                portfolioUtilities.calculate_std(x3, self.cov_matrix)
            ),
            Candidate(
                x4,
                portfolioUtilities.calculate_return(x4, self.returns),
                portfolioUtilities.calculate_std(x4, self.cov_matrix)
            ),
            Candidate(
                x5,
                portfolioUtilities.calculate_return(x5, self.returns),
                portfolioUtilities.calculate_std(x5, self.cov_matrix)
            ),
            Candidate(
                x6,
                portfolioUtilities.calculate_return(x6, self.returns),
                portfolioUtilities.calculate_std(x6, self.cov_matrix)
            )
        ]), key=lambda x: x.expected_return, reverse=True)[:2]

    def map_solutions(self):
        self.initial_population.sort(key=lambda x: x.expected_return)
        returns_array = np.asarray([x.expected_return for x in self.initial_population])
        returns_array = (returns_array - returns_array.min()) / (returns_array - returns_array.min()).sum()
        previous = 0
        for i in range(len(self.initial_population)):
            self.initial_population[i].norm_fitness = returns_array[i]
            self.initial_population[i].cum_sum = self.initial_population[i].norm_fitness + previous
            previous += self.initial_population[i].norm_fitness

    def next_generation(self, current):
        # Select chromosomes to pair
        cum_sums = [o.cum_sum for o in self.initial_population]
        selected = []
        for x in range(len(cum_sums)//2):
            selected.append(self.roulette(cum_sums, np.random.rand()))

            # In case the roulette picks an index that has already been picked
            while len(set(selected)) != len(selected):
                selected[x] = self.roulette(cum_sums, np.random.rand())
        
        return [self.initial_population[int(selected[x])] for x in range(len(self.initial_population)//2)]

    def roulette(self, cum_sum, chance):
        veriable = list(cum_sum.copy())
        veriable.append(chance)
        veriable = sorted(veriable)
        return veriable.index(chance)
    
    def pair(self, generation):
        # Pairs selected chromosomes by fitness
        return [generation[i:i + 2] for i in range(0, len(generation), 2)]