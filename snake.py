import pygame
import random

from pygame.locals import *

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = 0, 155, 0
bg = (206, 212, 218)

size = s_with, s_height = 800, 600

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')


clock = pygame.time.Clock()

block_size = 20
FPS = 15


def snake(snakelist):
    for X, Y in snakelist:
        pygame.draw.rect(
            screen, green, [X, Y, block_size, block_size])


def messageToScreen(msg, color):
    screen.fill(bg)
    font = pygame.font.SysFont(None, 36)
    text = font.render(msg, True, color)
    textpos = text.get_rect()
    textpos.center = screen.get_rect().center
    screen.blit(text, textpos)
    pygame.display.update()


def lead(key):
    if key == K_LEFT:
        return -block_size, 0
    if key == K_RIGHT:
        return block_size, 0
    if key == K_UP:
        return 0, -block_size
    if key == K_DOWN:
        return 0, block_size
    return 0, 0


def gameLoop():
    gameExit, gameOver = False, False
    lead_x, lead_y = s_with / 2, s_height / 2
    lead_change = 0, 0

    snakeList = []
    snakeLen = 1

    randAppleX = random.randrange(0, s_with - block_size, step=block_size)
    randAppleY = random.randrange(0, s_height - block_size, step=block_size)

    while not gameExit:
        while gameOver:
            messageToScreen('Game over! Press "ESC" to Quit', red)
            for event in pygame.event.get():
                if event.type == QUIT:
                    gameExit, gameOver = True, False
                if event.type == KEYDOWN:
                    if event.key != K_ESCAPE:
                        gameExit, gameOver = False, False
                        lead_x, lead_y = s_with / 2, s_height / 2
                        lead_change = 0, 0
                        randAppleX = random.randrange(
                            0, s_with - block_size, step=block_size)
                        randAppleY = random.randrange(
                            0, s_height - block_size, step=block_size)
                    else:
                        gameExit, gameOver = True, False

        for event in pygame.event.get():
            if event.type == QUIT:
                gameExit = True
            if event.type == KEYDOWN:
                if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                    lead_change = lead(event.key)

        lead_x += lead_change[0]
        lead_y += lead_change[1]

        if lead_x < 0 or lead_x > s_with or \
                lead_y < 0 or lead_y > s_height:
            gameOver = True

        screen.fill(bg)
        pygame.draw.rect(
            screen, red, [randAppleX, randAppleY, block_size, block_size])

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLen:
            del snakeList[0]
        snake(snakeList)

        pygame.display.update()

        if lead_x == randAppleX and lead_y == randAppleY:
            randAppleX = random.randrange(
                0, s_with - block_size, step=block_size)
            randAppleY = random.randrange(
                0, s_height - block_size, step=block_size)

        clock.tick(FPS)

    pygame.quit()
    quit()


if __name__ == '__main__':
    gameLoop()
