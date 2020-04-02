import math
import random
from dna import *
from simulate import *


class Generation:

    def __init__(self, population_size, mutation_rate, screen_dim):
        """
        Initializes the attributes of a generation
        """
        self.screen_dim = screen_dim
        self.generation_count = 1
        self.population_size = population_size
        self.population = []
        self.mating_pool = []
        self.mutation_rate = mutation_rate

    def populate(self):
        """
        Generate random birds for population
        """
        for count in range(self.population_size):
            bird = DNA(self.screen_dim)
            self.population.append(bird)

    def calculate_fitness(self):
        """
        Calculate fitness for each bird by running game which sets score for each population member
        Implements scaling then softmax algorithm to convert scores into probability fitnesses
        """
        g = Game(self.population)
        g.main_loop()
        self.population = g.get_population()
        sum = 0
        soft_max_sum = 0
        for bird in self.population:
            sum += bird.score
        for bird in self.population:
            soft_max_sum += math.exp(bird.score / sum)
        for bird in self.population:
            bird.fitness = math.exp(bird.score) / soft_max_sum

    def gen_mating_pool(self):
        """
        Creates mating pool for population of birds, assuming fitness has been calculated
        Scales (probabilistic fitnesses) and adds weighted number of birds to pool
        """
        for bird in self.population:
            num = int(bird.fitness * 1000)
            for i in range(num):
                self.mating_pool.append(bird)

    def reproduction(self):
        """
        Generates new population, overwriting old
        Employs crossover and mutation for heredity/variation
        """
        next_population = []
        for count in range(self.population_size):
            idx1 = random.randint(0, len(self.mating_pool) - 1)
            idx2 = random.randint(0, len(self.mating_pool) - 1)
            parent1 = self.mating_pool[idx1]
            parent2 = self.mating_pool[idx2]
            child = DNA(self.screen_dim)
            child.crossover(parent1, parent2)
            child.mutate(self.mutation_rate)
            next_population.append(child)
        self.population = next_population
        self.generation_count += 1
