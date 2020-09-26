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
states = {
    Player.State.active: Sprites("running animation", 13, offset=playerOffset),
    Player.State.jump: Sprites("jump", 14, offset=playerOffset),
    Player.State.idle: Sprites("idle", 16, offset=playerOffset)
}

G = Ground("ground")
P = Player(states, G, x=int(K.width*0.23), y=K.height - int(G.tile.h * 0.8), scale=2)


def toggleFullscreen():
    global fullscreen, screen

    fullscreen = not fullscreen
    screen = d.set_mode(SCREENSIZE, FULLSCREEN) if fullscreen else d.set_mode((K.width, K.height))
    P.scale = 3 if fullscreen else 2

    S = (d.Info().current_w, d.Info().current_h)

    x = int(S[0] * 0.23)
    y = P.groundY = S[1] - int(P.Ground.tile.h * 0.8)
    for state in P.state.values():
        state.x = x
        state.y = y


def gameLoop():
    def update():
        screen.fill(K.black)
        P.update()
        P.draw(screen)
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
                    P.Ground.start(update, 5, P)
                elif keys[K_x]:
                    P.Ground.stop(update, P)
                elif keys[K_j]:
                    P.jump(update)

        update()


gameLoop()
