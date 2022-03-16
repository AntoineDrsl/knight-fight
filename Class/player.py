from dotenv import dotenv_values
import pygame

# Load .env
CONFIG = dotenv_values()

class Player():
    def __init__(self, x, y, color, side):
        self.x = x
        self.y = y
        self.radius = int(CONFIG.get('DEFAULT_RADIUS'))
        self.color = color
        self.vel = 5
        self.circle = (self.x, self.y)
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
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, self.circle, self.radius)
        self.basic_health(win)

    def move(self):
        keys = pygame.key.get_pressed()
        
        # Move
        if keys[pygame.K_RIGHT] and self.x < int(CONFIG.get('WINDOW_WIDTH')):
            self.x += self.vel
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel

        # Jump
        if not self.isJump:
            if keys[pygame.K_SPACE]:
                self.isJump = True
        else:
            if self.jumpCount >= (int(CONFIG.get('DEFAULT_JUMP')) * -1):
                # When jumping
                self.y -= round((self.jumpCount * abs(self.jumpCount)) * 0.5)
                self.jumpCount -= 1
            else:
                # When jump finish
                self.jumpCount = 10
                self.isJump = False

        self.update()

    def update(self):
        self.circle = (self.x, self.y)

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
        pygame.draw.rect(win, (255, 0, 0), (self.health_bar_x, self.health_bar_y, self.current_health / self.health_ratio, self.health_bar_height))
        pygame.draw.rect(win, (255, 255, 255), (self.health_bar_x, self.health_bar_y, self.health_bar_length, self.health_bar_height), self.health_bar_border)