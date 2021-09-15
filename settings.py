#game options/settings
WIDTH = 480
HEIGHT = 600
FPS = 60
TITLE = "Jumpy!"
FONT_NAME = "arial"
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
MOB_LAYER = 2

#player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
GRAVITY = 0.8
MAX_JUMP = -22

#starting platforms
PLATFORM_LIST = [(10, HEIGHT-40),
                 (WIDTH/2-50, HEIGHT*3/4),
                 (125, HEIGHT-350),
                 (350, 200),
                 (173, 100)]

#define colors
WHITE = (255, 255, 255)
BGCOLOR = (0, 155, 155)

#mob
MOB_FREQ = 5000
