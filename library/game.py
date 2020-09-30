import pygame
import pygame.freetype
from pygame.locals import *
import sys
from library.Elements import Ground, Player
from library.constants import K
from library.Sprites import Sprites
from library.client import Client
pointTo = Sprites.Offset

pygame.init()
clock = pygame.time.Clock()
d = pygame.display
SCREENSIZE = (d.Info().current_w, d.Info().current_h)
screen = d.set_mode((K.width, K.height))
fullscreen = False
d.set_caption("RUN")

playerOffset = (0.5, 0.87)
players = {}
N = 0


def generateStates():
    states = {
        Player.State.active: Sprites("running animation", 13, offset=playerOffset),
        Player.State.jump: Sprites("jump", 14, offset=playerOffset),
        Player.State.idle: Sprites("idle", 16, offset=playerOffset)
    }

    return states


def addPlayer(c=None):
    global N

    if c is not None:
        for i in range(c["count"]):
            print(N, c["count"])
            print(c[f'{i}'])
            if i in players:
                continue

            P = Player(generateStates(), Ground("ground"), screen=(K.width, K.height), scale=2, clientList=c, ID=i)
            players[i] = P
            N += 1
    else:
        P = Player(generateStates(), Ground("ground"), screen=(K.width, K.height), scale=2)
        print(P.id)
        players[P.id] = P
        N += 1
        return P.id


def toggleFullscreen():
    global fullscreen, screen

    fullscreen = not fullscreen
    screen = d.set_mode(SCREENSIZE, FULLSCREEN) if fullscreen else d.set_mode((K.width, K.height))

    scale = 3 if fullscreen else 2
    for player in players:
        player.scale = scale


def gameLoop():
    def update():
        c = Client.clientList
        screen.fill(K.black)
        if c["count"] != N:
            addPlayer(c)

        for i in range(c["count"]):
            if i != x:
                setattr(players[i], "current", c[f'{i}'][1])

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
                    players[x].Ground.start(update, 5)
                elif keys[K_x]:
                    players[x].Ground.stop(update)
                elif keys[K_j]:
                    players[x].jump(update)

        update()


x = addPlayer()
gameLoop()
