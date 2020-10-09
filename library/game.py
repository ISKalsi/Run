import pygame
import pygame.freetype
from pygame.locals import *
import sys
from library.Elements import Ground, Player
from library.constants import K, State
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
        State.active: Sprites("running animation", 13, offset=playerOffset),
        State.jump: Sprites("jump", 14, offset=playerOffset),
        State.idle: Sprites("idle", 16, offset=playerOffset),
        State.slowDown: Sprites("run to stop", 13, offset=playerOffset)
    }

    return states


def addPlayer(c=None):
    global N

    if c:
        for i in c["id"]:
            if i == x:
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


def delPlayer(c):
    global N
    k = 0
    for i in range(N):
        if i not in c["id"] and i in players:
            del players[i]
            k += 1
    N -= k


def toggleFullscreen():
    global fullscreen, screen

    fullscreen = not fullscreen
    screen = d.set_mode(SCREENSIZE, FULLSCREEN) if fullscreen else d.set_mode((K.width, K.height))

    scale = 3 if fullscreen else 2
    for i in Client.clientList["id"]:
        players[i].scale = scale


def gameLoop():
    def update(j=x):
        c = Client.clientList
        screen.fill(K.black)
        if c["count"] > N:
            addPlayer(c)
        elif c["count"] < N:
            delPlayer(c)

        for i in c["id"]:
            st, sc = c["players"][f'{i}']
            if i != x and i != j and players[i].currentState != st:
                if st == State.active:
                    players[i].Ground.start(update, 5)
                elif st == State.idle:
                    players[i].Ground.stop(update)
                elif st == State.jump:
                    players[i].jump(update)

            players[i].update()
            players[i].draw(screen, sc)
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
                if keys[K_q]:
                    players[x].currentState = State.exit
                    pygame.quit()
                    sys.exit()

                if keys[K_LCTRL] and keys[K_f] and (keys[K_LSUPER] or keys[K_LSHIFT]):
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

if x != -1:
    gameLoop()
else:
    print("Game full.")
