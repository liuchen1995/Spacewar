import pygame
from pygame.sprite import Sprite

class Life(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the cat, and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the cat image, and get its rect.
        self.image = pygame.image.load('gfx/SpaceShip.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
