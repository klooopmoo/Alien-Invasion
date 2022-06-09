import sys
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represnt a single alien in the fleet """
    def __init__(self, ai_settings, screen):
        """init the alien and set its starting position"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #load the alien image and set its react attribute
        self.image = pygame.image.load("images/bowser.bmp")
        self.rect = self.image.get_rect()

        # start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store the aliens exact location
        self.x = float(self.rect.x)



    def blitme(self):
        """draw the alien at its curreent lcoation """
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move alien to the right or left """
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x


    def check_edges(self):
        """Return true if alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


