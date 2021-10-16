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

gameExit = False

lead_x = s_with / 2
lead_y = s_height / 2
lead_x_change = 0
lead_y_change = 0

clock = pygame.time.Clock()

block_size = 10
FPS = 30

while not gameExit:
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
        gameExit = True

    lead_x += lead_x_change
    lead_y += lead_y_change
    screen.fill(bg)
    pygame.draw.rect(screen, black, [lead_x, lead_y, block_size, block_size])

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
quit()
