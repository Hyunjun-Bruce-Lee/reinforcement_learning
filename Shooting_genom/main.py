import numpy as np
import pygame, random
from copy import deepcopy
from shooting_game import shooting, SCREEN_SIZE, PIXEL_SIZE
import pickle
from datetime import datetime

class Genome():
    def __init__(self):
        self.fitness = 0
        self.simulation_time = 10
        # define weight matrix
        hidden_layer = 10
        self.w1 = np.random.randn(30, hidden_layer)
        self.w2 = np.random.randn(hidden_layer, 20)
        self.w3 = np.random.randn(20, hidden_layer)
        self.w4 = np.random.randn(hidden_layer, 3)
      
    def forward(self, inputs):
        # define foward method
        net = np.matmul(inputs, self.w1)
        net = self.leaky_relu(net)
        net = np.matmul(net, self.w2)
        net = self.leaky_relu(net)
        net = np.matmul(net, self.w3)
        net = self.leaky_relu(net)
        net = np.matmul(net, self.w4)
        net = self.softmax(net)
        return net
    
    def softmax(self, x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)
  
    def leaky_relu(self, x):
        return np.where(x > 0, x, x * 0.01)


load_genomes = False
genome_dir = './genoms/genom.bin'


N_POPULATION = 50 # number of genoms (pool)
N_BEST = 5 # number of genoms to keep after each generation (if n == 5, ~ Top 5)
N_CHILDREN = 5 # number of childrens in each generation
PROB_MUTATION = 0.4


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_SIZE * PIXEL_SIZE, SCREEN_SIZE * PIXEL_SIZE))
pygame.display.set_caption('shooting')

if load_genomes == True:
   with open(genome_dir, 'rb') as f:
      genomes = pickle.load(f)
else :
    genomes = [Genome() for _ in range(N_POPULATION)]

best_genomes = None

n_gen = 0
while True:
    time_a = datetime.now()

    n_gen += 1
  
    for i, genome in enumerate(genomes):
        snake = shooting(screen, genome=genome)
        fitness, score = snake.run(genome.simulation_time)
    
        genome.fitness = fitness
    
        # print('Generation #%s, Genome #%s, Fitness: %s, Score: %s' % (n_gen, i, fitness, score))

    if best_genomes is not None:
        genomes.extend(best_genomes)
    genomes.sort(key=lambda x: x.fitness, reverse=True)

    time_b = datetime.now()
    
    with open(genome_dir, 'wb') as f:
       pickle.dump(genomes, f)

    print(f'>>> Generaton #{n_gen}\n\tBest Fitness {genomes[0].fitness}\n\tsimulation time : {time_b - time_a}')
    # print(genomes[0].w1, genomes[0].w2)
  
    best_genomes = deepcopy(genomes[:N_BEST])
    
    # create children
    for i in range(N_CHILDREN):
        new_genome = deepcopy(best_genomes[0])
        # extract two genomes from best genomes for inheritance
        a_genome = random.choice(best_genomes)
        b_genome = random.choice(best_genomes)

        # randomly inherit from extracted two genomes (extracted genomes are father and mother)
        # created genom(children) will be configured based on its mother and father
        # the persentage is random (mother & father)
        cut = random.randint(0, new_genome.w1.shape[1])
        new_genome.w1[i, :cut] = a_genome.w1[i, :cut]
        new_genome.w1[i, cut:] = b_genome.w1[i, cut:]

        cut = random.randint(0, new_genome.w2.shape[1])
        new_genome.w2[i, :cut] = a_genome.w2[i, :cut]
        new_genome.w2[i, cut:] = b_genome.w2[i, cut:]

        cut = random.randint(0, new_genome.w3.shape[1])
        new_genome.w3[i, :cut] = a_genome.w3[i, :cut]
        new_genome.w3[i, cut:] = b_genome.w3[i, cut:]

        cut = random.randint(0, new_genome.w4.shape[1])
        new_genome.w4[i, :cut] = a_genome.w4[i, :cut]
        new_genome.w4[i, cut:] = b_genome.w4[i, cut:]

        new_genome.simulation_time += 2

        # add created genom to best genome group (as its constructed with the ones from best genomes)
        best_genomes.append(new_genome)


    # mutation (add divercity)
    # as childrens are solely based on the perents, the pool of genes are limited to the genes initialized at the begining.
    # to add diversity(for poential oprimal weight) replace partial of childrens gene(respect to mutation probability) with random value and create aditional children with mutation
    # this makes the algorithm not to require differentiation for training which makes it to run much faster
    genomes = []
    for i in range(int(N_POPULATION / (N_BEST + N_CHILDREN))):
        for bg in best_genomes:
            new_genome = deepcopy(bg)
      
            mean = 20
            stddev = 10

            if random.uniform(0, 1) < PROB_MUTATION:
              new_genome.w1 += new_genome.w1 * np.random.normal(mean, stddev, size=(30, 10)) / 100 * np.random.randint(-1, 2, (30, 10))
            if random.uniform(0, 1) < PROB_MUTATION:
              new_genome.w2 += new_genome.w2 * np.random.normal(mean, stddev, size=(10, 20)) / 100 * np.random.randint(-1, 2, (10, 20))
            if random.uniform(0, 1) < PROB_MUTATION:
              new_genome.w3 += new_genome.w3 * np.random.normal(mean, stddev, size=(20, 10)) / 100 * np.random.randint(-1, 2, (20, 10))
            if random.uniform(0, 1) < PROB_MUTATION:
              new_genome.w4 += new_genome.w4 * np.random.normal(mean, stddev, size=(10, 3)) / 100 * np.random.randint(-1, 2, (10, 3))
        
            genomes.append(new_genome)
