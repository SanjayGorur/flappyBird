from generation import *
import tensorflow as tf

screen_dim = (700, 700)
num_generations = 50
population_size = 10
mutation_rate = 0.02


gen = Generation(population_size, mutation_rate, screen_dim)
gen.populate()

while gen.generation_count <= num_generations:
    gen.calculate_fitness()
    gen.gen_mating_pool()
    gen.reproduction()
