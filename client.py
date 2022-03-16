import pygame
from Class.network import Network
from Class.player import Player
from dotenv import dotenv_values
from functions import *

# Load .env
CONFIG = dotenv_values()

# Create window
WIN = pygame.display.set_mode((int(CONFIG.get('WINDOW_WIDTH')), int(CONFIG.get('WINDOW_HEIGHT'))))
pygame.display.set_caption("Client")

# Redraw window with new values
def redrawWindow(win, player, player2):
    win.fill((0, 0, 0))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()

# Launch loop game
def main():
    run = True
    clock = pygame.time.Clock()
    # Create network get data
    n = Network()
    startPos = read_pos(n.getPos())
    startSide = n.getSide()
    opponentSide = 'right' if startSide == 'left' else 'left'
    # Create current player
    p = Player(startPos[0], startPos[1], (0, 255, 0), startSide)
    # Opponent
    p2 = Player(int(CONFIG.get('P2_DEFAULT_X')), int(CONFIG.get('P2_DEFAULT_Y')), (255, 0, 0), opponentSide)

    while run:
        # Send current user info and get opponent ones
        data = n.send({ 'position': make_pos((p.x, p.y)), 'health': p.current_health })
        # Update opponent
        p2Pos = read_pos(data['position'])
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.current_health = int(data['health'])
        p2.update()

        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Test
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    p.get_health(50)
                if event.key == pygame.K_q:
                    p.get_damage(50)
        
        p.move()
        redrawWindow(WIN, p, p2)
        clock.tick(60)

# Launch
main()