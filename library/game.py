import pygame
from pygame.locals import *
import sys
from library.Elements import Ground
from library.constants import K

pygame.init()
clock = pygame.time.Clock()
d = pygame.display
SCREENSIZE = (d.Info().current_w, d.Info().current_h)
screen = d.set_mode((K.width, K.height))
fullscreen = False
d.set_caption("RUN")

G = Ground("ground")


def update(xOffset=0):
    screen.fill(K.black)
    G.update(xOffset)
    G.sprites.draw(screen)
    d.update()


while True:
    clock.tick(K.fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if keys[K_LCTRL] and keys[K_f] and keys[K_LSUPER]:
                fullscreen = not fullscreen
                screen = d.set_mode(SCREENSIZE, FULLSCREEN) if fullscreen else d.set_mode((K.width, K.height))
                G.scale = 6 if fullscreen else 4
                continue

            if keys[K_RIGHT]:
                G.scrollBG(update, False)

            if keys[K_LEFT]:
                G.scrollBG(update, True)

    update(G.scroll)
