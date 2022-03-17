from json import load
import os
from pickle import TRUE
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
            self.sprites = [pygame.image.load(os.path.join('assets/characters/current/movement', str(x) + '.png')) for x in range(1,18)]
            self.sprites_attack = [pygame.image.load(os.path.join('assets/characters/current/attack', str(x) + '.png')) for x in range(1,13)]
            self.sprites_hurt = [pygame.image.load(os.path.join('assets/characters/current/hurt', str(x) + '.png')) for x in range(1,13)]
        else: 
            self.sprites = [pygame.image.load(os.path.join('assets/characters/opponent/movement', str(x) + '.png')) for x in range(1,18)]
            self.sprites_attack = [pygame.image.load(os.path.join('assets/characters/opponent/attack', str(x) + '.png')) for x in range(1,13)]
            self.sprites_hurt = [pygame.image.load(os.path.join('assets/characters/opponent/hurt', str(x) + '.png')) for x in range(1,13)]

        # SPRITE IMAGE
        self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (int(CONFIG.get('WINDOW_WIDTH')) / 5, int(CONFIG.get('WINDOW_HEIGHT')) / 5))
        self.attacking = False
        self.counter_attack = 0
        # HURT COUNTER
        self.counter_hurt = 0
        self.hurting = False

        # SPRITE HITBOX        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.hitbox = pygame.Rect(x + 90, y + 30, 40, 90)

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

        # Sound
        self.pain = pygame.mixer.Sound(os.path.join('assets/characters/sounds', 'pain.wav'))
        self.slash = pygame.mixer.Sound(os.path.join('assets/characters/sounds', 'slash.wav'))
    
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
        
        # Attack
        if keys[pygame.K_e]:
            if self.attacking == False:
                self.attacking = True
            self.slash.play()

        # Sprint
        if keys[pygame.K_LSHIFT]:
            self.vel = 10
        else:
            self.vel = 5
            
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
        self.rect.topleft = (self.x, self.y)
        self.hitbox = pygame.Rect(self.x + 90, self.y + 30, 40, 90)

        # Update sprite image
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites[self.current_sprite], (int(CONFIG.get('WINDOW_WIDTH')) / 5, int(CONFIG.get('WINDOW_HEIGHT')) / 5))

        # Update sprite direction
        self.image = pygame.transform.flip(self.image, True if self.direction == 'left' else False, False)

    def get_damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0

        if self.hurting == False:
            self.hurting = True

    def get_health(self, amount):
        if self.current_health < self.max_health:
            self.current_health += amount
        if self.current_health >= self.max_health:
            self.current_health = self.max_health

    def health_update(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.health_bar_x, self.health_bar_y, self.current_health / self.health_ratio, self.health_bar_height))
        pygame.draw.rect(win, (255, 255, 255), (self.health_bar_x, self.health_bar_y, self.health_bar_length, self.health_bar_height), self.health_bar_border)

        # Test - Draw hitbox
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox)

    def attack(self):
        # Attack animation
        if self.counter_attack >= len(self.sprites_attack):
            self.counter_attack = 0
            self.attacking = False
        self.image = pygame.transform.flip(self.sprites_attack[self.counter_attack], True if self.direction == 'left' else False, False)
        self.image = pygame.transform.scale(self.image, (int(CONFIG.get('WINDOW_WIDTH')) / 5, int(CONFIG.get('WINDOW_HEIGHT')) / 5))
        self.counter_attack += 1

    def drawAttackHitbox(self, win):
        # Attack hitbox
        hitbox_x = (self.x + int(CONFIG.get('HITBOX_X_RIGHT'))) if self.direction == 'right' else (self.x - int(CONFIG.get('HITBOX_X_LEFT')))
        self.attackHitbox = pygame.Rect(hitbox_x, self.y - int(CONFIG.get('HITBOX_Y')), int(CONFIG.get('HITBOX_WIDTH')), int(CONFIG.get('HITBOX_HEIGHT')))

        # TEST - Draw attack hitbox
        # pygame.draw.rect(win, (255, 0, 0), self.attackHitbox)

    def drawHurtAnimation(self):
        # Hurt animation
        if self.counter_hurt >= len(self.sprites_hurt):
            self.counter_hurt = 0
            self.attacking = False
        self.image = pygame.transform.flip(self.sprites_hurt[self.counter_hurt], True if self.direction == 'left' else False, False)
        self.image = pygame.transform.scale(self.image, (int(CONFIG.get('WINDOW_WIDTH')) / 5, int(CONFIG.get('WINDOW_HEIGHT')) / 5))
        self.counter_hurt += 1
        self.pain.play()