import pygame
import pygame.freetype
from pygame.locals import *

import sys
from library.Elements import Ground, Player
from library.constants import K, State
from library.Sprites import Sprites
from library.ui import Background

pointTo = Sprites.Offset

playerOffset = (0.5, 0.87)
player: Player
score = 0

pygame.init()
clock = pygame.time.Clock()
display = pygame.display


K.screenSize = (display.Info().current_w, display.Info().current_h)
K.currentScreenSize = (K.width, K.height)
screen = display.set_mode(K.currentScreenSize)
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

    K.isFullScreen = not K.isFullScreen
    if K.isFullScreen:
        K.currentScreenSize = K.screenSize
        screen = display.set_mode(K.screenSize, FULLSCREEN)
        scale = 3
    else:
        K.currentScreenSize = (K.width, K.height)
        screen = display.set_mode((K.width, K.height))
        scale = 2

    player.scale = scale
    background.scaleToFitHeight()


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
        background.update()
        player.update()

        background.draw(screen)
        player.draw(screen)

        display.update()

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
                    player.Ground.start(10, 0.6)
                    background.start()
                elif keys[K_x]:
                    player.Ground.stop()
                    background.stop()
                elif keys[K_j]:
                    player.jump()

        update()


player = Player(generateStates(), Ground("footpath"), scale=2)
bgLayers = "sky", "MountBack", "MountMiddle", "MountFront", "BuildingsBack"
background = Background(bgLayers, (2, 4))
gameLoop()
