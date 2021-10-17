import pygame

from pygame.locals import *

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
bg = (206, 212, 218)

size = s_with, s_height = 800, 600

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')


clock = pygame.time.Clock()

block_size = 10
FPS = 30


def messageToScreen(msg, color):
    font = pygame.font.SysFont(None, 36)
    text = font.render(msg, True, color)
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    textpos.centery = screen.get_rect().centery
    screen.blit(text, textpos)
    pygame.display.update()


def gameLoop():
    gameExit = False
    gameOver = False

    lead_x = s_with / 2
    lead_y = s_height / 2
    lead_x_change = 0
    lead_y_change = 0
    while not gameExit:

        while gameOver:
            screen.fill(bg)
            messageToScreen('Game over! Press "ESC" to Quit', red)
            for event in pygame.event.get():
                if event.type == QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == KEYDOWN:
                    if event.key != K_ESCAPE:
                        gameLoop()
                    else:
                        gameExit = True
                        gameOver = False

        for event in pygame.event.get():
            if event.type == QUIT:
                gameExit = True
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
        if lead_x <= 0 or lead_x >= s_with or \
                lead_y <= 0 or lead_y >= s_height:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change
        screen.fill(bg)
        pygame.draw.rect(
            screen, black, [lead_x, lead_y, block_size, block_size])

        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
    quit()


if __name__ == '__main__':
    gameLoop()
