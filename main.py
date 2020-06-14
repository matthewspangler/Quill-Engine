# -------------------------------------------------------------------- #
# Quill Engine - A Platformer Game Engine
# By Matthew Spangler
# -------------------------------------------------------------------- #
# main.py
#   main function, create instance of Title Screen scene, game loop.
# -------------------------------------------------------------------- #

# Game library imports:
import pygame
# Local imports:
from constants import *
from title import TitleScene

def main():
    # Initialize all imported pygame modules
    pygame.init()

    # Set up FPS
    fps = 60
    fpsClock = pygame.time.Clock()

    # Set screen/window resolution
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    # Set starting scene as the title screen / main menu
    starting_scene = TitleScene()

    # Set up title scene
    active_scene = starting_scene
    
    active_surface = pygame.Surface([640, 480])

    # Game loop.
    while True:
        # Frames per second command
        dt = fpsClock.tick(fps)

        # Change scene if previous scene ended
        active_scene = active_scene.next

        # Check for user input
        active_scene.events(pygame.event.get(), pygame.key.get_pressed())

        # Game logic & mechanics
        active_scene.update(dt)

        # Draw / render frame
        active_scene.draw(screen, active_surface)

        # This command makes everything drawn on screen finally get displayed
        pygame.display.flip()  # TODO: should I use display.update() instead?

if __name__ == "__main__":
    main()
