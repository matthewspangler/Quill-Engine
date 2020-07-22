import pygame

from constants import *
from game import GameScene
from scene import Scene


class TitleScene(Scene):
    def __init__(self, ):
        Scene.__init__(self)

    def events(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter
                self.change_scene(GameScene())

    def update(self, clock_tick):
        pass

    def draw(self, screen, surface):
        # Screen background color
        screen.fill(TITLE_BG_COLOR)

        # Make large font
        largeTitleFont = pygame.font.Font(TITLE_FONT, 40)

        # Make small font
        smallTitleFont = pygame.font.Font(TITLE_FONT, 30)

        # Create instances of text
        titleText = largeTitleFont.render('Platformer Engine Test', False, WHITE)
        subtitleText = smallTitleFont.render('Press enter to play!', False, WHITE)

        # Render the text
        screen.blit(titleText, (50, 0))
        screen.blit(subtitleText, (50, 200))
