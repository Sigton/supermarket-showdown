import pygame

SCREEN_X = 960
SCREEN_Y = 720
RESOLUTION = [SCREEN_X, SCREEN_Y]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

TILE_RES = 48

SPAWN_POINTS = [(4, -1), (10, -1)]
PATHFINDING_GOAL = (7, 13)

# must be a factor of 48
CUSTOMER_MOVE_SPEED = 0.5
CUSTOMER_ANIM_SPEED = 10

DAY_LENGTH = 300

# wave generation constants
INIT_WAVE_SIZE = 5
WAVE_SIZE_MUL = 1.2
VARIANCE = 3

# balancing constants
INITIAL_SALARY = 50
INITIAL_MONEY = 750
SALARY_INCREASE = 25

# font time
def load_font(font_size):
    return pygame.font.Font("src/resources/font.otf", font_size)