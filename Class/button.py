import pygame

class Button : 
    def __init__(self, x, y, width, height, text, command) : 
        self.command = command

        # Button
        self.bg = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont(None, 25)
        self.btnText = self.font.render(text, True, (255, 255, 255))

    def update(self, mousePos) :
        if self.bg.collidepoint(mousePos):
            self.command()
    
    def render(self, display, color) :
        self.posRect = self.btnText.get_rect(center = (self.bg.x + self.bg.width/2, self.bg.y + self.bg.height/2))
        pygame.draw.rect(display, color, self.bg, border_radius= 15)
        display.blit(self.btnText, self.posRect)