import pygame
import random
import numpy as np
from copy import deepcopy

# game related variables
FPS = 60
SCREEN_SIZE = 30
PIXEL_SIZE = 5
LINE_WIDTH = 1


# rewords (+)
SHOOT_REWORD = 1
TARGET_HIT_REWORD = 20

# penalties (-)
BULET_MISS_PENALTY = 1.2
MOVE_OUT_OF_BORD_PENALTY = 0.8


class shooting:
    def __init__(self, screen, genome):
        self.earned_reword = 0
        self.screen = screen
        self.genome = genome
        self.target = None
        self.bulet = list()
        self.shooter = [round(SCREEN_SIZE/2), 3] #shooters initial location
        self.score = 0
        self.generate_target()

    def generate_target(self):
        flag = np.random.randint(100)
        # generate target from left if flag is odd number else from right
        # d stans for direction(direction for bulit to move toward)
        x,d = (0,0) if flag%2 == 1 else (SCREEN_SIZE-1,1)
        self.target = np.array([x,25,d])

    def generate_bulet(self):
        # generate bulet when shooter shoots(K_SPACE)
        self.bulet.append([deepcopy(self.shooter[0]), 4])

    def move_target(self):
        # move_target according to direction
        if self.target[-1] == 0:
            self.target += [1,0,0]
        else:
            self.target -= [1,0,0]
        
        # if target reaches screen border regenerate target
        if self.target[0] in [0,SCREEN_SIZE]:
            self.generate_target()

    def move_bulet(self):
        # move bulet upward
        if len(self.bulet) != 0:
            self.bulet = [[i,j+1] for i,j in self.bulet]
        for i in self.bulet:
            if i[1] >= SCREEN_SIZE:
                self.bulet.remove(i)
                self.earned_reword -= BULET_MISS_PENALTY


    def target_hit_check(self):
        # event when bulet hits the target
        for b in self.bulet:
            if (self.target[0] == b[0]) and (self.target[1] == b[1]):
                self.score += 1
                self.earned_reword += TARGET_HIT_REWORD
                self.generate_target()

    def control(self,key):
        # define actions in game
        new_position = [-1,-1]
        if key == pygame.K_LEFT:
            new_position = np.array(self.shooter) - [1,0]
        elif key == pygame.K_RIGHT:
            new_position = np.array(self.shooter) + [1,0]
        elif key == pygame.K_SPACE:
            self.generate_bulet()
            self.earned_reword += SHOOT_REWORD
        
        if new_position[0] in range(1,SCREEN_SIZE):
            # check shooters position (doesn't move when shooter goes out of screen)
            self.shooter = deepcopy(new_position)
        else:
            self.earned_reword -= MOVE_OUT_OF_BORD_PENALTY

    def generate_inputs(self):
        # genoms will get current screen info as an input
        current_screen_info = np.zeros([SCREEN_SIZE,SCREEN_SIZE])
        current_screen_info[self.target[0]][self.target[1]] = 1 # mark current target location as 1
        return np.array(current_screen_info)

    def run(self, simulation_time):
        font = pygame.font.Font('/Users/hyunjun_bruce_lee/Library/Fonts/FiraCode-Bold.ttf', 20)
        font.set_bold(True)
        shooter_img, bulet_img, target_img = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE)), pygame.Surface((PIXEL_SIZE, PIXEL_SIZE)), pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        shooter_img.fill((0,0,255)), bulet_img.fill((0,255,0)), target_img.fill((255,200,200))
        clock = pygame.time.Clock()
        flag = 0

        while True:
            if flag > simulation_time:
                break
            clock.tick(FPS)
            for e in pygame.event.get():
                # shut down
                if e.type == pygame.QUIT:
                    pygame.quit()
                # moves
                elif e.type == pygame.KEYDOWN:
                    self.control(e.key)

            if __name__ != '__main__':
                inputs = self.generate_inputs()
                outputs = self.genome.forward(inputs)
                out_key = np.argmax(outputs)
                if out_key == 0:
                    key_event = pygame.K_SPACE
                elif out_key == 1:
                    key_event = pygame.K_LEFT
                else:
                    key_event = pygame.K_RIGHT
            
            self.control(key_event)
            if flag%2 == 1:
                self.move_target()
            self.move_bulet()
            self.target_hit_check()

            self.screen.fill((0,0,0))
            self.screen.blit(shooter_img, (self.shooter[0] * PIXEL_SIZE, self.shooter[1] * PIXEL_SIZE))
            self.screen.blit(shooter_img, ((self.shooter[0]+1) * PIXEL_SIZE, self.shooter[1] * PIXEL_SIZE))
            self.screen.blit(shooter_img, ((self.shooter[0]-1) * PIXEL_SIZE, self.shooter[1] * PIXEL_SIZE))
            self.screen.blit(shooter_img, (self.shooter[0] * PIXEL_SIZE, (self.shooter[1] + 1) * PIXEL_SIZE))
            self.screen.blit(target_img, (self.target[0] * PIXEL_SIZE, self.target[1]  * PIXEL_SIZE))
            for b in self.bulet:
                self.screen.blit(bulet_img, (b[0] * PIXEL_SIZE, b[1] * PIXEL_SIZE))
            score_txt = font.render(str(self.score), False, (255, 255, 255))
            self.screen.blit(score_txt, (5,5))
            pygame.display.update()
            flag += 1
        return self.earned_reword, self.score


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    s = pygame.display.set_mode((SCREEN_SIZE * PIXEL_SIZE, SCREEN_SIZE * PIXEL_SIZE))
    pygame.display.set_caption('Shooting')

    while True:
        game = shooting(s,genome = None)
        indicator, score = game.run()
        print(f'indicator : {indicator}, score : {score}')
