import pygame

# local imports
from constants import *

class Sensor(pygame.sprite.Sprite):
    def __init__(self, player_rect, offset, width, height, inactive_color=GRAY, active_color=WHITE):
        # Call the parent's constructor
        super().__init__()
        # If the sensor is triggered by a solid object or tile, it becomes activated
        self.activated = False
        # Offset is the starting position of the sensor rectangle relative to the player rect x/y
        # Offset should be in [x, y] format
        self.offset = offset
        self.rect = pygame.Rect(player_rect.x + offset[0], player_rect.y + offset[1], width, height)
        # Active and inactive color are useful for debug mode, so we can see which sensors are being triggered
        self.active_color = active_color
        self.inactive_color = inactive_color
        # Make an image so we can create a mask for collision, AND draw it to screen during debug mode
        self.image = pygame.Surface([self.rect.width, self.rect.height])
        # Fill surface with color so we can generate the mask
        self.image.fill(MASK_COLOR)
        self.image.set_colorkey(MASK_BG_COLOR)
        # Generate mask (for pixel-accurate collision)
        self.mask = pygame.mask.from_surface(self.image)

    # Sensors require the player's rectangle in order to update their positions
    def update(self, player_rect):
        # align sensors relative to player position
        self.rect.x = player_rect.x + self.offset[0]
        self.rect.y = player_rect.y + self.offset[1]

    def collide(self, rect):
        # TODO: code for collision with sensor here
        pass