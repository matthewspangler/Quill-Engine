# -------------------------------------------------------------------- #
# game.py
#   contains main game loop,
#	including events, drawing, and update
# -------------------------------------------------------------------- #
pass
# General imports:
import sys
# Game related imports:
import pygame
from pygame.locals import *
import pytmx
import pyscroll
# Local imports:
from constants import *
from player import Player
from scene import Scene

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
        self.player_one = Player(100, 120)

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

    # Events: processing input from user via keyboard, mouse, etc
    def events(self, events, pressed_keys):
        for event in events:
            if event.type == QUIT:
                # exit button or quit command issued
                pygame.quit()
                sys.exit()
            # Key down events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print("Player input: W")
                elif event.key == pygame.K_a:
                    print("Player input: A")
                    if self.player_one.x_speed > -10:  # speed limit
                        self.player_one.x_speed -= 1
                elif event.key == pygame.K_s:
                    print("Player input: S")
                elif event.key == pygame.K_d:
                    print("Player input: D")
                    if self.player_one.x_speed < 10:  # speed limit
                        self.player_one.x_speed += 1
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_F10:
                    self.debug_mode = not self.debug_mode
                    print("Debug mode switched")
            # Key up events
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    print("Player released: W")
                elif event.key == pygame.K_a:
                    if self.player_one.x_speed < 0:
                        self.player_one.x_speed += 1
                    print("Player released: A")
                elif event.key == pygame.K_s:
                    print("Player released: S")
                elif event.key == pygame.K_d:
                    if self.player_one.x_speed > 0:
                        self.player_one.x_speed -= 1
                    print("Player released: D")

    # game logic/mechanics here. process user input
    def update(self, dt):
        # TODO: de-spaghettify the collision logic!
        layer_index = 0
        for layer in self.lvl1_tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                # layer is tile layer
                pass
            layer_index += 1
            if isinstance(layer, pytmx.TiledObjectGroup):
                # layer is object layer
                if layer.name == "Collision Layer": # layer is collision layer
                    # Check for collision with sensors:
                    # TODO: some of this collision code needs moved to sensor.collide function
                    # TODO: collision with Rect's can't handle slopes!
                    for sensor in self.player_one.sensors:
                        # Check if each object in collision layer has collided with the sensor
                        collisions = 0
                        for obj in layer:
                            solid_tile = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            # Check for collision with sensors:
                            if sensor.rect.colliderect(solid_tile):
                                collisions += 1
                        if collisions >= 1:
                            sensor.activated = True
                        else:
                            sensor.activated = False

        # Check if player is on ground:
        if self.player_one.s_left_floor.activated or self.player_one.s_right_floor.activated:
            self.player_one.on_ground = True

        # Make player fall (gravity) unless player is on the ground.
        if self.player_one.on_ground:
            self.player_one.y_speed = 0
        else:
            self.player_one.y_speed += self.player_one.gravity

        # Update the player position
        self.player_one.update()

        # Update active sprite group
        self.active_sprite_list.update()

    # Code for what is drawn on screen each frame here
    def draw(self, screen, surface):
        # Clear screen
        surface.fill(BLACK)

        # Draw sprite / level data group to surface
        self.group.draw(surface)

        # Debug mode rendering logic
        if self.debug_mode:
            self.draw_debug(screen, surface)

        # Draw/render surface onto screen
        screen.blit(surface, (0, 0))

    # All this function's code could just be put into the draw() function,
    # but I put it here because I'm tired of scrolling over it.
    def draw_debug(self, screen, surface):
        screen.fill(TITLE_BG_COLOR)

        # Make small font
        debugFont = pygame.font.Font(HUD_FONT, 30)

        # Create instances of text
        debugText = debugFont.render("Debug mode", False, WHITE)
        positionText = debugFont.render("Player X,Y: %s,%s" %
                                        (self.player_one.rect.x, self.player_one.rect.y), False, WHITE)

        # Render the debug text
        surface.blit(debugText, (5, 5))
        surface.blit(positionText, (20, 35))

        # Render the sensors
        for sensor in self.player_one.sensors:
            if sensor.activated:
                pygame.draw.rect(surface, sensor.active_color, sensor)
            else:
                pygame.draw.rect(surface, sensor.inactive_color, sensor)
