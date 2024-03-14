import pygame
import sys
from src.player import Player
from src.wall import Wall
from src.bullet import Bullet
from src.enemy import Enemy
from src.constants import BG_COLOR, LEVEL_1_WALLS

# Initialize Pygame
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Create player and enemy
player = Player()
enemy = Enemy()

# Create walls
walls = pygame.sprite.Group()
for wall_position in LEVEL_1_WALLS:
    walls.add(Wall(wall_position))

# Create data structure to keep track of bullets
bullets = pygame.sprite.Group()

# Main game loop
playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.add(Bullet(player.rect.x + 45, player.rect.y))

    # Update the positions of game objects
    player.update()
    enemy.update(bullets)
    bullets.update()

    # Check collisions between bullets and walls
    new_bullet_list = []
    coll_wall = pygame.sprite.groupcollide(
        bullets, walls, True, False)

    for bullet, hit_walls in coll_wall.items():
        for wall in hit_walls:
            bullets.remove(bullet)

    # Check collisions between bullets and the enemy
    coll_enemy = pygame.sprite.spritecollide(enemy, bullets, False)
    for x in coll_enemy:
        enemy.is_hit = True

    # Draw background before drawing foreground
    screen.fill(BG_COLOR)

    # Single sprites are drawn with screen.blit()
    screen.blit(player.current_sprite, (player.rect.x, player.rect.y))
    screen.blit(enemy.current_sprite, (enemy.rect.x, enemy.rect.y))

    # Groups of sprites can be drawn with group.draw()
    walls.draw(screen)
    bullets.draw(screen)

    # Draw the score to the screen
    state_text = font.render(f'État: {enemy.state}', True, (255, 0, 0))
    screen.blit(state_text, (10, 565))

    # Update screen
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
