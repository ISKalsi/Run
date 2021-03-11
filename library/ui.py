import pygame
from enum import Enum, auto
from library.Sprites import Sprites
from library.constants import K

display = pygame.display
clock = pygame.time.Clock()


def __initEnumStates__(size: int):
    return (auto() for _ in range(size))


class Button:
    class Type(Enum):
        IMAGE, SPRITE, NORMAL = __initEnumStates__(3)

    class State(Enum):
        DOWN, HOVER, UP = __initEnumStates__(3)

    def __init__(self):
        pass


class Menu:
    pass


class Background:
    def __init__(self, layers: tuple[str, ...], speedRange: tuple[int, int], transitionTime=1.3):
        self.__layersN = layersN = len(layers)
        self.__speedRange = speedRange

        ratio = (speedRange[1] - speedRange[0]) / (layersN-1)
        self.__maxVelocity = [(ratio * i) + 2 for i in range(layersN - 1)]
        self.__maxVelocity.insert(0, 0)
        self.__velocity = [0 for _ in range(layersN)]
        self.__transitionTime = transitionTime
        self.__acceleration = self.__getAcceleration(transitionTime)

        self.__arrayLayers = [
            [Sprites(layers[i], 1, path="background") for _ in range(3)] for i in range(layersN)
        ]
        self.__sprites = pygame.sprite.Group(*self.__arrayLayers)
        self.__resetLayerAxisX()

        self.__isStart = False
        self.__isStop = False

        self.__startIterator = None
        self.__stopIterator = None

        self.scaleToFitHeight()

    def __resetLayerAxisX(self, index=None):
        if index is None:
            for layer in self.__arrayLayers:
                for i in range(3):
                    layer[i].x = layer[i].w * i
        else:
            for i in range(3):
                self.__arrayLayers[index][i].x = self.__arrayLayers[index][i].w * i

    def __getAcceleration(self, time):
        v = self.__maxVelocity
        u = self.__velocity
        t = time * K.fps
        return [(v[i]-u[i]) / t for i in range(self.__layersN)]

    def scaleToFitHeight(self):
        percent = (K.currentScreenSize[1] / self.__arrayLayers[0][0].originalHeight) * 100
        self.scale(percent)
    
    def scale(self, percent):
        for layer in self.__arrayLayers:
            for sprite in layer:
                sprite.scale(percent/100, True)

        self.__resetLayerAxisX()

    def start(self):
        self.__isStart = True
        self.__startIterator = self.__start()

    def stop(self):
        self.__isStop = True
        self.__stopIterator = self.__stop()

    def update(self):
        for i, layer in enumerate(self.__arrayLayers):
            for sprite in layer:
                sprite.updateDisplacementX(self.__velocity[i])

            if layer[1].x <= 0:
                self.__resetLayerAxisX(i)

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

    def draw(self, screen):
        self.__sprites.draw(screen)

    def __start(self):
        while self.__velocity[-1] > -self.__maxVelocity[-1]:
            for i in range(self.__layersN):
                self.__velocity[i] -= self.__acceleration[i]

            yield

    def __stop(self):
        while self.__velocity[-1] < 0:
            for i in range(self.__layersN):
                self.__velocity[i] += self.__acceleration[i]

            yield
        else:
            for i in range(self.__layersN):
                self.__velocity[i] = 0
