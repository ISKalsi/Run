from library.Sprites import Sprites
import pygame
import pygame.freetype
from math import ceil
from library.constants import K, State
from library.client import Client

d = pygame.display
c = pygame.time.Clock()


class Ground:
    totalGrounds = 0

    def __init__(self, name, scale=4):
        self.name = name
        self.tile = Sprites(name, 1)

        self.Player = None                        # initialize with player when using this class

        Ground.totalGrounds += 1
        i = self.ID = Ground.totalGrounds - 1

        self.groundW = int(self.tile.rect.w * 0.8)
        self.baseY = - int(self.tile.rect.h * i)

        self.s = scale
        g = self.array = self.generateGround(name, scale)
        self.sprites = pygame.sprite.Group(*g)

        self.scroll = 0
        self.momentum = 0

    @property
    def scale(self):
        return self.s

    @scale.setter
    def scale(self, new):
        g = self.array = self.generateGround(self.name, new)
        self.sprites = pygame.sprite.Group(*g)

    @property
    def id(self):
        return self.ID

    @id.setter
    def id(self, new):
        self.ID = new
        self.baseY = - int(self.tile.rect.h * new)

    def generateGround(self, name, scale=4):
        self.tile.scale(scale, True)

        gw = self.groundW = int(self.tile.rect.w * 0.8)
        self.baseY = - int(self.tile.rect.h * 0.9 * self.id)

        n = ceil(d.Info().current_w / gw) + 2
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
            g[i].update(initialOffset + (gw * i + self.scroll) % w, h - t.h + self.baseY)

    def start(self, update, cap):
        self.Player.currentState = State.active

        while True:
            c.tick(K.fps)

            self.momentum -= 0.1
            update(self.ID)

            if self.momentum <= -cap:
                break

    def stop(self, update):
        while self.Player.state[self.Player.currentState].currentFrame != 0:
            c.tick(K.fps)

            update(self.ID)

        self.Player.currentState = State.slowDown

        while self.momentum < 0:
            c.tick(K.fps)

            self.momentum += 0.1
            update(self.ID)

        self.Player.state[self.Player.currentState].currentFrame = 0
        self.Player.currentState = State.idle


class Player(Client):
    # Constructor
    def __init__(self, states, ground, screen=(0, 0), scale=1, clientList=None, ID=None):
        Client.__init__(self, self, clientList, ID)

        while self.id is None:
            pass

        self.groundY: int  # for jump handling
        self.momentum = 0

        G = self.Ground = ground  # Ground underneath the Player
        G.Player = self
        G.id = self.id

        self.state = states

        self.score = pygame.freetype.Font(K.scoreFont, 30 * scale)
        self.scoreX = screen[0]/4 * self.id

        self.s = self.scale = scale

    # getters&setters + decorated properties
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
        return self.s

    @scale.setter
    def scale(self, new):
        self.s = new
        S = (d.Info().current_w, d.Info().current_h)

        self.score = pygame.freetype.Font(K.scoreFont, 30 * new)
        self.scoreX = S[0] / 4 * self.id

        self.Ground.scale = 4
        baseY = self.Ground.baseY
        groundH = self.Ground.tile.h

        x = int(S[0] * 0.10 * (self.id+1))
        y = self.groundY = S[1] - int(groundH * 0.8) + baseY
        for sprite in self.state.values():
            sprite.scale(new, True)
            sprite.x = x
            sprite.y = y

    # methods
    def update(self):
        self.Ground.update()

        self.y -= int(self.momentum)
        self.state[self.currentState].update(self.x, self.y, delay=3)

    def draw(self, screen, score=None):
        self.Ground.sprites.draw(screen)

        x = str(-int((score if score else self.Ground.scroll) / 30))               # the score
        self.score.render_to(screen, (self.scoreX, 0), x, K.white)     # score's corresponding font object
        sprite = self.state[self.currentState]
        screen.blit(sprite.image, sprite.rect)

    def disconnect(self, update):
        if self.currentState == State.active:
            self.Ground.stop(update)

        while self.state[self.currentState].currentFrame != 1:
            c.tick(K.fps)
            update(self.id)

        self.currentState = State.disconnected
        self.state[self.currentState].reverse = False
        self.state[self.currentState].dead = False
        self.state[self.currentState].currentFrame = 0
        update(self.id)

    def reconnect(self, update):
        self.state[self.currentState].reverse = True
        self.state[self.currentState].dead = False

        while not self.state[self.currentState].dead:
            c.tick(K.fps)
            update(self.id)

        self.currentState = State.idle
        self.state[self.currentState].currentFrame = 0
        update(self.id)

    def jump(self, update):
        self.momentum = 30
        prevState = self.currentState
        self.currentState = State.jump
        self.state[State.jump].currentFrame = 4

        while True:
            c.tick(K.fps)
            self.momentum -= 2
            update(self.id)
            if self.y >= self.groundY:
                self.y = self.groundY
                self.momentum = 0
                self.currentState = prevState
                self.state[State.jump].currentFrame = 0
                self.state[State.jump].delay = 0
                update(self.id)
                break
