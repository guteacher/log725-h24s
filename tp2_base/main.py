import pygame
import sys
from src.player import Player
from src.wall import Wall

pygame.init()

# Define colors
BG_COLOR = (153, 178, 178)

# Initialize Pygame
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create entities
player = Player()
walls = pygame.sprite.Group()
wall1 = Wall(500, 150, 50, 200)
wall2 = Wall(250, 50, 100, 50)
walls.add(wall1, wall2)

# Main game loop
playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

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

    # single sprites are drawn with screen.blit()
    screen.blit(player.image, (player.rect.x, player.rect.y))

    # groups of sprites can be drawn with group.draw()
    walls.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()