import pygame

# local imports
from constants import *

# TODO: I have some old code commented out, which I will delete when I'm sure I don't need it.

class Sensor(pygame.sprite.Sprite):
    def __init__(self, player_rect, relative_position, sensor_state, inactive_color=GRAY, active_color=WHITE):
        # Call the parent's constructor
        super().__init__()

        # Sensor is active when it detects collision with a solid object
        self.activated = False

        # State keeps track of whether it's a floor, wall, or ceiling sensor
        self.state = sensor_state

        # Sensor's x/y determined via offset of player's x/y 
        self.relative_position = relative_position

        # Local variables to make self.rect definition more human-readable,
        # although these aren't really necessary:
        relative_x = self.relative_position[0]
        relative_y = self.relative_position[1]
        width = 1
        height = 1

        # Define the rectangle
        self.rect = pygame.Rect(player_rect.x + relative_x,
                                player_rect.y + relative_y, width, height)

        # Colors help us distinguish the sensors with our eyes in debug mode
        self.active_color = active_color
        self.inactive_color = inactive_color

        # Image allows us to create a collision mask with pygame
        self.image = pygame.Surface([self.rect.width, self.rect.height])

        # Mask colors help us generate the collision mask
        self.image.fill(MASK_COLOR)
        self.image.set_colorkey(MASK_BG_COLOR)

        # And here's out collision mask!
        self.mask = pygame.mask.from_surface(self.image)

    # Sensors require the player's rectangle in order to update their positions
    def update(self, player_rect):
        # align sensors relative to player position
        self.rect.x = player_rect.x + self.relative_position[0]
        self.rect.y = player_rect.y + self.relative_position[1]

    """http://info.sonicretro.org/SPG:Solid_Tiles#Height_Masks
    If the height value found is 16px ($10), that's the entire tile filled at that X position, so 
    then the sensor has to check for another tile above the first one found, 
    and search for that one's height value. """
    def collide(self, platform):
        collision_coordinates = pygame.sprite.collide_mask(platform, self)
        if collision_coordinates:  # If collision happened
            # http://info.sonicretro.org/SPG:Solid_Tiles#Height_Masks
            absolute_collision = (platform.rect.x + collision_coordinates[0], platform.rect.y + collision_coordinates[1])
            height = self.rect.bottom - absolute_collision[1]
            return True, height
        return False, None

    # TODO: function should detect platforms nearby, not just ones directly collided with.
    def detect_plaforms(self, platforms):

        # What's the best way to check only the adjacent tiles to the sensor?
        # We want to avoid checking every tile on the map because that's a waste of processing

        height = 0
        collision_count = 0
        for platform in platforms:
            collided, new_height = self.collide(platform)
            if collided:
                collision_count += 1
                self.activated = True
                # http://info.sonicretro.org/SPG:Solid_Tiles#Reaction
                # Once a tile has been found, it's 'height' (or position horizontally for horizontal sensors)
                # will be returned for Sonic to use to re-position himself.
                height = new_height
        if collision_count == 0:
            self.activated = False
        return height
