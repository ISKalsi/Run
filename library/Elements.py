from library.Sprites import Sprites
import pygame
import pygame.freetype
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
        print(d.Info().current_h)
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


class Player:
    class State:
        idle = "idle"
        active = "run"
        jump = "jump"
        slash = "slash"

    def __init__(self, states, ground, x=0, y=0, scale=4):
        s = self.state = states
        self.currentState = Player.State.idle

        for state in s.values():
            state.rect.x = x
            state.rect.y = y

        self.groundY = y     # for jump handling
        self.momentum = 0

        self.scale = scale

        self.score = pygame.freetype.Font(K.scoreFont, 30*scale)
        self.Ground = ground            # Ground underneath the Player

    @property
    def x(self):
        return self.state[self.currentState].x

    @x.setter
    def x(self, new):
        self.state[self.currentState].x = new

    @property
    def y(self):
        return self.state[self.currentState].y

    @y.setter
    def y(self, new):
        self.state[self.currentState].y = new

    @property
    def scale(self):
        pass

    @scale.setter
    def scale(self, new):
        self.score = pygame.freetype.Font(K.scoreFont, 30 * new)
        for sprite in self.state.values():
            sprite.scale(new, True)

    def changeState(self, state):
        self.currentState = state

    def update(self):
        self.y -= int(self.momentum)
        self.state[self.currentState].update(self.x, self.y, delay=3)

    def draw(self, screen):
        x = str(-int(self.Ground.scroll / 30))               # the score
        self.score.render_to(screen, (0, 0), x, K.white)     # score's corresponding font object
        sprite = self.state[self.currentState]
        screen.blit(sprite.image, sprite.rect)

    def jump(self, update):
        self.momentum = 30
        s = Player.State
        self.currentState = s.jump
        self.state[s.jump].currentFrame = 4

        while True:
            c.tick(K.fps)
            self.momentum -= 2
            update()
            if self.y >= self.groundY:
                self.y = self.groundY
                self.momentum = 0
                self.currentState = s.idle
                self.state[s.jump].currentFrame = 0
                self.state[s.jump].delay = 0
                update()
                break
