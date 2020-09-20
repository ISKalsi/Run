import pygame
from pygame.locals import *
import sys
from library.Elements import Ground, Player
from library.constants import K
from library.Sprites import Sprites

pointTo = Sprites.Offset

pygame.init()
clock = pygame.time.Clock()
d = pygame.display
SCREENSIZE = (d.Info().current_w, d.Info().current_h)
screen = d.set_mode((K.width, K.height))
fullscreen = False
d.set_caption("RUN")

G = Ground("ground")
P = Player("stickman_still", x=250, y=420, offset=(0.5, 0.80))


def update():
    screen.fill(K.white)
    G.update()
    P.update()
    G.sprites.draw(screen)
    P.draw(screen)
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

            if keys[K_SPACE]:
                G.start(update, 5)
            elif keys[K_x]:
                G.stop(update)
            elif keys[K_j]:
                P.jump(update)

    update()
