
# Game library imports
import pygame

# Local imports
from constants import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        # Call the parent's constructor
        super().__init__()

        # Set image
        self.image = image

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        # Position of tile/platform in grid
        self.grid_x, self.grid_y = x, y

        # Add position of tile to the tile.rect.
        # X and Y are only the location of the tile in the grid, not the x, y in pixels.
        self.rect.x, self.rect.y = self.grid_x * TILE_DIMENSIONS[0], self.grid_y * TILE_DIMENSIONS[1]

        # Pixel array helps us set up the mask
        pixelArray = pygame.PixelArray(image)

        # Extract red color from collision tiles, making it transparent
        # In the collision mask, red is the color we want to ignore, the background color.
        pixelArray = pixelArray.extract(MASK_BG_COLOR)

        # Make surface from the pixel array
        mask_surface = pixelArray.make_surface()
        mask_surface.set_colorkey(WHITE)

        # Set collision mask
        self.mask = pygame.mask.from_surface(mask_surface)

        # Clean up
        pixelArray.close()
