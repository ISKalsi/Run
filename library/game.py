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

states = {
    Player.State.idle: Sprites("running animation", 13, offset=(0.5, 0.87)),
    # Player.State.idle: Sprites("jump", 14, offset=(0.5, 0.87)),
    Player.State.jump: Sprites("jump", 14, offset=(0.5, 0.87))
}

G = Ground("ground")
# P = Player("stickman_still", x=int(K.width*0.33), y=(K.height*0.86), offset=(0.5, 0.824))
P = Player(states, G, x=int(K.width*0.23), y=int(K.height*0.86), scale=2)


def toggleFullscreen():
    global fullscreen, screen

    fullscreen = not fullscreen
    screen = d.set_mode(SCREENSIZE, FULLSCREEN) if fullscreen else d.set_mode((K.width, K.height))
    G.scale = 6.6 if fullscreen else 4
    # P.scale = 6 if fullscreen else 4
    P.scale = 5 if fullscreen else 2
    S = (d.Info().current_w, d.Info().current_h)
    # P.x = int(S[0]*0.33)
    P.x = int(S[0] * 0.23)
    P.y = P.groundY = int(S[1] * 0.86)


def gameLoop():
    def update():
        screen.fill(K.black)
        G.update()
        P.update()
        G.sprites.draw(screen)
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
                    G.start(update, 5)
                elif keys[K_x]:
                    G.stop(update)
                elif keys[K_j]:
                    P.jump(update)

        update()


gameLoop()
