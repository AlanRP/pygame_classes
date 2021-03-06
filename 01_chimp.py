import pygame
import sys
import os
from pygame.locals import *

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

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


def loadSound(name):
    class NoneSound:
        def play(self):
            pass
    if not pygame.mixer:
        return NoneSound()
    fullName = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullName)
    except pygame.error:
        print('Cannot load sound:', fullName)
        raise SystemExit(str(geterror()))
    return sound

class Fist(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # call Sprite initializer
        self.image, self.rect = loadImage('fist.bmp', -1)
        self.punching = 0

    def update(self):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move(5, 10)
    
    def punch(self, target):
        "returns true if the fist collides with the target"
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        "called to pull the fist back"
        self.punching = 0


class Chimp(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the 
    monkey when it is punched."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = loadImage('chimp.bmp', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0

    def update(self):
        "walk on spin, depending on the monkeys state"
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        "move the monkey across the screen, and turn at the ends"
        newpos = self.rect.move((self.move, 0))
        if self.rect.left < self.area.left or \
            self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect = newpos

    def _spin(self):
        "spin the monkey image"
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


def main():
    pygame.init()

    screen = pygame.display.set_mode((468, 60))
    pygame.display.set_caption('Monkey Fever')
    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        background.blit(text, textpos)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    whiff_sound = loadSound('whiff.wav')
    punch_sound = loadSound('punch.wav')
    chimp = Chimp()
    fist = Fist()
    allsprites = pygame.sprite.RenderPlain((fist, chimp))
    clock = pygame.time.Clock()

    while 1:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()  #punch
                    chimp.punched()
                else:
                    whiff_sound.play()  #miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()

