from library.Sprites import Sprites
import pygame.freetype
from math import ceil
from library.constants import K, State


class Ground:
    def __init__(self, name, scale=4):
        self.name = name
        t = self.tile = Sprites(name, 1)

        self.Player = None                        # initialize with player when using this class

        self.__scale = scale
        g = self.array = self.generateGround(name, scale)
        n = self.arrayN = len(self.array)
        self.netWidth = t.w * n
        self.sprites = pygame.sprite.Group(*g)

        self.scroll = 0
        self.velocity = 0
        self.acceleration = 0
        self.__startRate = 0

        self.__isStart = False
        self.__isStop = False

        self.__startIterator = None
        self.__stopIterator = None

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, new):
        g = self.array = self.generateGround(self.name, new)
        N = self.arrayN = len(self.array)
        self.netWidth = self.tile.w * N
        self.sprites = pygame.sprite.Group(*g)

    def generateGround(self, name, scale=4):
        self.tile.scale(scale, True)

        w = int(self.tile.w)
        n = ceil(K.currentScreenSize[0] / w) + 1
        g = tuple([Sprites(name, 1) for _ in range(n)])
        for i, ground in enumerate(g):
            ground.scale(scale, True)
            ground.x = -self.tile.w + (self.tile.w * i)
            ground.y = K.currentScreenSize[1] - self.tile.h

        return g

    def start(self, maxSpeed, timeInSec):
        self.__startRate = maxSpeed * 2 / (timeInSec * K.fps) ** 2

        if -maxSpeed < self.velocity:
            self.__isStart = True
            self.__startIterator = self.__start(self.__startRate, int(timeInSec * K.fps))

    def stop(self):
        if not self.__isStop:
            self.__isStop = True
            self.__stopIterator = self.__stop()

    def update(self):
        self.scroll += int(self.velocity)

        if self.__isStart:
            try:
                next(self.__startIterator)
            except StopIteration:
                self.__isStart = False

        if self.__isStop:
            try:
                next(self.__stopIterator)
            except StopIteration:
                self.__isStop = False

        for g in self.array:
            g.updateDisplacementX(self.velocity)
            if g.x < -self.tile.w:
                g.updateDisplacementX(self.netWidth)

    def __start(self, rate, frames):
        self.Player.currentState = State.active

        for _ in range(frames):
            self.acceleration -= rate
            self.velocity += self.acceleration

            yield

        self.acceleration = 0

    def __stop(self):
        while self.Player.sprites[self.Player.currentState].currentFrame != 0:
            yield

        self.Player.currentState = State.slowDown

        while self.velocity < 0:
            self.acceleration += self.__startRate
            self.velocity += self.acceleration

            yield
        else:
            self.velocity = self.acceleration = 0

        self.Player.sprites[self.Player.currentState].currentFrame = 0
        self.Player.currentState = State.idle


class Player:
    # Constructor
    def __init__(self, sprites, ground, scale=1):
        self.currentState = State.idle

        self.groundY: int  # for jump handling
        self.velocity = 0
        self.acceleration = 0

        G = self.Ground = ground  # Ground underneath the Player
        G.Player = self

        self.sprites: dict[State, Sprites] = sprites

        self.score = pygame.freetype.Font(K.scoreFont, 30 * scale)

        self.s = scale
        self.scale = scale

        self.__isJump = False
        self.__jumpIterator = None

    # getters&setters + decorated properties
    @property
    def x(self):
        return self.sprites[self.currentState].x

    @x.setter
    def x(self, new):
        self.sprites[self.currentState].x = new

    @property
    def y(self):
        return self.sprites[self.currentState].y

    @y.setter
    def y(self, new):
        self.sprites[self.currentState].y = new

    @property
    def scale(self):
        return self.s

    @scale.setter
    def scale(self, new):
        self.s = new
        S = K.currentScreenSize

        self.score = pygame.freetype.Font(K.scoreFont, 30 * new)

        self.Ground.scale = 4
        groundH = self.Ground.tile.h

        x = int(S[0] * 0.10)
        y = self.groundY = S[1] - int(groundH * 0.8)
        for sprite in self.sprites.values():
            sprite.scale(new, True)
            sprite.setGlobalPosition(x, y)

    def jump(self):
        self.__isJump = True
        self.__jumpIterator = self.__jump(2000, 0.4)

    # methods
    def update(self):
        self.Ground.update()

        if self.__isJump:
            try:
                next(self.__jumpIterator)
            except StopIteration:
                self.__isJump = False

        y = self.y
        self.sprites[self.currentState].update(delay=2)
        self.y = y + int(self.velocity)

    def draw(self, screen):
        self.Ground.sprites.draw(screen)

        x = str(-int(self.Ground.scroll / 30))               # the score
        self.score.render_to(screen, (0, 0), x, K.white)     # score's corresponding font object
        sprite = self.sprites[self.currentState]
        sprite.draw(screen)

    # def disconnect(self, update):
    #     if self.currentState == State.active:
    #         self.Ground.stop(update)
    #
    #     while self.state[self.currentState].currentFrame != 1:
    #         c.tick(K.fps)
    #         update(self.id)
    #
    #     self.currentState = State.disconnected
    #     self.state[self.currentState].reverse = False
    #     self.state[self.currentState].dead = False
    #     self.state[self.currentState].currentFrame = 0
    #     update(self.id)
    #
    # def reconnect(self, update):
    #     self.state[self.currentState].reverse = True
    #     self.state[self.currentState].dead = False
    #
    #     while not self.state[self.currentState].dead:
    #         c.tick(K.fps)
    #         update(self.id)
    #
    #     self.currentState = State.idle
    #     self.state[self.currentState].currentFrame = 0
    #     update(self.id)
    def __setJumpHeight(self, height, time):
        self.acceleration = height / time / time
        self.velocity = - self.acceleration * time / 2

    def __jump(self, heightInPx, timeInSec):
        self.__setJumpHeight(heightInPx, timeInSec * K.fps)
        prevState = self.currentState
        self.currentState = State.jump
        self.sprites[State.jump].currentFrame = 4

        while True:
            self.velocity += self.acceleration

            yield

            if self.y > self.groundY:
                self.y = self.groundY
                self.velocity = 0
                self.acceleration = 0
                self.currentState = prevState
                self.sprites[State.jump].currentFrame = 0
                self.sprites[State.jump].delay = 0
                return


class Obstacle:
    def __init__(self, variations: list[Sprites]):
        self.variations = variations
        self.scaleRange = (1, 2)
