import numpy as np
import pygame, random
from copy import deepcopy
from snake_game import Snake, SCREEN_SIZE, PIXEL_SIZE


class Genome():
  def __init__(self):
    self.fitness = 0
    # define weight matrix
    hidden_layer = 10
    self.w1 = np.random.randn(6, hidden_layer)
    self.w2 = np.random.randn(hidden_layer, 20)
    self.w3 = np.random.randn(20, hidden_layer)
    self.w4 = np.random.randn(hidden_layer, 3)
    
  def forward(self, inputs):
    # define foward method
    net = np.matmul(inputs, self.w1)
    net = self.relu(net)
    net = np.matmul(net, self.w2)
    net = self.relu(net)
    net = np.matmul(net, self.w3)
    net = self.relu(net)
    net = np.matmul(net, self.w4)
    net = self.softmax(net)
    return net
  
  # define activation function
  def relu(self, x):
    return x * (x >= 0)

  def softmax(self, x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

  def leaky_relu(self, x):
    return np.where(x > 0, x, x * 0.01)







N_POPULATION = 50 # number of worker
N_BEST = 5
N_CHILDREN = 5
PROB_MUTATION = 0.4



pygame.init()
pygame.font.init()
s = pygame.display.set_mode((SCREEN_SIZE * PIXEL_SIZE, SCREEN_SIZE * PIXEL_SIZE))
pygame.display.set_caption('Snake')

# generate 1st population
genomes = [Genome() for _ in range(N_POPULATION)]
best_genomes = None

n_gen = 0
while True:
  n_gen += 1

  for i, genome in enumerate(genomes):
    snake = Snake(s, genome=genome)
    fitness, score = snake.run()

    genome.fitness = fitness

    # print('Generation #%s, Genome #%s, Fitness: %s, Score: %s' % (n_gen, i, fitness, score))

  if best_genomes is not None:
    genomes.extend(best_genomes)
  genomes.sort(key=lambda x: x.fitness, reverse=True)

  print('===== Generaton #%s\tBest Fitness %s =====' % (n_gen, genomes[0].fitness))
  # print(genomes[0].w1, genomes[0].w2)

  best_genomes = deepcopy(genomes[:N_BEST])

  # crossover
  for i in range(N_CHILDREN):
    new_genome = deepcopy(best_genomes[0])
    a_genome = random.choice(best_genomes)
    b_genome = random.choice(best_genomes)

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

    best_genomes.append(new_genome)

  # mutation
  genomes = []
  for i in range(int(N_POPULATION / (N_BEST + N_CHILDREN))):
    for bg in best_genomes:
      new_genome = deepcopy(bg)

      mean = 20
      stddev = 10

      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.w1 += new_genome.w1 * np.random.normal(mean, stddev, size=(6, 10)) / 100 * np.random.randint(-1, 2, (6, 10))
      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.w2 += new_genome.w2 * np.random.normal(mean, stddev, size=(10, 20)) / 100 * np.random.randint(-1, 2, (10, 20))
      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.w3 += new_genome.w3 * np.random.normal(mean, stddev, size=(20, 10)) / 100 * np.random.randint(-1, 2, (20, 10))
      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.w4 += new_genome.w4 * np.random.normal(mean, stddev, size=(10, 3)) / 100 * np.random.randint(-1, 2, (10, 3))

      genomes.append(new_genome)
