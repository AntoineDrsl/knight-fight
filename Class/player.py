from json import load
import os
from posixpath import basename
from unittest.mock import patch
from dotenv import dotenv_values
import pygame

# Load .env
CONFIG = dotenv_values()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, side):

        pygame.sprite.Sprite.__init__(self)
        self.sprites = [pygame.image.load(os.path.join('assets/characters/current/movement', str(x) + '.png')) for x in range(1,13)]
        # SPRITE IMAGE
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        # SPRITE HITBOX        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.x = x
        self.y = y
        self.color = color
        self.vel = 5

        # Health
        self.current_health = int(CONFIG.get('DEFAULT_HEALTH'))
        self.max_health = int(CONFIG.get('DEFAULT_HEALTH'))
        self.health_bar_length = int(CONFIG.get('HEALTH_BAR_WIDTH'))
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_bar_x = int(CONFIG.get('HEALTH_BAR_RIGHT')) if side == 'left' else int(CONFIG.get('HEALTH_BAR_LEFT'))
        self.health_bar_y = int(CONFIG.get('HEALTH_BAR_TOP'))
    
    def move(self):
        keys = pygame.key.get_pressed()
           
        # Move
        if keys[pygame.K_RIGHT] and self.x < int(CONFIG.get('WINDOW_WIDTH')):
            self.x += self.vel
            self.current_sprite += 1
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel
            self.current_sprite += 1
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.vel
            self.current_sprite += 1
        if keys[pygame.K_DOWN] and self.y < int(CONFIG.get('WINDOW_HEIGHT')):
            self.y += self.vel
            self.current_sprite += 1

        self.update()

    def update(self):
        self.rect.center = (self.x, self.y)
        
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

    def get_damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0

    def get_health(self, amount):
        if self.current_health < self.max_health:
            self.current_health += amount
        if self.current_health >= self.max_health:
            self.current_health = self.max_health

    def basic_health(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.health_bar_x, self.health_bar_y, self.current_health / self.health_ratio, int(CONFIG.get('HEALTH_BAR_HEIGHT'))))