class K:
    # screen
    screenSize: tuple[int, int]
    fullScreen = False
    width = 1200
    height = 800
    fps = 60

    # colors
    black = (0, 0, 0)
    green = (0, 255, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    transparent = (0, 0, 0, 0)

    # fonts
    scoreFont = "LcdSolid.ttf"


class State:
    idle, active, jump, slowDown = range(4)
    full, disconnected, exit = range(-3, 0)
