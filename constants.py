# -------------------------------------------------------------------- #
# constants.py
# -------------------------------------------------------------------- #

# Titles, names, labels
WINDOW_CAPTION = "Platformer Engine Test"
DEV_STUDIO = "Name Subject To Change Studios"

# FPS
FPS = 60
GAMESPEED = 1 / FPS
SCALE = 60

# Asset paths
TITLE_FONT = 'assets/fonts/pixeldroidBoticRegular.ttf'
HUD_FONT = 'assets/fonts/alagard_by_pix3m-d6awiwp.ttf'
CHARACTER_SHEET = 'assets/sprites/sonicmania.png'
LEVEL_01_TMX = 'assets/levels/ghz1.tmx'
LEVEL_01_TSX = 'assets/levels/ghz.tsx'
LEVEL_01_TILESET = 'assets/tilesets/cavestory-sand.png'

# Player states
STOPPED_STATE = "stopped"
WALKING_STATE = "walking"
RUNNING_STATE = "running"
JUMPING_STATE = "jumping"
ROLLING_STATE = "rolling"
DASHING_STATE = "dashing"

# Sensor states
SENSOR_RIGHT_FLOOR = "right floor"
SENSOR_LEFT_FLOOR = "left floor"
SENSOR_RIGHT_WALL = "right wall"
SENSOR_LEFT_WALL = "left wall"

# Sonic spritesheets & animations
WALK_FRAMES_COUNT = 12 # there are 12 walk right sonic frames
WALK_START_POS = (1, 142) # x and y of right walking sprites on the sprite sheet
STAND_FRAMES_COUNT = 1
STAND_START_POS = (1, 13)

FRAME_SPACING = 1 # each sprite canvas is seperated by 1 pixel
FRAME_WIDTH = 48 # each sonic sprite is 48 pixels wide, by 48 pixels high
FRAME_HEIGHT = 48

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 100, 10)
YELLOW = (255, 255, 0)
PINK = (255, 100, 180)
PURPLE = (240, 0, 255)
GRAY = (127, 127, 127)
BROWN = (100, 40, 0)

# Scene colors
TITLE_BG_COLOR = BLACK
GAME_BG_COLOR = GREEN

# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Collision mask colors
MASK_BG_COLOR = RED
MASK_COLOR = BLACK

# Dimensions of tiles in Tiled maps
TILE_DIMENSIONS = (16, 16)
