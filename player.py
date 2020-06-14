# -------------------------------------------------------------------- #
# player.py
#   Player class
# -------------------------------------------------------------------- #

# Game library imports:
import pygame
# Local imports:
from spritesheet import SpriteSheet
from constants import *
from sensor import Sensor

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # TODO: allow these to be defined by passing arguments when class instance is created
        self.air = 0.09375
        self.jump_speed = 6.5
        self.top_speed = 6
        self.gravity = 0.21875

        # Physics variables
        self.x_speed = 0
        self.y_speed = 0
        self.on_ground = False

        # TODO: Make a proper sprite sheet.
        player_sprites = SpriteSheet(CHARACTER_SHEET)  # temporary sprite sheet, placeholder.

        self.p_walk_frames_r = []

        # Load all the right facing images into a list
        image = player_sprites.get_image(1, 13, 48, 48)
        self.p_walk_frames_r.append(image)

        # Set the image the player starts with
        self.image = self.p_walk_frames_r[0]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        # variables for location of player on screen
        self.rect.x, self.rect.y = x, y

        # Sensors (for collision physics)
        # see http://info.sonicretro.org/SPG:Solid_Tiles#Sensor_Process
        self.s_center = Sensor(self.rect, [25, 29], 1, 1, WHITE)
        self.s_left_wall = Sensor(self.rect, [25-8, 29], 8, 1, PINK)
        self.s_right_wall = Sensor(self.rect, [25+1, 29], 8, 1, RED)
        self.s_left_floor = Sensor(self.rect, [25-7, 29+1], 1, 19, GREEN)
        self.s_right_floor = Sensor(self.rect, [25+7, 29+1], 1, 19, PURPLE)
        self.sensors = [
            self.s_center,
            self.s_left_wall,
            self.s_right_wall,
            self.s_left_floor,
            self.s_right_floor
        ]

    def update(self):
        # Move left/right & up/down based on x & y speeds
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Update the sensors to player's new position
        for sensor in self.sensors:
            sensor.update(self.rect)

