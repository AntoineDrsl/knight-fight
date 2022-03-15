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
    # Current player
    n = Network()
    startPos = read_pos(n.getPos())
    p = Player(startPos[0], startPos[1], (0, 255, 0), 'left')
    # Opponent
    p2 = Player(int(CONFIG.get('P2_DEFAULT_X')), int(CONFIG.get('P2_DEFAULT_Y')), (255, 0, 0), 'right')

    while run:
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
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