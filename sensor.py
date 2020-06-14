import pygame
#local imports
from spritesheet import SpriteSheet
from constants import *

class Sensor(pygame.sprite.Sprite):
    def __init__(self, player_rect, offset, width, height, inactive_color=GRAY, active_color=WHITE):
        # Call the parent's constructor
        super().__init__()
        self.activated = False
        # Offset is the starting position of the sensor rectangle relative to the player rect x/y
        # Offset should be in [x, y] format
        self.offset = offset
        self.rect = pygame.Rect(player_rect.x + offset[0], player_rect.y + offset[1], width, height)
        self.active_color = active_color
        self.inactive_color = inactive_color

    # Sensors require the player's rectangle in order to update their positions
    def update(self, player_rect):
        self.rect.x = player_rect.x + self.offset[0]
        self.rect.y = player_rect.y + self.offset[1]

    def collide(self, rect):
        # TODO: code for collision with sensor here
        pass