import pygame
from Class.network import Network
from Class.player import Player
from Class.background import Background
from Class.hearth import Hearth
from Class.button import Button
from dotenv import dotenv_values
from functions import *

pygame.init()

# Load .env
CONFIG = dotenv_values()

# Create window
WIN = pygame.display.set_mode((int(CONFIG.get('WINDOW_WIDTH')), int(CONFIG.get('WINDOW_HEIGHT'))))

# ALL SPRITES
ALL_SPRITES = pygame.sprite.Group()

# Background
BG = Background('./assets/background/boat.png', [0, 0])

pygame.display.set_caption("Client")
FONT = pygame.font.SysFont(None, 25)
CLOCK = pygame.time.Clock()

def pause() :
    paused = True

    while paused is True:
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                quit.update(pygame.mouse.get_pos())
                paused = continu.update(pygame.mouse.get_pos())
        
        s = pygame.Surface((int(CONFIG.get('WINDOW_WIDTH')), int(CONFIG.get('WINDOW_HEIGHT'))))
        s.set_alpha(100)
        s.fill((255, 255, 255))
        WIN.blit(s, (0,0))
        

        message_to_screen("Jeu en pause", (0, 0, 0))
        quit = Button (100, 550, 300, 60, "Quitter", quit_game)
        continu = Button(650, 550, 300, 60, "Continuer", continue_game)

        quit.render(WIN, (200, 0, 0))
        continu.render(WIN, (0, 200, 0))

        pygame.display.update()
        CLOCK.tick(5)

def text_objects(text, color) :
    textSurface = FONT.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color):
    textSurf, textRect = text_objects(msg, color)
    textRect.center = (int(CONFIG.get('WINDOW_WIDTH'))/2), (int(CONFIG.get('WINDOW_HEIGHT'))/2)
    WIN.blit(textSurf, textRect)

# Redraw window with new values
def redrawWindow(win, player, player2):
    win.fill((0, 0, 0))
    win.blit(BG.image, BG.rect)
    ALL_SPRITES.draw(win)
    player.health_update(win)
    player2.health_update(win)
    if player.attacking:
        player.drawAttackHitbox(win)
    if player2.attacking:
        player2.drawAttackHitbox(win)
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

        if hearthCooldown > 0:
            hearthCooldown -= 1

        # Add hearth sprite
        if hearth:
            ALL_SPRITES.add([hearth])

        # Update all sprites
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
            
        p.move()

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
                p.get_damage(1)
                if p.hurting == True:
                    p.drawHurtAnimation()

        redrawWindow(WIN, p, p2)
        CLOCK.tick(60)

# Launch
main()