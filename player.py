# -------------------------------------------------------------------- #
# player.py
#   Player class
# -------------------------------------------------------------------- #

# Game library imports:
import pygame

# Local imports:
from constants import *
from sensor import Sensor
from spritesheet import SpriteSheet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # TODO: allow these to be defined by passing arguments when class instance is created

        # Physics constants:
        self.air = 0.09375
        self.jump_speed = 6.5
        self.top_speed = 6
        self.gravity = 0.21875
        self.acceleration = 0.5
        self.friction = 0.5

        # Variables:
        # air speed
        self.x_speed = 0
        self.y_speed = 0
        # ground speed
        self.ground_speed = 0
        # states
        self._state = STOPPED_STATE

        # Flags
        self.flag_ground = False
        self.flag_allow_jump = False
        self.flag_allow_horizontal_movement = True
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
        self.jump_frames = []
        self.stand_frames = []

        # Append all right walking frames
        for x in range(WALK_FRAMES_COUNT):
            image = player_sprites.get_image(x * FRAME_WIDTH + x * FRAME_SPACING,
                                             WALK_START_POS[1], FRAME_WIDTH, FRAME_HEIGHT)
            self.walk_frames.append(image)

        for x in range(STAND_FRAMES_COUNT):
            image = player_sprites.get_image(x * FRAME_WIDTH + x * FRAME_SPACING,
                                             STAND_START_POS[1], FRAME_WIDTH, FRAME_HEIGHT)
            self.stand_frames.append(image)

        # A dictionary of the various animations that correspond to Sonic's various states.
        self.animations = {
            WALKING_STATE: self.walk_frames,
            JUMPING_STATE: self.jump_frames,
            STOPPED_STATE: self.stand_frames
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

        # Control lock timers
        self.hlock = 0

    # Change sonic to a different state and reset the animation for the new state
    def change_state(self, state):
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

    def set_hlock(self, frames):
        self.hlock = frames
        self.flag_allow_horizontal_movement = False

    def update_lock_timers(self, dt):
        if self.hlock > 0:
            # TODO: might need to change use of FPS constant once I program in variable FPS.
            self.hlock = max(self.hlock - 60 * dt, 0)
        if self.hlock == 0:
            self.flag_allow_horizontal_movement = True

    def handle_physics(self):
        # flags are turned on each step (60 steps per second)
        if self.flag_allow_horizontal_movement:
            self.advance_animation()
            # Right movement
            if self.key_right:
                if self.flag_ground:
                    self.ground_speed += self.acceleration
                # Limit ground_speed by top_speed
                if self.ground_speed > self.top_speed:
                    self.ground_speed = self.top_speed
            # Left movement
            elif self.key_left:
                if self.flag_ground:
                    self.ground_speed -= self.acceleration
                # Limit ground_speed by negative top_speed
                if self.ground_speed < - self.top_speed:
                    self.ground_speed = - self.top_speed

            elif not self.key_left and not self.key_right and self.flag_ground:
                if self.ground_speed > 0:
                    self.ground_speed -= self.friction
                elif self.ground_speed < 0:
                    self.ground_speed += self.friction

    def calculate_state(self):
        if self.flag_ground:
            if self.ground_speed == 0:
                self.change_state(STOPPED_STATE)
            elif self.ground_speed > 0 or self.ground_speed < 0:
                self.change_state(WALKING_STATE)
            elif self.ground_speed > 6 or self.ground_speed < -6:
                self.change_state(RUNNING_STATE)
            elif self.ground_speed > 10 or self.ground_speed < -10:
                self.change_state(DASHING_STATE)

    # TODO: set_gravity()
    def set_gravity(self):
        pass

    def key_press(self, event, pressed_keys):
        if event.key == pygame.K_a:
            print("Player input: A")
            self.key_left = True
        elif event.key == pygame.K_d:
            print("Player input: D")
            self.key_right = True

    def key_release(self, event, pressed_keys):
        if event.key == pygame.K_a:
            print("Player input: A")
            self.key_left = False
        elif event.key == pygame.K_d:
            print("Player input: D")
            self.key_right = False

    def update(self, dt):
        # Timing of animations, physics, etc.
        self.update_lock_timers(dt)

        # Physics
        self.handle_physics()

        # TODO: why are gsp and xsp different variables? How do we integrate them into self.rect.x?
        self.rect.x += self.ground_speed
        self.rect.y += self.y_speed

        # Set image to current frame in animation sequence
        self.image = self.animations.get(self._state)[self.frame_index]

        # Update the sensors to player's new position
        for sensor in self.sensors:
            sensor.update(self.rect)

        # Set player state
        self.calculate_state()