import pygame
from Class.network import Network
from Class.player import Player
from Class.hearth import Hearth
from dotenv import dotenv_values
from functions import *
from interface import *

pygame.init()

# Load .env
CONFIG = dotenv_values()

# Create window
WIN = pygame.display.set_mode((int(CONFIG.get('WINDOW_WIDTH')), int(CONFIG.get('WINDOW_HEIGHT'))))
pygame.display.set_caption("Client")
CLOCK = pygame.time.Clock()

# ALL SPRITES
BG = Background('./assets/background/boat.png', [0, 0])
ALL_SPRITES = pygame.sprite.Group()

# Redraw window with new values
def redrawWindow(win, player, player2):
    # Make background
    win.blit(BG.image, BG.rect)
    # Update healthes
    player.health_update(win)
    player2.health_update(win)
    # Create hitboxes
    if player.attacking:
        player.drawAttackHitbox(win)
    if player2.attacking:
        player2.drawAttackHitbox(win)
    # Update sprites
    ALL_SPRITES.draw(win)
    pygame.display.update()

# Launch loop game
def main():
    run = True
    # Current player data
    n = Network()
    startPos = read_pos(n.getPos())
    startSide = n.getSide()
    opponentSide = 'right' if startSide == 'left' else 'left'
    startDirection = n.getDirection()
    opponentDirection = 'right' if startDirection == 'left' else 'left'
    # Create current player
    p = Player(startPos[0], startPos[1], startSide, startDirection)
    # Create opponent
    p2 = Player(int(CONFIG.get('P2_DEFAULT_X')), int(CONFIG.get('P2_DEFAULT_Y')), opponentSide, opponentDirection)
    # Hearth
    hearth = False
    hearthCooldown = 0

    # Add sprites to the list
    ALL_SPRITES.add([p, p2])

    while run:
        ### OPPONENT ###

        # Send current user info and get opponent ones
        data = n.send({ 
            'position': make_pos((p.x, p.y)), 
            'health': p.current_health, 
            'direction': p.direction, 
            'attacking': p.attacking, 
            'hearth': make_pos((hearth.x, hearth.y)) if hearth else False
        })

        # Update opponent
        p2Pos = read_pos(data['position'])
        if(p2.x != p2Pos[0] or p2.y != p2Pos[1]):
            p2.current_sprite += 1
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.current_health = int(data['health'])
        p2.direction = data['direction']

        ### HEARTH ###

        # Get hearth position from server
        hearthPos = read_pos(data['hearth'])
        if hearth:
            hearth.setPosition(hearthPos[0], hearthPos[1])
        else:
            hearth = Hearth(hearthPos[0], hearthPos[1])

        # Check hearth collision
        if hearthCooldown == 0 and hearth.rect.colliderect(p.hitbox):
            p.get_health(50)
            ALL_SPRITES.remove(hearth)
            hearth = False
            hearthCooldown = int(CONFIG.get('HEARTH_COOLDOWN'))

        # Pass hearth cooldown
        if hearthCooldown > 0:
            hearthCooldown -= 1

        # Add hearth sprite
        if hearth:
            ALL_SPRITES.add([hearth])

        # Update all sprites
        ALL_SPRITES.update()

        # Update current user
        p.move()

        ### Attack ###

        # Current player attacking
        if p.attacking == True:
            # Play animation
            p.attack()
            if p.attackHitbox and p.attackHitbox.colliderect(p2.hitbox):
                p2.hurting = True
                if p2.hurting == True:
                    p2.drawHurtAnimation()

        # Opponent attacking
        if data['attacking']:
            # Play animation
            p2.attacking = True
            p2.attack()
            # Take damage if collision
            if p2.attackHitbox and p2.attackHitbox.colliderect(p.hitbox):
                p.get_damage(p.damage)
                if p.hurting == True:
                    p.drawHurtAnimation()

        ### INTERFACE ###
        if p.current_health <= 0:
            lose(WIN)
        elif p2.current_health <= 1:
            win(WIN)

        ### EVENTS ###

        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                # Pause
                if event.key == pygame.K_ESCAPE : 
                    pause(WIN)

        # Update window
        redrawWindow(WIN, p, p2)
        CLOCK.tick(60)

# Launch
main()