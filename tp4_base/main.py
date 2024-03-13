import pygame
import sys
from src.player import Player
from src.wall import Wall
from src.bullet import Bullet

pygame.init()

# Define colors
BG_COLOR = (153, 178, 178)

# Initialize Pygame
bullets = []
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create entities
player = Player()
walls = pygame.sprite.Group()
wall1 = Wall(550, 150, 50, 200)
wall2 = Wall(100, 150, 100, 50)
walls.add(wall1, wall2)

# Main game loop
playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.rect.x + 45, player.rect.y))

    if len(bullets) > 5:
        bullets = bullets[1:5]
        print(len(bullets))
    else:
        print(len(bullets))

    # before player update
    previous_x = player.rect.x
    previous_y = player.rect.y

    # player update 
    player.update()

    # check for collisions between player and walls
    wall_collisions = pygame.sprite.spritecollide(player, walls, False)
    for wall_collision in wall_collisions:
        print("Collided")

        # fall back to previous position
        player.rect.x = previous_x
        player.rect.y = previous_y
        break

    # draw
    screen.fill(BG_COLOR)
    for bullet in bullets:
        bullet.update()
        screen.blit(bullet.image, (bullet.rect.x, bullet.rect.y))
    

    # single sprites are drawn with screen.blit()
    screen.blit(player.current_sprite, (player.rect.x, player.rect.y))

    # groups of sprites can be drawn with group.draw()
    walls.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()