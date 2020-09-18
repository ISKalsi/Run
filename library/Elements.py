from library.Sprites import Sprites
import pygame
from pygame.locals import *
from math import ceil
import sys
from library.constants import K

d = pygame.display
c = pygame.time.Clock()


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
        self.momentum = 0

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
        gw = self.groundW = int(self.tile.rect.w * 0.8)
        n = ceil(d.Info().current_w / gw) + 2
        print(d.Info().current_w)
        g = tuple([Sprites(name, 1) for _ in range(n)])
        [g[i].scale(scale, True) for i in range(len(g))]
        return g

    def update(self):
        self.scroll += int(self.momentum)

        g = self.array
        t = self.tile.rect
        gw = self.groundW
        h = d.Info().current_h
        initialOffset = -t.w
        w = (len(g)) * gw
        for i in range(len(g)):
            g[i].update(initialOffset + (gw * i + self.scroll) % w, h - t.h)

    def start(self, update, cap):
        while True:
            c.tick(K.fps)
            isQuit()

            self.momentum -= 0.1
            update()

            if self.momentum <= -cap:
                break

    def stop(self, update):
        while self.momentum < 0:
            c.tick(K.fps)
            isQuit()

            self.momentum += 0.1
            update()
