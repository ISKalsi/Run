import json
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

        self.once = False
        f = self.currentFrame = 0
        self.image = self.images[f]
        self.rect = self.cells[f]

    def _getImage(self, rect):
        image = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA, 32)
        image = image.convert_alpha()
        image.blit(self._sheet, (0, 0), rect)
        return image


class Sprites(pygame.sprite.Sprite, SpriteSheet):
    def __init__(self, name, frames=0, path=""):
        pygame.sprite.Sprite.__init__(self)
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

            self.once = False
            f = self.currentFrame = 0
            self.image = self.images[f]
            self.rect: pygame.Rect = self.cells[f]
            self.originalWidth = self.rect.w
            self.originalHeight = self.rect.h
        self.delay = 0
        self.dead = False

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

    def update(self, x=0, y=0, once=False, delay=0):
        if self.dead:
            f = self.currentFrame = 12
        else:
            if self.delay:
                self.once = once
                self.delay -= 1
                return

            self.delay = delay
            self.once = once
            f = self.currentFrame = (self.currentFrame + 1) % self.frames

            if once and f == 0:
                self.once = False

        self.image = self.images[f]
        self.rect = self.cells[f]
        self.rect.x = x
        self.rect.y = y
