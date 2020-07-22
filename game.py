# -------------------------------------------------------------------- #
# game.py
#   contains main game loop,
#	including events, drawing, and update
# -------------------------------------------------------------------- #

# General imports:
import sys

# Game related imports:
import pygame
import pyscroll
import pytmx
from pygame.locals import *

# Local imports:
from constants import *
from player import Player
from scene import Scene
from solid_platform import Platform

class GameScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        # Set window caption
        pygame.display.set_caption(WINDOW_CAPTION)

        # TODO: rewrite scenes class to allow resizing of screen globally.
        # See end paragraph of this article:https://nerdparadise.com/programming/pygame/part7
        screen_size = [SCREEN_WIDTH, SCREEN_HEIGHT]

        # List variable for layers - 0 = background color; 1 = scenery; 2 = level; 3 = player; 4 = foreground
        # Each layer is a seperate surface.
        self.layers = [pygame.Surface(screen_size) for i in range(4)]

        # Create a sprite group of active sprites, which are all rendered in draw() function
        self.active_sprite_list = pygame.sprite.Group()

        # Create instance of player
        self.player_one = Player(150, 50, self)

        # Add player to list of active sprites, so it gets rendered in draw() function
        self.active_sprite_list.add(self.player_one)

        # Time to load our TMX level map.
        self.lvl1_tmx_data = pytmx.load_pygame(LEVEL_01_TMX)

        # Create new data source for pyscroll
        self.map_data = pyscroll.data.TiledMapData(self.lvl1_tmx_data)

        # Create new renderer (camera)
        # Clamp_camera is used to prevent the map from scrolling past the edge
        # TODO: remove screen width/height constants once we get dynamic screen sizes figured out
        self.map_layer = pyscroll.BufferedRenderer(self.map_data,
                                                   screen_size,
                                                   clamp_camera=True)
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)

        # TODO: Figure out how to center player in map.
        # TODO: uncomment the following lines of code, and remove/rewrite active_sprite_list
        # For that, see https://github.com/bitcraft/pyscroll/wiki/Tutorial-(WIP)

        # Add our player to the group
        self.group.add(self.player_one)

        # Can be switched on with F10 key, for that see events()
        self.debug_mode = False

        self.jump_key_pressed = False

        self.platforms = self.get_solid_platforms(self.lvl1_tmx_data.get_layer_by_name("Collision Mask"))

    def get_solid_platforms(self, tmx_layer):
        solid_platforms = []
        # Least effort involved getting all tile images.
        # TODO: If we could only check tiles near player's sensors, that might be faster.
        for x, y, image in tmx_layer.tiles():
            solid_platforms.append(Platform(x, y, image))
        return solid_platforms

    # Events: processing input from user via keyboard, mouse, etc
    def events(self, events, pressed_keys):
        for event in events:
            if event.type == QUIT:
                # exit button or quit command issued
                pygame.quit()
                sys.exit()
            # Key down events
            elif event.type == pygame.KEYDOWN:
                # Player keypress events
                self.player_one.key_press(event, pressed_keys)

                # Advances player animation to next frame in list
                if event.key == pygame.K_n:
                    self.player_one.advance_animation()
                # Quit game key
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Turn on debug mode
                elif event.key == pygame.K_F10:
                    self.debug_mode = not self.debug_mode
                    print("Debug mode switched")

            # Key up events
            elif event.type == pygame.KEYUP:
                # Player key release events
                self.player_one.key_release(event, pressed_keys)

    # game logic/mechanics here. process user input
    def update(self, dt):

        # Update active sprite group
        self.active_sprite_list.update(dt)

    # Code for what is drawn on screen each frame here
    def draw(self, screen, surface):
        # Clear screen/fill with background color
        surface.fill(GAME_BG_COLOR)

        # Draw sprite / level data group to surface
        self.group.draw(surface)

        # Debug mode rendering logic
        if self.debug_mode:
            self.draw_debug(screen, surface)

        # Draw/render surface onto screen
        screen.blit(surface, (0, 0))

    # All this function's code could just be put into the draw() function,
    # but I put it here because I'm tired of scrolling over it.
    # TODO: rewrite debug drawing code so all text in in a list that is displayed within a for loop.
    # TODO: that way we can add more debug outputs easily by appending them to the list
    def draw_debug(self, screen, surface):
        screen.fill(TITLE_BG_COLOR)

        # Make small font
        debugFont = pygame.font.Font(HUD_FONT, 20)

        # Create instances of text
        debugText = debugFont.render("Debug mode", False, WHITE)
        positionText = debugFont.render("Player X,Y: %s,%s" %
                                        (self.player_one.rect.x, self.player_one.rect.y), False, WHITE)
        speedText = debugFont.render("XSP, YSP: %s,%s" %
                                        (self.player_one.x_speed, self.player_one.y_speed), False, WHITE)
        playerstateText = debugFont.render("State: %s" % self.player_one._state, False, WHITE)

        # Render the debug text
        surface.blit(debugText, (5, 5))
        surface.blit(positionText, (20, 35))
        surface.blit(speedText, (20, 65))
        surface.blit(playerstateText, (20, 95))

        # Render the sensors
        for sensor in self.player_one.sensors:
            if sensor.activated:
                pygame.draw.rect(surface, sensor.active_color, sensor)
            else:
                pygame.draw.rect(surface, sensor.inactive_color, sensor)
