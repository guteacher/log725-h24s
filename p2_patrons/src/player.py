import pygame
import math
from src.constants import CURRENT_W, CURRENT_H, JUMP_SOUND
from src.extracter import Extracter


class Player(pygame.sprite.Sprite):
    PERCENT_OF_SCREEN_HEIGHT = 0.1296296296296296
    ANIMATION_SPEED = 4   # frames before updating the running or idle animation frame
    change_animation = 2

    facing_right = True
    on_ground = True
    idle_index = 1
    running_index = 0
    speed = [0, 0]

    animation_frame = 'idle'
    IDLE_PATH = 'assets/sprites/idle.png'
    JUMP_PATH = 'assets/sprites/jump.png'
    LANDING_PATH = 'assets/sprites/landing.png'
    MID_AIR_PATH = 'assets/sprites/mid air.png'
    RUN_PATH = 'assets/sprites/run.png'
    extracter = Extracter()

    RUNNING_SPEED = round(CURRENT_W / 200)  # pixels / (1/60) seconds
    JUMP_SPEED = round(CURRENT_H / -40.5)   # pixels / (1/60) seconds
    GRAVITY_CONSTANT = -0.05 * JUMP_SPEED
    # NOTE: 35 is the idle height for outline, 34 is for no outline
    scale_factor = CURRENT_H * PERCENT_OF_SCREEN_HEIGHT / 34
    idle_images = [[], []]  # left, right
    # 21 with outline, 19 without
    for image in extracter.extract_images(IDLE_PATH, 19, scale_factor):
        idle_images[0].append(pygame.transform.flip(image, True, False))
        idle_images[1].append(image)

    jump_image = pygame.image.load(JUMP_PATH).convert_alpha()
    jump_image = extracter.scale_image(jump_image, scale_factor)
    jump_images = [pygame.transform.flip(jump_image, True, False), jump_image]

    landing_image = pygame.image.load(LANDING_PATH).convert_alpha()
    landing_image = extracter.scale_image(landing_image, scale_factor)
    landing_images = [pygame.transform.flip(
        landing_image, True, False), landing_image]

    mid_air_images = [[], []]  # left, right
    # 22 with outline , 20 without
    for image in extracter.extract_images(MID_AIR_PATH, 20, scale_factor):
        # image = pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert_alpha()
        mid_air_images[0].append(pygame.transform.flip(image, True, False))
        mid_air_images[1].append(image)

    run_images = [[], []]  # left, right
    # 23 with outline, 21 without
    for image in extracter.extract_images(RUN_PATH, 21, scale_factor):
        run_images[0].append(pygame.transform.flip(image, True, False))
        run_images[1].append(image)
    # first percent is the grass percent of the tile (3/TILE_SIDELENGTH)
    # second percent is the percent of screen height for a tile
    GROUND_ADJUSTMENT = math.ceil(
        0.1111111111111111 * 0.07901234567901234 * CURRENT_H)

    def __init__(self, world):
        super(Player, self).__init__()

        self.world = world
        self.image: pygame.Surface = self.idle_images[1][0]
        self.rect: pygame.Rect = self.image.get_rect()
        collide_width = self.rect.width - 8 * self.scale_factor
        self.collide_rect: pygame.Rect = pygame.rect.Rect(
            (0, 0), (collide_width, self.rect.height))
        self.rect.left = 0.05 * CURRENT_W

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def reset_change_animation(self):
        self.change_animation = self.ANIMATION_SPEED

    def get_image(self, images: list, index: int = None) -> pygame.image:
        """
        gets an image from a list of right images and left images according to direction player is facing
        :param images: list containing a right facing image(s) [0] and left facing image(s) [1]
        :param index: index of the image to return. if equal to None, images does not contain lists
        :return: the image of proper facing direction
        """
        if index is None:
            return images[self.facing_right]
        return images[self.facing_right][index]

    def update_idle(self):
        """
        Updates the idle animation
        """
        if self.change_animation <= 0:
            self.image = self.get_image(self.idle_images, self.idle_index)
            self.idle_index += 1
            if self.idle_index >= len(self.idle_images[0]):
                self.idle_index = 0
            self.reset_change_animation()
        else:
            self.change_animation -= 1

    def update_running(self):
        """
        Updates the running animations
        """
        if self.change_animation <= 0:
            self.image = self.get_image(self.run_images, self.running_index)
            self.running_index += 1
            if self.running_index >= len(self.run_images[0]):
                self.running_index = 0
            self.reset_change_animation()
        else:
            self.change_animation -= 1

    def is_on_ground(self):
        return self.on_ground

    def get_facing_side(self):
        return 1 if self.facing_right else 0

    def gravity(self):
        self.on_ground = False
        for platform in pygame.sprite.spritecollide(self, self.world.platform_list, False):
            if self.rect.bottom == platform.rect.top + self.GROUND_ADJUSTMENT:
                self.on_ground = True
                break
        if not self.on_ground:
            self.speed[1] += self.GRAVITY_CONSTANT
            if self.speed[1] > 0 and self.animation_frame != f'mid-air down {self.facing_right}':
                self.image = self.get_image(self.mid_air_images, 1)
                self.animation_frame = f'mid-air down {self.facing_right}'
            elif 0 > self.speed[1] >= -12 and self.animation_frame != f'mid-air up {self.facing_right}':
                self.image = self.get_image(self.mid_air_images, 0)
                self.animation_frame = f'mid-air up {self.facing_right}'

    def update(self, seconds_passed=1/60):
        self.gravity()
        self.rect.y += self.speed[1]

        platform_hit_list = pygame.sprite.spritecollide(
            self, self.world.platform_list, False)  # detect collisions

        for platform in platform_hit_list:
            if self.speed[1] > 0 and self.rect.bottom > platform.rect.top + self.GROUND_ADJUSTMENT:  # going down
                self.rect.bottom = platform.rect.top + self.GROUND_ADJUSTMENT
                self.speed[1] = 0
            elif self.speed[1] < 0 and platform.rect.top < self.rect.top < platform.rect.bottom:  # going up
                self.rect.top = platform.rect.bottom
                self.speed[1] = 0

        self.rect.x += self.speed[0]
        platform_hit_list = pygame.sprite.spritecollide(
            self, self.world.platform_list, False)  # detect collisions
        for platform in platform_hit_list:
            if (self.speed[0] > 0 and
                    platform.rect.left < self.rect.right and
                    platform.rect.top + self.GROUND_ADJUSTMENT < self.rect.bottom):
                self.rect.right = platform.rect.left  # going right
            elif (self.speed[0] < 0 and
                  platform.rect.right > self.rect.left and
                  platform.rect.top + self.GROUND_ADJUSTMENT < self.rect.bottom):
                self.rect.left = platform.rect.right  # going left
        # if self.speed == [0, 0] and will_land and self.ON_GROUND:  # if standing still
        if self.speed == [0, 0]:  # if standing still
            self.update_idle()
            self.animation_frame = 'idle'
        # animate only if running on the ground
        elif self.speed[0] != 0 and self.on_ground:
            self.update_running()
            self.animation_frame = 'running'
        return self.rect

    def stop(self, pressed_keys):

        if self.speed[0] == 0:
            # if right keys are still pressed
            if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
                self.speed[0] += self.RUNNING_SPEED
            # if left keys are still pressed
            if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
                self.speed[0] -= self.RUNNING_SPEED
            if self.speed[0] > 0:
                self.facing_right = True
            elif self.speed[0] < 0:
                self.facing_right = False

        elif (pressed_keys[pygame.K_LEFT] + pressed_keys[pygame.K_a] +
              pressed_keys[pygame.K_RIGHT] + pressed_keys[pygame.K_d] == 0):
            if self.on_ground:
                self.image = self.get_image(self.idle_images, True)
            self.speed[0] = 0

    def force_stop(self):
        self.speed = [0, 0]

    def go_left(self):
        if self.speed[0] > -self.RUNNING_SPEED:
            self.speed[0] -= self.RUNNING_SPEED
        self.facing_right = False

    def go_right(self):
        if self.speed[0] < self.RUNNING_SPEED:
            self.speed[0] += self.RUNNING_SPEED
        self.facing_right = True

    def jump(self, play_jump_sound: bool):
        """ Called when user hits 'jump' button. """
        #  player can jump to a height of two platforms
        if self.on_ground:
            if play_jump_sound:
                pygame.mixer.Channel(1).play(JUMP_SOUND)
            self.image = self.get_image(self.jump_images)
            # self.image = pygame.transform.flip(self.jump_frame, self.FACING_LEFT, False)
            self.speed[1] = self.JUMP_SPEED
            self.on_ground = False
            self.animation_frame = 'jump'

    def update_rect(self):
        pos = self.rect.bottomleft
        self.rect: pygame.Rect = self.image.get_rect()
        collide_width = self.rect.width - 8 * self.scale_factor
        self.rect.bottomleft = pos
        self.collide_rect: pygame.Rect = pygame.rect.Rect(
            (0, 0), (collide_width, self.rect.height))
        self.collide_rect.midbottom = self.rect.midbottom
