import pygame
import random

# Screen settings
GAME_NAME = 'Dungeon Archer'
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
HUD = 50
FPS_GAME = 60
FPS_MENU = 8

# Fonts settings
pygame.font.init()
font_hud = pygame.font.Font('./config/fonts/VecnaBold.ttf', 36)
font_hud_num = pygame.font.Font('./config/fonts/Tridenth.ttf', 40)
font_dmg = pygame.font.Font('./config/fonts/AtariClassic.ttf', 16)
font_crit = pygame.font.Font('./config/fonts/AtariClassic.ttf', 20)

# Player settings
PLAYER_OFFSET = 12
PLAYER_VELOCITY = 3.85
PLAYER_BOOST_SCALE = 1.45
SCALE = 2.5

# Map settings
TILE_SIZE = 42  # default setting 48=16x3
ROW = 50
COLUMNS = 80
SCROLL_THRESH = 250
TILE_AMOUNT = 40  # last image index in config/images/maps

# Weapon settings
ARROW_SPEED = 10
ARROW_OFFSET = 50
FIREBALL_OFFSET = 15

# Enemy settings
ENEMY_SCALE = 1
ENEMY_SPEED = 4
ENEMY_OFFSET = 3
AI_COUNTER = 3
ENEMY_AI_SPEED = 0.75

# Damage setting

DAMAGE_TEXT_SPEED = 1.35

# Objects setting
OBJECT_SCALE = 2.5

# Items settings
ITEM_SCALE = 1

# Color settings
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
RED_dark = (160, 30, 50)
BLUE = (0, 190, 245)
BG = (241, 241, 244)
GRAY = (88, 88, 88)
BAR_TOP = (150, 250, 250)
BAR_END = (50, 150, 250)
GREEN = (12, 236, 16)
COLOR_01 = (236, 236, 45)
MIX = (154, 212, 52)
COLORS = []
for i in range(10):
    COLOR = (random.randint(15, 255), random.randint(65, 255), random.randint(15, 255))
    COLORS.append(COLOR)

# Function
path = './config/settings/'
typ = '.txt'


def get_value(name):
    file_name = str(path + name + typ)
    with open(file_name, 'r') as file:
        value = int(file.read())
    return value


def update_value(name, value):
    file_name = str(path + name + typ)
    with open(file_name, "w") as file:
        file.write(str(value))
    return True
