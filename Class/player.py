from json import load
import os
from posixpath import basename
from traceback import print_tb
from unittest.mock import patch
from dotenv import dotenv_values
import pygame

# Load .env
CONFIG = dotenv_values()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, side, direction):

        pygame.sprite.Sprite.__init__(self)
        if side == 'right': 
            self.sprites = [pygame.image.load(os.path.join('assets/characters/current/movement', str(x) + '.png')) for x in range(1,13)]
            self.sprites_attack = [pygame.image.load(os.path.join('assets/characters/current/attack', str(x) + '.png')) for x in range(1,13)]
        else: 
            self.sprites = [pygame.image.load(os.path.join('assets/characters/opponent/movement', str(x) + '.png')) for x in range(1,13)]
            self.sprites_attack = [pygame.image.load(os.path.join('assets/characters/opponent/attack', str(x) + '.png')) for x in range(1,13)]
            
        # SPRITE IMAGE
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.attacking = False
        self.counter_attack = 0

        # SPRITE HITBOX        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # ATTACK HITBOX
        self.attackHitbox = None

        # MOVE
        self.x = x
        self.y = y
        self.direction = direction
        self.vel = 5

        # Jump
        self.isJump = False
        self.jumpCount = int(CONFIG.get('DEFAULT_JUMP'))

        # Health bar
        self.health_bar_length = int(CONFIG.get('HEALTH_BAR_WIDTH'))
        self.health_bar_height = int(CONFIG.get('HEALTH_BAR_HEIGHT'))
        self.health_bar_border = int(CONFIG.get('HEALTH_BAR_BORDER'))
        self.health_bar_x = int(CONFIG.get('HEALTH_BAR_RIGHT')) if side == 'left' else int(CONFIG.get('HEALTH_BAR_LEFT'))
        self.health_bar_y = int(CONFIG.get('HEALTH_BAR_TOP'))

        # Health
        self.current_health = int(CONFIG.get('DEFAULT_HEALTH'))
        self.max_health = int(CONFIG.get('DEFAULT_HEALTH'))
        self.health_ratio = self.max_health / self.health_bar_length
    
    def move(self):
        keys = pygame.key.get_pressed()
           
        # Move
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x < int(CONFIG.get('WINDOW_WIDTH')):
            self.x += self.vel
            self.direction = 'right'
            self.current_sprite += 1
        if (keys[pygame.K_LEFT] or keys[pygame.K_q]) and self.x > 0:
            self.x -= self.vel
            self.direction = 'left'
            self.current_sprite += 1
        
        if keys[pygame.K_e]:
            if self.attacking == False:
                self.attacking = True
            
        # Jump
        if not self.isJump:
            if (keys[pygame.K_SPACE] or keys[pygame.K_z]):
                self.isJump = True
        else:
            if self.jumpCount >= (int(CONFIG.get('DEFAULT_JUMP')) * -1):
                # When jumping
                self.y -= round((self.jumpCount * abs(self.jumpCount)) * 0.5)
                self.jumpCount -= 1
                self.current_sprite += 1
            else:
                # When jump finish
                self.jumpCount = 10
                self.isJump = False

        self.update()

    def update(self):
        # Update sprite
        self.rect.center = (self.x, self.y)

        # Update sprite image
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        # Update sprite direction
        self.image = pygame.transform.flip(self.image, True if self.direction == 'left' else False, False)

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

    def health_update(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.health_bar_x, self.health_bar_y, self.current_health / self.health_ratio, self.health_bar_height))
        pygame.draw.rect(win, (255, 255, 255), (self.health_bar_x, self.health_bar_y, self.health_bar_length, self.health_bar_height), self.health_bar_border)

    def attack(self, win):
        # Attack animation
        if self.counter_attack >= len(self.sprites_attack):
            self.counter_attack = 0
            self.attacking = False
        self.image = pygame.transform.flip(self.sprites_attack[self.counter_attack], True if self.direction == 'left' else False, False)
        self.counter_attack += 1

    def drawAttackHitbox(self, win):
        # Attack hitbox
        hitbox_x = (self.x + int(CONFIG.get('HITBOX_X_RIGHT'))) if self.direction == 'right' else (self.x - int(CONFIG.get('HITBOX_X_LEFT')))
        self.attackHitbox = pygame.draw.rect(win, (255, 0, 0), (hitbox_x, self.y - int(CONFIG.get('HITBOX_Y')), int(CONFIG.get('HITBOX_WIDTH')), int(CONFIG.get('HITBOX_HEIGHT'))))