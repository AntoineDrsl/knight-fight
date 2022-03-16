import pygame
from Class.network import Network
from Class.player import Player
from Class.background import Background
from dotenv import dotenv_values
from functions import *

pygame.init()

# Load .env
CONFIG = dotenv_values()

# Create window
WIN = pygame.display.set_mode((int(CONFIG.get('WINDOW_WIDTH')), int(CONFIG.get('WINDOW_HEIGHT'))))

# ALL SPRITES
ALL_SPRITES = pygame.sprite.Group()

bg = Background('./assets/background/boat.png', [0, 0])
pygame.display.set_caption("Client")


font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()

def pause() :
    paused = True

    while paused is True:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE:
                    paused = False
                elif event.key == pygame.K_q :
                    pygame.quit()
                    quit()
        WIN.fill((255, 255, 255, 100))

        message_to_screen("Jeu en pause", (0, 0, 0, 100))

        pygame.display.update()
        clock.tick(5)


def text_objects(text, color) :
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color):
    textSurf, textRect = text_objects(msg, color)
    textRect.center = (int(CONFIG.get('WINDOW_WIDTH'))/2), (int(CONFIG.get('WINDOW_HEIGHT'))/2)
    WIN.blit(textSurf, textRect)

# Redraw window with new values
def redrawWindow(win, player, player2):
    win.fill((0, 0, 0))
    win.blit(bg.image, bg.rect)
    ALL_SPRITES.draw(win)
    player.health_update(win)
    player2.health_update(win)
    pygame.display.update()

# Launch loop game
def main():
    run = True
    # Current player
    n = Network()
    startPos = read_pos(n.getPos())
    startSide = n.getSide()
    opponentSide = 'right' if startSide == 'left' else 'left'
    # Create current player
    p = Player(startPos[0], startPos[1], (0, 255, 0), startSide)
    # Opponent
    p2 = Player(int(CONFIG.get('P2_DEFAULT_X')), int(CONFIG.get('P2_DEFAULT_Y')), (255, 0, 0), opponentSide)

    # ADD SPRITE TO THE LIST
    ALL_SPRITES.add([p, p2])

    while run:
        # Send current user info and get opponent ones
        data = n.send({ 'position': make_pos((p.x, p.y)), 'health': p.current_health })
        # Update opponent
        p2Pos = read_pos(data['position'])
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.current_health = int(data['health'])
        
        ALL_SPRITES.update()

        for event in pygame.event.get():
                
            # Quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Test
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE : 
                    pause()
                if event.key == pygame.K_a:
                    p.get_health(50)
                if event.key == pygame.K_q:
                    p.get_damage(50)
        
        p.move()
        redrawWindow(WIN, p, p2)
        clock.tick(60)

# Launch
main()