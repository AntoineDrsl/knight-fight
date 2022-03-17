import os
from dotenv import dotenv_values
import pygame

# Load .env
CONFIG = dotenv_values()

class Hearth(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # HEARTH SPRITE
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('assets/hearth.png')), (int(CONFIG.get('WINDOW_WIDTH')) / 15, int(CONFIG.get('WINDOW_HEIGHT')) / 15))

        # HEARTH POSITION
        self.x = x
        self.y = y

        # HEARTH HITBOX        
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def move(self):
        if(self.y <= int(CONFIG.get('GROUND_Y'))):
            self.y += 1
        self.rect.topleft = (self.x, self.y)

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (self.x, self.y)