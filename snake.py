import pygame
import os
from pygame.locals import *
import random

BG = 27, 64, 34
FPS = 6
BLK_SIZE = 30
WINDOW_SIZE = W_WIDTH, W_HEIGTH = 720, 540
DIRECTION = {
    K_LEFT: [-BLK_SIZE, 0], K_RIGHT: [BLK_SIZE, 0],
    K_UP: [0, -BLK_SIZE], K_DOWN: [0, BLK_SIZE],
}


def loadImage(name, colorKey=None):
    fullName = os.path.join('data', name)
    try:
        image = pygame.image.load(fullName)
    except pygame.error:
        print('Cannot load image:', name)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorKey is not None:
        if colorKey is -1:
            colorKey = image.get_at((0, 0))
        image.set_colorkey(colorKey, RLEACCEL)
    return image, image.get_rect()


class Apple:
    def __init__(self, parentScreen):
        self.apple, rect = loadImage('apple.png', -1)
        self.apple = pygame.transform.scale(
            self.apple, (BLK_SIZE, BLK_SIZE))
        self.parentScreen = parentScreen
        self.pos = [0, 0]

    def draw(self):
        self.parentScreen.blit(self.apple, self.pos)
        pygame.display.flip()

    def move(self, xyException):

        while True:
            x = random.randrange(0, W_WIDTH - BLK_SIZE, step=BLK_SIZE)
            y = random.randrange(0, W_HEIGTH - BLK_SIZE, step=BLK_SIZE)
            self.pos = [x, y]
            if self.pos not in xyException:
                break
        self.draw()


class Snake:
    def __init__(self, parentScreen, length):
        self.length = length
        self.parentScreen = parentScreen
        self.color = [6, 155, 0]

        self.block, rect = loadImage('block.jpg', -1)
        self.block = pygame.transform.scale(self.block, (BLK_SIZE, BLK_SIZE))

        self.xy = [[BLK_SIZE, BLK_SIZE]]*length
        self.direction = K_DOWN

    def increaseLength(self):
        self.length += 1
        self.xy.append([-1, -1])

    def draw(self):
        self.parentScreen.fill(BG)
        for i, [x, y] in enumerate(self.xy):
            j = i if i < 25 else 25
            q = j*j
            _color = -q + 28*j + 50, int(-0.1*q + 240), int(0.3 * q)
            # print(_color)
            pygame.draw.rect(
                self.parentScreen, _color, [x + 1, y + 1, BLK_SIZE - 2, BLK_SIZE - 2])

    def walk(self):
        self.xy[1:] = self.xy[:-1]

        self.xy[0] = self.sumPos(self.xy[0], DIRECTION[self.direction])

        self.draw()

    def sumPos(self, pos: list([0, 0]), value: list([0, 0])):
        return [pos[0] + value[0], pos[1] + value[1]]


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(WINDOW_SIZE)
        self.snake = Snake(self.surface, 30)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.move(self.snake.xy)
        self.pause = False
        self.gameOver = False
        self.clock = pygame.time.Clock()

    def play(self):
        self.snake.walk()
        self.displayScore()
        self.snacking()

        if self.isOver():
            self.pause = True
            self.gameOver = True
            self.showGameOver()

        pygame.display.flip()

    def isOver(self):
        snk = self.snake
        for i in range(1, self.snake.length):
            if snk.xy[0][0] == snk.xy[i][0] and snk.xy[0][1] == snk.xy[i][1]:
                return True
        if snk.xy[0][0] < 0 or snk.xy[0][0] >= W_WIDTH or \
                snk.xy[0][1] < 0 or snk.xy[0][1] >= W_HEIGTH:
            return True
        return False

    def snacking(self):
        if self.snake.xy[0] == self.apple.pos:
            self.snake.increaseLength()
            self.apple.move(self.snake.xy)
        else:
            self.apple.draw()

    def showGameOver(self):
        # self.surface.fill(BG)
        font = pygame.font.SysFont(None, 30)
        line1 = font.render(
            f'Game is Over! You score is {self.snake.length}', True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(
            f'To play again, press Enter. To exit press Escape!', True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    def displayScore(self):
        font = pygame.font.SysFont(None, 30)
        score = font.render(
            f'Score: {self.snake.length}', True, (255, 255, 255))
        self.surface.blit(score, (400, 10))

    def reset(self):
        self.pause = False
        self.gameOver = False
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_RETURN and self.gameOver:
                        self.reset()
                    elif event.key == K_SPACE and not self.gameOver:
                        self.pause = not self.pause

                    elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                        self.snake.direction = event.key

                elif event.type == QUIT:
                    running = False
            if not self.pause:
                self.play()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
