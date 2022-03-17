import pygame
from dotenv import dotenv_values
from Class.button import Button
from Class.background import Background
from functions import *

# Load .env
CONFIG = dotenv_values()

# Background
BG_PAUSE = Background('./assets/background/underwater.jpeg', [-500, -750])
BG_WIN = Background('./assets/background/victory.jpeg', [0, 0])
pygame.font.init()
FONT = pygame.font.SysFont(None, 70)

# Pause window
def pause(window) :
    paused = True
    while paused is True:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE : 
                    paused = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                quit.update(pygame.mouse.get_pos())
                paused = continu.update(pygame.mouse.get_pos())
        
        # Display window
        s = pygame.Surface((int(CONFIG.get('WINDOW_WIDTH')), int(CONFIG.get('WINDOW_HEIGHT'))))
        s.fill((255, 255, 255))
        s.blit(BG_PAUSE.image, BG_PAUSE.rect)
        window.blit(s, (0, 0))
        message_to_screen("Jeu en pause", (0, 0, 0), window)

        # Buttons
        quit = Button (100, 550, 300, 60, "Quitter", quit_game)
        continu = Button(650, 550, 300, 60, "Continuer", continue_game)
        quit.render(window, (200, 0, 0))
        continu.render(window, (0, 200, 0))

        pygame.display.update()

# Lose window
def lose(window) :
    lose = True
    while lose is True:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE : 
                    quit_game()

        # Display window
        window.fill((0, 0, 0))
        message_to_screen("Game Over !", (255, 255, 255), window)

        pygame.display.update()

# Win window
def win(window):
    win = True
    while win is True:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE : 
                    quit_game()

        # Display window
        s = pygame.Surface((int(CONFIG.get('WINDOW_WIDTH')), int(CONFIG.get('WINDOW_HEIGHT'))))
        s.set_alpha(100)
        s.fill((255, 255, 255))
        s.blit(BG_WIN.image, BG_WIN.rect)
        window.blit(s, (0,0))
        message_to_screen("Victory !", (255, 255, 255), window)

        pygame.display.update()

# Add message to screen
def message_to_screen(msg, color, window):
    textSurf, textRect = text_objects(msg, color)
    textRect.center = (int(CONFIG.get('WINDOW_WIDTH'))/2), (int(CONFIG.get('WINDOW_HEIGHT'))/2)
    window.blit(textSurf, textRect)

# Make text object
def text_objects(text, color):
    textSurface = FONT.render(text, True, color)
    return textSurface, textSurface.get_rect()