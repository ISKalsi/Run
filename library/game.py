import pygame
import pygame.freetype
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

playerOffset = (0.5, 0.87)
players = []

for _ in range(4):
    states = {
        Player.State.active: Sprites("running animation", 13, offset=playerOffset),
        Player.State.jump: Sprites("jump", 14, offset=playerOffset),
        Player.State.idle: Sprites("idle", 16, offset=playerOffset)
    }

    P = Player(states, Ground("ground"), screen=(K.width, K.height), scale=2)
    players.append(P)

N = len(players)


def toggleFullscreen():
    global fullscreen, screen

    fullscreen = not fullscreen
    screen = d.set_mode(SCREENSIZE, FULLSCREEN) if fullscreen else d.set_mode((K.width, K.height))

    scale = 3 if fullscreen else 2
    for player in players:
        player.scale = scale


def gameLoop():
    def update():
        screen.fill(K.black)
        for i in range(N):
            players[N-i-1].update()
            players[N-i-1].draw(screen)
        d.flip()

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
                    toggleFullscreen()
                    continue

                if keys[K_SPACE]:
                    players[0].Ground.start(update, 5)
                elif keys[K_x]:
                    players[0].Ground.stop(update)
                elif keys[K_j]:
                    players[0].jump(update)

        update()


gameLoop()
