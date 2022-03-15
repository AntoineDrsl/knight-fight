from dotenv import dotenv_values
import pygame

# Load .env
CONFIG = dotenv_values()

class Player():
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 5
        self.circle = (self.x, self.y)

        # Health
        self.current_health = int(CONFIG.get('DEFAULT_HEALTH'))
        self.max_health = int(CONFIG.get('DEFAULT_HEALTH'))
        self.health_bar_length = int(CONFIG.get('HEALTH_BAR_LENGTH'))
        self.health_ratio = self.max_health / self.health_bar_length
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, self.circle, self.radius)

    def move(self):
        keys = pygame.key.get_pressed()
        
        # Move
        if keys[pygame.K_RIGHT] and self.x < int(CONFIG.get('WINDOW_WIDTH')):
            self.x += self.vel
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y < int(CONFIG.get('WINDOW_HEIGHT')):
            self.y += self.vel

        self.update()

    def update(self):
        self.circle = (self.x, self.y)

    def get_damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0

    def get_damage(self, amount):
        if self.current_health < self.max_health:
            self.current_health += amount
        if self.current_health >= self.max_health:
            self.current_health = self.max_health