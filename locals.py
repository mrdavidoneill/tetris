import pygame, sys, random                  # sys for closing programm.  random for Apple position
from pygame.locals import *                 # for using pygame keywords like QUIT or KEYDOWN

pygame.init()  # Initialises pygame for all

# =========== CONSTANTS =========== #

# =========== COLOURS =========== #
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
GREY = (155,155,155)
RED   = (255,  0,  0)
GREEN   = (0,  255,  0)
BLUE   = (0,  0,  255)
CYAN   = (0,  255,  255)
PURPLE   = (128,  0,  128)
ORANGE   = (255,  165,  0)
YELLOW =  (255,  255,  0)

# =========== KEYWORDS =========== #
DOWN = "down"
LEFT = "left"
RIGHT = "right"
I = "i"
O = "o"
T = "t"
S = "s"
Z = "z"
J = "j"
L = "l"
LANDED = "landed"
POSSIBLE = "possible"
ROTATIONS = "rotations"
COLOR = "color"

KEY_TO_DIR = {K_LEFT: LEFT, K_RIGHT: RIGHT, K_DOWN: DOWN}