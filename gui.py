import pygame
from pygame.locals import *
import random as r
import time

class Grid:

    def __init__(self, size = 70):
        self.grid = [[0] * 3 for _ in range(3)]
        self.size = size
        self.screen_size = (3*size, 3*size)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.turn = 0

    def next_turn(self):
        if self.turn >=9:
            return
        x = r.randint(0,2)
        y = r.randint(0,2)
        while self.grid[x][y] != 0:
            x = r.randint(0,2)
            y = r.randint(0,2)
        self.draw_zero(x,y)
        self.grid[x][y] = 2
        self.turn += 1


    def draw_cross(self, row, col):
        pygame.draw.line(self.screen, pygame.Color('red'),
                        ((col+0.1)*self.size, (row+0.1)*self.size),
                        ((col+0.9)*self.size, (row+0.9)*self.size), 2)
        pygame.draw.line(self.screen, pygame.Color('red'),
                        ((col+0.1)*self.size, (row+0.9)*self.size),
                        ((col+0.9)*self.size, (row+0.1)*self.size), 2)
        pygame.display.flip()

    def draw_zero(self, row, col):
        pygame.draw.circle(self.screen, pygame.Color('blue'),
                           ((col+0.5)*self.size, (row+0.5)*self.size), self.size*0.47, 2)
        pygame.display.flip()

    def is_win(self):
        if any(tuple(row) == (1,1,1) or tuple(row) == (2,2,2) for row in self.grid) or \
        any(row == (1,1,1) or row == (2,2,2) for row in zip(*self.grid)) or \
        (self.grid[0][0], self.grid[1][1], self.grid[2][2]) in [(1,1,1), (2,2,2)] or \
        (self.grid[0][2], self.grid[1][1], self.grid[2][0]) in [(1,1,1), (2,2,2)]:
            return True
        return False

    def run(self, single = False):
        self.grid = [[0] * 3 for _ in range(3)]
        self.screen.fill(pygame.Color('white'))
        f = pygame.font.Font(None, int(self.size // 1.5))
        for x in range(0, self.size*3, self.size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.size*3))
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, x), (self.size*3, x))
        pygame.display.flip()

        running = True
        self.turn = 0
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in [1,3]:
                        x,y=pygame.mouse.get_pos()
                        y,x=x//self.size, y//self.size
                        if self.grid[x][y] == 0:
                            if self.turn%2 == 0:
                                self.grid[x][y] = 1
                                self.draw_cross(x,y)
                            else:
                                self.grid[x][y] = 2
                                self.draw_zero(x,y)
                            self.turn += 1
                            if single and not self.is_win():
                                time.sleep(0.5)
                                self.next_turn()
                                #time.sleep(0.5)
                            if self.is_win():
                                self.screen.fill(pygame.Color('white'))
                                text = f.render('WON!', True, (0,0,0))
                                self.screen.blit(text, (1.5*self.size, 1.5*self.size))
                                pygame.display.update()
                                [self.draw_zero, self.draw_cross][self.turn%2](1.2,0.2)
                                time.sleep(0.5)
                                pygame.display.flip()
                                running = False
                                break
                            if self.turn >= 9:
                                self.screen.fill(pygame.Color('white'))
                                text = f.render('DRAW', True, (0,0,0))
                                self.screen.blit(text, (1*self.size, 1*self.size))
                                pygame.display.update()
                                pygame.display.flip()
                                running = False

        text = pygame.font.Font(None, int(self.size // 3)).\
        render('press ENTER for restart', True, (0,0,0))
        self.screen.blit(text, (0.3*self.size, 2.3*self.size))
        pygame.display.update()
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    running = False
                    break
                if event.type == KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game()
                        running = False
                        break

    def game(self):
        self.screen.fill(pygame.Color('white'))
        f = pygame.font.Font(None, int(self.size // 3))
        text = f.render('Choose mode', True, (0,0,0))
        self.screen.blit(text, (0.8*self.size, 0.2*self.size))

        text_single = f.render('Single:', True, (0,0,0))
        self.screen.blit(text_single, (0.2*self.size, 0.8*self.size))

        text_multi = f.render('PvP:', True, (0,0,0))
        self.screen.blit(text_multi, (2*self.size, 0.8*self.size))
        pygame.display.update()

        self.draw_zero(1.4,1.9)
        self.draw_cross(1.2,1.7)

        self.draw_cross(1.3,0.1)

        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in [1,3]:
                        x,y=pygame.mouse.get_pos()
                        y,x=x/self.size, y/self.size
                        #print(f'x:{x}, y:{y}')
                        if (1.3<=x<=2.25 and 0.15<=y<=1.1):
                            self.run(single = True)
                            running = False
                            break
                        elif (1.2<=x<=2.25 and 1.7<=y<=2.9):
                            self.run(single = False)
                            running = False
                            break

if __name__ == "__main__":

    pygame.init()
    pygame.display.set_caption('Крестики нолики')
    a = Grid()
    a.game()
