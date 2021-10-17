import pygame
import os
from pygame.locals import *
import time

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

bg = 27, 64, 34


class Snake:

    def __init__(self, parentScreen):
        self.parentScreen = parentScreen
        fullName = os.path.join(data_dir, 'block.jpg')
        self.block = pygame.image.load(fullName).convert()
        self.x = 100
        self.y = 100
        self.direction = K_DOWN

    def draw(self):
        self.parentScreen.fill(bg)
        self.parentScreen.blit(self.block, (self.x, self.y))
        pygame.display.flip()

    def moveLeft(self):
        self.direction = K_LEFT

    def moveRight(self):
        self.direction = K_RIGHT

    def moveUp(self):
        self.direction = K_UP

    def moveDown(self):
        self.direction = K_DOWN

    def walk(self):
        if self.direction == K_LEFT:
            self.x -= 10
            self.draw()
        elif self.direction == K_RIGHT:
            self.x += 10
            self.draw()
        elif self.direction == K_UP:
            self.y -= 10
            self.draw()
        elif self.direction == K_DOWN:
            self.y += 10
            self.draw()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((500, 500))
        self.surface.fill(bg)
        self.snake = Snake(self.surface)
        self.snake.draw()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                        self.snake.direction = event.key

                elif event.type == QUIT:
                    running = False
            time.sleep(0.2)
            self.snake.walk()


if __name__ == '__main__':
    game = Game()
    game.run()
