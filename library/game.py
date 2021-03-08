import pygame
import pygame.freetype
from pygame.locals import *

import sys

from library.Elements import Ground, Player
from library.constants import K, State
from library.Sprites import Sprites

pointTo = Sprites.Offset

playerOffset = (0.5, 0.87)
player: Player
score = 0

pygame.init()
clock = pygame.time.Clock()
display = pygame.display


K.screenSize = (display.Info().current_w, display.Info().current_h)
screen = display.set_mode((K.width, K.height))
display.set_caption("RUN")


def generateStates():
    states = {
        State.active: Sprites("running animation", 13, offset=playerOffset),
        State.jump: Sprites("jump", 14, offset=playerOffset),
        State.idle: Sprites("idle", 16, offset=playerOffset),
        State.slowDown: Sprites("run to stop", 13, offset=playerOffset),
        State.disconnected: Sprites("disconnect", 13, offset=playerOffset, once=True)
    }

    return states


def toggleFullscreen():
    global screen

    K.fullscreen = not K.fullscreen
    screen = display.set_mode(K.screenSize, FULLSCREEN) if K.fullscreen else display.set_mode((K.width, K.height))

    scale = 3 if K.fullscreen else 2
    player.scale = scale


def isQuit():
    if pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    if pygame.event.get(KEYDOWN):
        if pygame.key.get_pressed()[K_ESCAPE]:
            pygame.quit()
            sys.exit()


def gameLoop():
    def update():
        screen.fill(K.black)

        player.update()
        player.draw(screen, score)
        display.flip()

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
                    player.currentState = State.exit
                    pygame.quit()
                    sys.exit()

                if keys[K_LCTRL] and keys[K_f] and (keys[K_LSUPER] or keys[K_LSHIFT]):
                    toggleFullscreen()
                    continue

                if keys[K_SPACE]:
                    player.Ground.start(update, 5)
                elif keys[K_x]:
                    player.Ground.stop(update)
                elif keys[K_j]:
                    player.jump(update)

        update()


player = Player(generateStates(), Ground("footpath"), screen=(K.width, K.height), scale=2)
gameLoop()
