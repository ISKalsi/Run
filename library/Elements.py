from library.Sprites import Sprites
import pygame
from math import ceil
from pygame.locals import *
import sys

d = pygame.display


def isQuit():
    if pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    if pygame.event.get(KEYDOWN):
        if pygame.key.get_pressed()[K_ESCAPE]:
            pygame.quit()
            sys.exit()


class Ground:
    def __init__(self, name, scale=4):
        self.name = name
        self.tile = Sprites(name, 1)
        self.groundW = int(self.tile.rect.w * 0.8)
        self.scale = scale
        g = self.array = self.generateGround(name, scale)
        self.sprites = pygame.sprite.Group(g)
        self.scroll = 0

    @property
    def scale(self):
        pass

    @scale.setter
    def scale(self, new):
        self.tile.scale(new, True)
        self.groundW = int(self.tile.rect.w * 0.8)
        g = self.array = self.generateGround(self.name, new)
        self.sprites = pygame.sprite.Group([tile for tile in g])

    def generateGround(self, name, scale=4):
        self.tile.scale(scale, True)
        n = ceil(d.Info().current_w / self.groundW) + 1
        print(d.Info().current_w)
        g = tuple([Sprites(name, 1) for _ in range(n)])
        [g[i].scale(scale, True) for i in range(len(g))]
        return g

    def update(self, xOffset=0):
        g = self.array
        t = self.tile.rect
        w = self.groundW
        initialOffset = w * 0.3
        for i in range(len(g)):
            x = -initialOffset + w * i
            g[i].update(x + xOffset, d.Info().current_h - t.h)

    def scrollBG(self, update, left):
        x = -1 if left else 1
        pressed = True
        momentum = 0
        while pressed:
            isQuit()

            self.scroll += int(x * momentum)
            momentum += 0.2

            update(self.scroll)

            if pygame.event.get(KEYUP):
                pressed = False

        while momentum > 0:
            isQuit()

            momentum -= 0.5
            self.scroll += int(x * momentum)

            update(self.scroll)
