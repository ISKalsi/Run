import json
from pygame.draw_py import floor
from pathlib import Path
import pygame


class SpriteSheet:
    def __init__(self, name, path=""):
        self.mediaPath = Path(__file__).resolve().parent / '../media' / path

        self._sheet = pygame.image.load(f'{self.mediaPath}/{name}/{name}.png').convert_alpha()
        self._metaData = json.load(open(f'{self.mediaPath}/{name}/{name}.json'))

        size = self._metaData["meta"]["size"]
        w = self._sheetWidth = size['w']
        h = self._sheetHeight = size['h']
        self.frames = w // h

        self.cells = []
        for i in range(self.frames):
            frame = self._metaData["frames"][f'{i}.']["frame"]
            self.cells.append(pygame.rect.Rect((frame['x'], frame['y']), (frame['w'], frame['h'])))

        self.images = []
        for i in range(self.frames):
            self.images.append(self._getImage(self.cells[i]))

        f = self.currentFrame = 0
        self.image = self.images[f]
        self.rect = self.cells[f]

    def _getImage(self, rect):
        image = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA, 32)
        image = image.convert_alpha()
        image.blit(self._sheet, (0, 0), rect)
        return image


class Sprites(pygame.sprite.Sprite, SpriteSheet):
    class Offset:
        center, \
            topLeft, topMid, topRight, \
            midLeft, midRight, \
            bottomLeft, bottomMid, bottomRight = range(9)

    def __init__(self, name, frames=0, path="", offset=Offset.topLeft, once=False, reverse=False):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        if frames == 0:
            SpriteSheet.__init__(self, name, path)
        else:
            self.mediaPath = Path(__file__).resolve().parent / '../media' / path

            self.frames = frames
            if frames != 1:
                self.images = list(
                    [pygame.image.load(f'{self.mediaPath}/{name}/{name}{i + 1}.png').convert_alpha() for i in
                     range(frames)]
                )
            else:
                self.images = [pygame.image.load(f'{self.mediaPath}/{name}/{name}.png').convert_alpha()]

            self.cells = list(
                [self.images[i].get_rect() for i in range(frames)]
            )

            f = self.currentFrame = 0
            self.image = self.images[f]
            self.rect: pygame.Rect = self.cells[f]

        self.originalWidth = self.rect.w
        self.originalHeight = self.rect.h
        self.delay = 0
        self.once = once
        self.dead = False
        self.reverse = reverse
        self.offset = offset
        self.offsetX = self.offsetY = 0
        self.pointTo(offset)

    def __repr__(self):
        return f"<{self.name}: {self.x}, {self.y}>"

    @property
    def x(self):
        return self.rect.x - self.offsetX

    @x.setter
    def x(self, new):
        self.rect.x = new + self.offsetX

    @property
    def y(self):
        return self.rect.y - self.offsetY

    @y.setter
    def y(self, new):
        self.rect.y = new + self.offsetY

    @property
    def w(self):
        return self.rect.w

    @property
    def h(self):
        return self.rect.h

    def pointTo(self, offset):
        w = self.rect.w
        h = self.rect.h
        x = y = 0
        pointTo = Sprites.Offset
        self.offset = offset
        if offset == pointTo.topMid:
            x = w // 2
        elif offset == pointTo.topRight:
            x = w
        elif offset == pointTo.midLeft:
            y = h // 2
        elif offset == pointTo.center:
            x = w // 2
            y = h // 2
        elif offset == pointTo.midRight:
            y = h // 2
            x = w
        elif offset == pointTo.bottomLeft:
            y = h
        elif offset == pointTo.bottomMid:
            y = h
            x = w // 2
        elif offset == pointTo.bottomRight:
            x = w
            y = h

        # for manual offset:
        # enter value between 0 and 1 for each X and Y as tuple
        # That value will be the ratio of offset distance with width/height
        # Eg:- bottomMid as a manual offset will look like (0.5, 1)
        elif type(offset) is tuple:
            x = int(w * offset[0])
            y = int(h * offset[1])

        a = self.offsetX = -x
        b = self.offsetY = -y
        self.rect.x += a
        self.rect.y += b

    def scale(self, n=4, fromOriginal=False):
        if fromOriginal:
            for i in range(self.frames):
                self.cells[i].w = self.originalWidth * n
                self.cells[i].h = self.originalHeight * n
        else:
            for i in range(self.frames):
                self.cells[i].w *= n
                self.cells[i].h *= n

        for i in range(self.frames):
            self.images[i] = pygame.transform.scale(self.images[i], (self.cells[i].w, self.cells[i].h))

        self.image = self.images[self.currentFrame]
        self.rect = self.cells[self.currentFrame]
        self.pointTo(self.offset)

    def update(self, delay=0):
        if self.dead:
            pass
        else:
            if self.delay:
                self.delay -= 1
                return

            self.delay = delay
            f = self.currentFrame = (self.currentFrame + (-1 if self.reverse else 1)) % self.frames

            if self.once and f == self.frames - 1:
                self.dead = True

        self.image = self.images[self.currentFrame]
        self.rect = self.cells[self.currentFrame]

    def setGlobalPosition(self, x, y):
        for i in range(self.frames):
            self.cells[i].x = x + self.offsetX
            self.cells[i].y = y + self.offsetY

    def updatePosition(self, x, y):
        self.x = floor(x)
        self.y = floor(y)

    def updatePositionX(self, x):
        self.x = floor(x)

    def updatePositionY(self, y):
        self.y = floor(y)

    def updateDisplacement(self, dx, dy):
        self.x = floor(self.x + dx)
        self.y = floor(self.y + dy)

    def updateDisplacementX(self, dx):
        self.x = floor(self.x + dx)

    def updateDisplacementY(self, dy):
        self.y = floor(self.y + dy)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
