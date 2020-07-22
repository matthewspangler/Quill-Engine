#-------------------------------------------------------------------- #
# player.py
#   Player class
# -------------------------------------------------------------------- #

import pygame
from math import sin, cos
from constants import *
from sensor import Sensor
from spritesheet import SpriteSheet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        # Call the parent's constructor
        super().__init__()

        self.game = game

        # Physics constants:
        self.air = 0.09375
        self.jump_speed = 6.5
        # TODO: set top_speed in accordance with sonic physics guide
        self.top_speed = 6
        self.gravity = 0.21875
        self.acceleration = 0.5
        self.deaccelerate = 0.5
        self.friction = 0.5
        # TODO : check if we need the next two:
        self.roll = 1.03125
        self.slope = 0.125

        # Movement can be rotated using angle and gangle:
        self.angle = 0.0
        self.gangle = 0.0
        self.rangle = 0.0

        # http://info.sonicretro.org/SPG:Solid_Tiles#The_Three_Speed_Variables
        # 3 Speed Variables:
        self.x_speed = 0
        self.y_speed = 0
        self.ground_speed = 0

        # Player's states
        self._state = STOPPED_STATE

        # Flags
        self.flag_ground = False
        self.flag_allow_jump = False
        self.flag_allow_vertical_movement = True
        self.flag_jump_next_frame = False
        self.flag_fell_off_wall_or_ceiling = False
        # TODO: I might not need this one?:
        self.flag_is_jumping = False

        # What movement keys are pressed
        self.key_up = False
        self.key_down = False
        self.key_left = False
        self.key_right = False
        self.key_jump = False

        # Get player sprite sheet
        player_sprites = SpriteSheet(CHARACTER_SHEET)

        # Animation lists
        self.walk_frames = []
        self.stand_frames = []
        self.dash_frames = []
        self.run_frames = []
        self.jump_frames = []

        # Append walking frames
        for x in range(WALK_FRAMES_COUNT):
            image = player_sprites.get_image(
                x * FRAME_WIDTH + x * FRAME_SPACING,
                WALK_START_POS[1], FRAME_WIDTH, FRAME_HEIGHT)
            self.walk_frames.append(image)

        # Append standing / stopped frames
        for x in range(STAND_FRAMES_COUNT):
            image = player_sprites.get_image(
                x * FRAME_WIDTH + x * FRAME_SPACING,
                STAND_START_POS[1], FRAME_WIDTH, FRAME_HEIGHT)
            self.stand_frames.append(image)

        # TODO: remove these three lines once we get dash & jump frames implimented
        self.dash_frames = self.walk_frames
        self.jump_frames = self.walk_frames
        self.run_frames = self.walk_frames

        # A dictionary of the various animations that correspond to Sonic's various states.
        self.animations = {
            WALKING_STATE: self.walk_frames,
            JUMPING_STATE: self.jump_frames,
            STOPPED_STATE: self.stand_frames,
            RUNNING_STATE: self.run_frames,
            DASHING_STATE: self.dash_frames
        }

        # A variable containing Sonic's current, active state:
        self._state = STOPPED_STATE

        # The current frame in Sonic's animation sequence.
        self.frame_index = 0

        # Set the image the player starts with
        self.image = self.animations.get(self._state)[self.frame_index]

        # Set a reference to the image rect.
        self.rect = self.image.get_rect()

        # variables for location of player on screen
        self.rect.x, self.rect.y = x, y

        # Sensors (for collision physics)
        # see http://info.sonicretro.org/SPG:Solid_Tiles#Sensor_Process

        # TODO: double sensor positions for accuracy!
        # TODO: make ceiling sensors!
        self.s_left_wall = Sensor(self.rect, [25, 29],
                                  SENSOR_LEFT_WALL, PINK)
        self.s_right_wall = Sensor(self.rect, [34, 29],
                                   SENSOR_RIGHT_WALL, RED)
        self.s_left_floor = Sensor(self.rect, [18, 30],
                                   SENSOR_LEFT_FLOOR, GREEN)
        self.s_right_floor = Sensor(self.rect, [32, 30],
                                    SENSOR_RIGHT_FLOOR, PURPLE)
        self.sensors = [
            self.s_left_wall,
            self.s_right_wall,
            self.s_left_floor,
            self.s_right_floor
        ]

    # Change sonic to a different state and reset the animation for the new state
    def change_state(self, state):
        if self._state != state:
            self._state = state
            self.frame_index = 0

    # Advance to the next frame in sonic's animation sequence
    def advance_animation(self):
        # Jump back to frame 0 if last frame in list was reached
        if self.frame_index < len(self.animations.get(self._state)) - 1:
            self.frame_index += 1
        else:
        # Otherwise, advance to the next frame in the animation sequence!
            self.frame_index = 0

    def handle_physics(self, dt):
        self.advance_animation()

    def perform_gravity_movement(self, dt):
        self.y_speed += self.gravity / dt

    # States are used to change the animations
    def calculate_state(self):
        if self.flag_ground:
            # stopped
            if self.ground_speed == 0:
                self.change_state(STOPPED_STATE)
            # walk right
            elif self.ground_speed > 0 and self.ground_speed < 6:
                self.change_state(WALKING_STATE)
            # walk left
            elif self.ground_speed < 0 and self.ground_speed > -6:
                self.change_state(WALKING_STATE)
            # run right
            elif self.ground_speed > 6 and self.ground_speed < 10:
                self.change_state(RUNNING_STATE)
            # run left
            elif self.ground_speed < -6 and self.ground_speed > -10:
                self.change_state(RUNNING_STATE)
            # dash right
            elif self.ground_speed > 10:
                self.change_state(DASHING_STATE)
            #dash left
            elif self.ground_speed < -10:
                self.change_state(DASHING_STATE)
            else:
                print("if you got here, this logic chain is broken")

        print("finish")

    # Handle key press events for player
    def key_press(self, event, pressed_keys):
        if event.key == pygame.K_a:
            print("Player input: A")
            self.key_left = True
        elif event.key == pygame.K_d:
            print("Player input: D")
            self.key_right = True

    # Handle key release events for player    
    def key_release(self, event, pressed_keys):
        if event.key == pygame.K_a:
            print("Player input: A")
            self.key_left = False
        elif event.key == pygame.K_d:
            print("Player input: D")
            self.key_right = False

    def perform_ground_test(self):
        pass

    def perform_speed_movement(self, dt):
        print(dt)
        self.rect.y += self.y_speed * dt

    # This function is called every frame
    def update(self, dt):
        # Prevents jumping when not on ground
        if self.flag_ground:
            if not self.key_jump:
                self.flag_allow_jump = True

        # Physics function
        self.handle_physics(dt)

        # Move player
        self.perform_speed_movement(dt)

        # Gravity - if player not on the ground!
        if not self.flag_ground: # or not self.perform_ground_test():
            self.perform_gravity_movement(dt)

        # Set the state each update so the right animations display
        self.calculate_state()

