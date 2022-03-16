import pygame
from Class.network import Network
from Class.player import Player
from dotenv import dotenv_values
from functions import *

# Load .env
CONFIG = dotenv_values()

# Create window
WIN = pygame.display.set_mode((int(CONFIG.get('WINDOW_WIDTH')), int(CONFIG.get('WINDOW_HEIGHT'))))

# ALL SPRITES
ALL_SPRITES = pygame.sprite.Group()

pygame.display.set_caption("Client")

# Redraw window with new values
def redrawWindow(win, player, player2):
    win.fill((0, 0, 0))
    # player.draw(win) # DEPRACTED ?
    # player2.draw(win) # DEPRACTED ?
    ALL_SPRITES.draw(win)
    pygame.display.update()

# Launch loop game
def main():
    run = True
    clock = pygame.time.Clock()
    # Create network for player
    n = Network()
    startPos = read_pos(n.getPos())
    # Create current player
    p = Player(startPos[0], startPos[1], (0, 255, 0), 'left')
    # Opponent
    p2 = Player(int(CONFIG.get('P2_DEFAULT_X')), int(CONFIG.get('P2_DEFAULT_Y')), (255, 0, 0), 'right')

    # ADD SPRITE TO THE LIST
    ALL_SPRITES.add([p, p2])

    while run:
        # Send current user position and get opponent position
        data = n.send({ 'position': make_pos((p.x, p.y)) })
        p2Pos = read_pos(data['position'])
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]

        ALL_SPRITES.update()

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