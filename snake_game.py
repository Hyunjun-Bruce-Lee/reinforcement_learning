import pygame
import os, random
import numpy as np

# define variables
FPS = 60
SCREEN_SIZE = 30
PIXEL_SIZE = 5
LINE_WIDTH = 1

# define directions
DIRECTIONS = np.array([
  (0, -1), # UP
  (1, 0), # RIGHT
  (0, 1), # DOWN
  (-1, 0) # LEFT
])


class Snake():
    snake, fruit = None, None
    
    # the game will run base on genome
    # s = display window
    def __init__(self, s, genome):
        self.genome = genome
    
        self.s = s
        self.score = 0 # score earned in game
        self.snake = np.array([[15, 26], [15, 27], [15, 28], [15, 29]]) # snake initial position(vertical at x coordinate 15) and length(4)
        self.direction = 0 # snake will face upward when the game start
        self.place_fruit() 
        self.timer = 0 # avoiding infinate loop
        self.last_fruit_time = 0 # infinate loop will be avoided refer to the time after getting a score
    
        self.fitness = 0. # validation indicator for genomes behavior
        self.last_dist = np.inf # distance between current position and current fruit position 
    
    def place_fruit(self, coord=None):
        # function for random fruit placement
        if coord:
            self.fruit = np.array(coord)
            return
    
        while True:
            x = random.randint(0, SCREEN_SIZE-1)
            y = random.randint(0, SCREEN_SIZE-1)
            if list([x, y]) not in self.snake.tolist():
                break
        self.fruit = np.array([x, y])
  
    def step(self, direction):
        # define snake game rule
        # if head goes out (screen) or encounter its own body game over
        # return False if game over else True
        old_head = self.snake[0]
        movement = DIRECTIONS[direction]
        new_head = old_head + movement
    
        if (
            new_head[0] < 0 or
            new_head[0] >= SCREEN_SIZE or
            new_head[1] < 0 or
            new_head[1] >= SCREEN_SIZE or
            new_head.tolist() in self.snake.tolist()
          ):
            return False
        
      # eat fruit
        if all(new_head == self.fruit): # if head encounters fruit
            self.last_fruit_time = self.timer # reset timer
            self.score += 1 # add score
            self.fitness += 10 # reword for getting a score
            self.place_fruit() # place a new fruit
        else:
            tail = self.snake[-1]
            self.snake = self.snake[:-1, :]
    
        self.snake = np.concatenate([[new_head], self.snake], axis=0)
        return True
  
    def get_inputs(self):
        # generate input for genoms
        # inputs for genoms are potential dangers and rewards which snake can see
        head = self.snake[0]
        result = [1., 1., 1., 0., 0., 0.] # result[:3] = flag for gameover, result[3:] = flag for finding fruit
    
        # check forward, left, right (relative direction considering current head facing)
        possible_dirs = [
          DIRECTIONS[self.direction], # straight forward
          DIRECTIONS[(self.direction + 3) % 4], # left
          DIRECTIONS[(self.direction + 1) % 4] # right
        ]
    
        # danger(0) ~ safe(1)
        # getting flags for game over
        for i, p_dir in enumerate(possible_dirs):
            # snake vision range = 5 (snake sees 5 cells)
            for j in range(5):
                guess_head = head + p_dir * (j + 1)
      
                if (
                  guess_head[0] < 0 or
                  guess_head[0] >= SCREEN_SIZE or
                  guess_head[1] < 0 or
                  guess_head[1] >= SCREEN_SIZE or
                  guess_head.tolist() in self.snake.tolist()
                ):
                    result[i] = j * 0.2
                    break
    
        # getting flag for fruit
        # heading straight forward to fruit
        if np.any(head == self.fruit) and np.sum(head * possible_dirs[0]) <= np.sum(self.fruit * possible_dirs[0]):
            result[3] = 1
        # fruit is on the left side
        if np.sum(head * possible_dirs[1]) < np.sum(self.fruit * possible_dirs[1]):
            result[4] = 1
        # fruit is on the right side
        # if np.sum(head * possible_dirs[2]) < np.sum(self.fruit * possible_dirs[2]):
        else:
            result[5] = 1
    
        return np.array(result)
  
    def run(self):
        # define rungame
        self.fitness = 0 # initialize validation indicator
    
        prev_key = pygame.K_UP # initialize initial keyord input
    
        # desine elements in game
        font = pygame.font.Font('/Users/hyunjun_bruce_lee/Library/Fonts/FiraCode-Bold.ttf', 20)
        font.set_bold(True)
        appleimage = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        appleimage.fill((0, 255, 200))
        img = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        img.fill((100, 100, 100))
        clock = pygame.time.Clock()
    
        while True:
            self.timer += 0.1
            # terminate scenario if runtime is too long
            if self.fitness < -FPS/2 or self.timer - self.last_fruit_time > 0.1 * FPS * 5:
                # self.fitness -= FPS/2
                #print('Terminate!')
                break
      
            clock.tick(FPS)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                elif e.type == pygame.KEYDOWN:
                  # QUIT
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    # PAUSE
                    if e.key == pygame.K_SPACE:
                        pause = True
                        while pause:
                            for ee in pygame.event.get():
                                if ee.type == pygame.QUIT:
                                    pygame.quit()
                                elif ee.type == pygame.KEYDOWN:
                                    if ee.key == pygame.K_SPACE:
                                        pause = False
                    if __name__ == '__main__':
                        # CONTROLLER
                        if prev_key != pygame.K_DOWN and e.key == pygame.K_UP:
                            self.direction = 0
                            prev_key = e.key
                        elif prev_key != pygame.K_LEFT and e.key == pygame.K_RIGHT:
                            self.direction = 1
                            prev_key = e.key
                        elif prev_key != pygame.K_UP and e.key == pygame.K_DOWN:
                            self.direction = 2
                            prev_key = e.key
                        elif prev_key != pygame.K_RIGHT and e.key == pygame.K_LEFT:
                            self.direction = 3
                            prev_key = e.key
              
            #   action
            if __name__ != '__main__':
                inputs = self.get_inputs()
                outputs = self.genome.forward(inputs)
                outputs = np.argmax(outputs)
        
                if outputs == 0: # straight
                    pass
                elif outputs == 1: # left
                    self.direction = (self.direction + 3) % 4
                elif outputs == 2: # right
                    self.direction = (self.direction + 1) % 4
      
            if not self.step(self.direction):
                break
      
            # compute fitness
            current_dist = np.linalg.norm(self.snake[0] - self.fruit)
            if self.last_dist > current_dist:
                self.fitness += 1.
            else:
                self.fitness -= 1.5
            self.last_dist = current_dist
      
            self.s.fill((0, 0, 0))
            pygame.draw.rect(self.s, (255,255,255), [0,0,SCREEN_SIZE*PIXEL_SIZE,LINE_WIDTH])
            pygame.draw.rect(self.s, (255,255,255), [0,SCREEN_SIZE*PIXEL_SIZE-LINE_WIDTH,SCREEN_SIZE*PIXEL_SIZE,LINE_WIDTH])
            pygame.draw.rect(self.s, (255,255,255), [0,0,LINE_WIDTH,SCREEN_SIZE*PIXEL_SIZE])
            pygame.draw.rect(self.s, (255,255,255), [SCREEN_SIZE*PIXEL_SIZE-LINE_WIDTH,0,LINE_WIDTH,SCREEN_SIZE*PIXEL_SIZE+LINE_WIDTH])
            for bit in self.snake:
                self.s.blit(img, (bit[0] * PIXEL_SIZE, bit[1] * PIXEL_SIZE))
            self.s.blit(appleimage, (self.fruit[0] * PIXEL_SIZE, self.fruit[1] * PIXEL_SIZE))
            score_ts = font.render(str(self.score), False, (255, 255, 255))
            self.s.blit(score_ts, (5, 5))
            pygame.display.update()
    
        return self.fitness, self.score



if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    s = pygame.display.set_mode((SCREEN_SIZE * PIXEL_SIZE, SCREEN_SIZE * PIXEL_SIZE))
    pygame.display.set_caption('Snake')
  
    while True:
        snake = Snake(s, genome=None)
        fitness, score = snake.run()
    
        print('Fitness: %s, Score: %s' % (fitness, score))
