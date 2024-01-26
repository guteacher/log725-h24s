import pygame
from pygame import gfxdraw, K_w, K_a, K_d, K_UP, K_LEFT, K_RIGHT, K_ESCAPE, K_F4, K_p, K_RALT, K_LALT, K_SPACE, \
    MOUSEBUTTONDOWN, QUIT, KEYUP, KEYDOWN, K_TAB, K_v, K_h, K_BACKSPACE, K_q, K_m, K_r
import base64
import io
import os
import platform
import sys
import json
import numpy as np
import datetime
from src.events.event import Event
from src.commands.input_handler import InputHandler

# CONSTANTS
VERSION = '1.17'
WHITE = 255, 255, 255
BLACK = 0, 0, 0
MATTE_BLACK = 20, 20, 20
GREEN = 40, 175, 99
RED = 255, 0, 0
YELLOW = 250, 237, 39
DARK_GREEN = 0, 128, 0
LIGHT_BLUE = 0, 191, 255
GREY = 204, 204, 204
BLUE = 33, 150, 243
BACKGROUND = 174, 222, 203
WORLD_SHIFT_SPEED_PERCENT = 0.00135
FONT_BOLD = 'assets/fonts/OpenSans-SemiBold.ttf'
FONT_REG = 'assets/fonts/OpenSans-Regular.ttf'
FONT_LIGHT = 'assets/fonts/OpenSans-Light.ttf'
GAME_CONFIG_FILE = 'config_game.json'

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'True'


class ClimberGame():

    def __init__(self, shift_speed=1, max_gaps=1, buildno=''):
        self._observers = []
        self.shift_speed = shift_speed
        self.max_gaps = max_gaps
        self.buildno = buildno
        self.inputs = InputHandler()

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, event):
        for obs in self._observers:
            obs.update(event)

    def load_configs(self):
        game_config = {}
        with open(GAME_CONFIG_FILE, 'r') as fp:
            game_config = json.load(fp)
        return game_config

    def save_config(self):
        with open(GAME_CONFIG_FILE, 'w') as fp:
            json.dump(self.game_config, fp, indent=4)

    def text_objects(self, text, font, colour=BLACK):
        text_surface = font.render(text, True, colour)
        return text_surface, text_surface.get_rect()

    def create_hud_text(self, text, color):
        text_surf, text_rect = self.text_objects(text, self.HUD_TEXT, color)
        text_rect.topleft = -2, -5
        bg_w, text_bg_h = text_surf.get_size()
        bg_w += 10
        bg = pygame.Surface((bg_w, text_bg_h), pygame.SRCALPHA, 32)
        bg.fill((50, 50, 50, 160))
        bg.blit(text_surf, (5, 0))
        return bg, text_rect

    def save_score(self, user_score: int) -> bool:
        """
        Takes a score and saves to file if it is a top 10 score else it returns False
        :param user_score: the score of the user
        :return: boolean indicating whether the score was a top 10 score
        """
        scores = self.game_config['high_scores']
        placement = None
        for i, score in enumerate(scores):
            if user_score > score:
                placement = i
                break
        if placement is not None:
            scores.insert(placement, user_score)
            scores.pop()
            self.save_config()
            return True
        return False

    def button(self, text, x, y, w, h, click, inactive_colour=BLUE, active_colour=LIGHT_BLUE, text_colour=WHITE):
        mouse = pygame.mouse.get_pos()
        return_value = False
        if x < mouse[0] < x + w and y < mouse[1] < y + h:  # if mouse is hovering the button
            pygame.draw.rect(self.SCREEN, active_colour, (x, y, w, h))
            if click and pygame.time.get_ticks() > 100:
                return_value = True
        else:
            pygame.draw.rect(self.SCREEN, inactive_colour, (x, y, w, h))

        text_surf, text_rect = self.text_objects(
            text, self.SMALL_TEXT, colour=text_colour)
        text_rect.center = (int(x + w / 2), int(y + h / 2))
        self.SCREEN.blit(text_surf, text_rect)
        return return_value

    def draw_circle(self, surface, x, y, radius, color):
        gfxdraw.aacircle(surface, x, y, radius, color)
        gfxdraw.filled_circle(surface, x, y, radius, color)

    def toggle_btn(self, text, x, y, w, h, click, text_colour=BLACK, enabled=True, draw_toggle=True, blit_text=True,
                   enabled_color=LIGHT_BLUE, disabled_color=GREY):
        mouse = pygame.mouse.get_pos()
        # draw_toggle and blit_text are used to reduce redundant drawing and blitting (improves quality)
        rect_height = h // 2
        if rect_height % 2 == 0:
            rect_height += 1

        if enabled and draw_toggle:
            pygame.draw.rect(self.SCREEN, WHITE, (x + self.TOGGLE_WIDTH -
                             h // 4, y, self.TOGGLE_ADJ + h, rect_height))
            pygame.draw.rect(self.SCREEN, enabled_color, (x +
                             self.TOGGLE_WIDTH, y, self.TOGGLE_ADJ, rect_height))
            self.draw_circle(self.SCREEN, int(
                x + self.TOGGLE_WIDTH), y + h // 4, h // 4, enabled_color)
            self.draw_circle(self.SCREEN, int(
                x + self.TOGGLE_WIDTH + self.TOGGLE_ADJ), y + h // 4, h // 4, enabled_color)
            self.draw_circle(self.SCREEN, int(
                x + self.TOGGLE_WIDTH + self.TOGGLE_ADJ), y + h // 4, h // 5, WHITE)  # small inner circle
        elif draw_toggle:
            pygame.draw.rect(self.SCREEN, WHITE, (x + self.TOGGLE_WIDTH -
                             h // 4, y, self.TOGGLE_ADJ + h, rect_height))
            pygame.draw.rect(self.SCREEN, disabled_color, (x +
                             self.TOGGLE_WIDTH, y, self.TOGGLE_ADJ, rect_height))

            self.draw_circle(self.SCREEN, int(x + self.TOGGLE_WIDTH),
                             (y + h // 4), (h // 4), disabled_color)
            self.draw_circle(self.SCREEN, int(
                x + self.TOGGLE_WIDTH + self.TOGGLE_ADJ), y + h // 4, h // 4, disabled_color)
            self.draw_circle(self.SCREEN, int(x + self.TOGGLE_WIDTH),
                             y + h // 4, h // 5, WHITE)  # small inner circle
        if blit_text:
            text_surf, text_rect = self.text_objects(
                text, self.MEDIUM_TEXT, colour=text_colour)
            text_rect.topleft = (x, y)
            self.SCREEN.blit(text_surf, text_rect)
        return x < mouse[0] < x + w and y < mouse[1] < y + h and click and pygame.time.get_ticks() > 100

    def view_high_scores(self):
        self.SCREEN.fill(WHITE)
        text_surf, text_rect = self.text_objects('High Scores', self.MENU_TEXT)
        text_rect.center = ((self.SCREEN_WIDTH // 2),
                            (self.SCREEN_HEIGHT // 6))
        self.SCREEN.blit(text_surf, text_rect)
        for i, score in enumerate(self.game_config['high_scores']):
            text_surf, text_rect = self.text_objects(
                str(score), self.LARGE_TEXT)
            text_rect.center = (self.SCREEN_WIDTH // 2,
                                int(self.SCREEN_HEIGHT * (i / 1.5 + 3) // 11))
            self.SCREEN.blit(text_surf, text_rect)
        on_high_scores = True
        pygame.display.update()
        back_button_rect = ((self.SCREEN_WIDTH - self.BUTTON_WIDTH) // 2,
                            self.SCREEN_HEIGHT * 4 // 5, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        while on_high_scores:
            click = False
            pressed_keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                alt_f4 = (event.type == KEYDOWN and event.key == pygame.K_F4
                          and (pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]))
                if event.type == QUIT or alt_f4:
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_BACKSPACE):
                    on_high_scores = False
                elif event.type == MOUSEBUTTONDOWN:
                    click = True
            if self.button('B A C K', *back_button_rect, click):
                break
            pygame.display.update([back_button_rect])
            self.clock.tick(60)

    def hide_mouse(self):
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(False)

    def show_mouse(self):
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(True)

    def main_menu_setup(self):
        self.show_mouse()
        self.SCREEN.fill(WHITE)
        text_surf, text_rect = self.text_objects(
            'Jungle Climb', self.MENU_TEXT)
        text_rect.center = (int(self.SCREEN_WIDTH / 2),
                            int(self.SCREEN_HEIGHT / 4))
        self.SCREEN.blit(text_surf, text_rect)
        text_surf, text_rect = self.text_objects(
            f'v{VERSION}', self.SMALL_TEXT)
        text_rect.center = (int(self.SCREEN_WIDTH * 0.98),
                            int(self.SCREEN_HEIGHT * 0.98))
        self.SCREEN.blit(text_surf, text_rect)
        text_surf, text_rect = self.text_objects(
            'Created by Elijah Lopez', self.LARGE_TEXT)
        text_rect.center = (int(self.SCREEN_WIDTH / 2),
                            int(self.SCREEN_HEIGHT * 0.84))
        self.SCREEN.blit(text_surf, text_rect)
        pygame.display.update()

    def main_menu(self):
        global ticks
        self.main_menu_setup()
        start_game = view_hs = False
        while True:
            click = False
            pressed_keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                alt_f4 = (event.type == KEYDOWN and (event.key == K_F4
                                                     and (pressed_keys[K_LALT] or pressed_keys[K_RALT])
                                                     or event.key == K_q or event.key == K_ESCAPE))
                if event.type == QUIT or alt_f4:
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_SPACE:
                    start_game = True
                elif event.type == KEYDOWN and (event.key == K_v or event.key == K_h):
                    view_hs = True
                elif event.type == MOUSEBUTTONDOWN:
                    click = True

            if self.button('S T A R T  G A M E', *self.button_layout_4[0], click):
                start_game = True
            elif self.button('V I E W  H I G H S C O R E S', *self.button_layout_4[1], click) or view_hs:
                self.view_high_scores()
                view_hs = False
                self.main_menu_setup()
            elif self.button('S E T T I N G S', *self.button_layout_4[2], click):
                self.settings_menu()
                self.main_menu_setup()
            elif self.button('Q U I T  G A M E', *self.button_layout_4[3], click):
                sys.exit()
            if start_game:
                while start_game:
                    result = self.run_logic(-1)
                    if result == "Restart":
                        self.main()
                    elif result == "Main Menu":
                        start_game = False
                        self.main()
                        self.main_menu_setup()

            pygame.display.update(self.button_layout_4)
            self.clock.tick(60)

    def settings_menu(self):
        self.SCREEN.fill(WHITE)
        text_surf, text_rect = self.text_objects('Settings', self.MENU_TEXT)
        text_rect.center = ((self.SCREEN_WIDTH // 2),
                            (self.SCREEN_HEIGHT // 4))
        self.SCREEN.blit(text_surf, text_rect)
        pygame.display.update()
        first_run = draw_bg_toggle = draw_jump_toggle = draw_show_fps = True
        while True:
            click = False
            pressed_keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                alt_f4 = (event.type == KEYDOWN and (event.key == K_F4 and (pressed_keys[K_LALT] or pressed_keys[K_RALT])
                                                     or event.key == K_q))
                if event.type == QUIT or alt_f4:
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    click = True
            if self.toggle_btn('Background Music', *self.button_layout_4[0], click, enabled=self.game_config['background_music'],
                               draw_toggle=draw_bg_toggle, blit_text=first_run):
                self.game_config['background_music'] = not self.game_config['background_music']
                self.save_config()
                draw_bg_toggle = True
            elif self.toggle_btn('Jump Sound', *self.button_layout_4[1], click, enabled=self.game_config['jump_sound'],
                                 draw_toggle=draw_jump_toggle, blit_text=first_run):
                self.game_config['jump_sound'] = not self.game_config['jump_sound']
                self.save_config()
                draw_jump_toggle = True
            elif self.toggle_btn('Show FPS', *self.button_layout_4[2], click, enabled=self.game_config['show_fps'],
                                 draw_toggle=draw_show_fps, blit_text=first_run):
                self.game_config['show_fps'] = not self.game_config['show_fps']
                self.save_config()
                draw_show_fps = True
            elif self.button('B A C K', *self.button_layout_4[3], click):
                return
            else:
                draw_bg_toggle = draw_jump_toggle = draw_show_fps = False
            first_run = False
            pygame.display.update(self.button_layout_4)
            self.clock.tick(60)

    def pause_menu_setup(self, background):
        self.SCREEN.blit(background, (0, 0))
        background = self.SCREEN.copy()
        text_surf, text_rect = self.text_objects(
            'Paused', self.MENU_TEXT, colour=WHITE)
        text_rect.center = ((self.SCREEN_WIDTH // 2),
                            (self.SCREEN_HEIGHT // 4))
        self.SCREEN.blit(text_surf, text_rect)
        pygame.display.update()
        return background

    def pause_menu(self, player):
        self.show_mouse()
        paused = True
        # store the pre-pause value in case player doesn't hold a right/left key down
        facing_left = player.facing_right
        background = pygame.Surface(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA, 32)
        background.fill((*MATTE_BLACK, 160))
        background = self.pause_menu_setup(background)
        while paused:
            click = False
            pks = pressed_keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                alt_f4 = (event.type == KEYDOWN and event.key == K_F4
                          and (pressed_keys[K_LALT] or pressed_keys[K_RALT]))
                if event.type == QUIT or alt_f4:
                    sys.exit()
                elif event.type == KEYDOWN:
                    right_key = event.key == K_RIGHT and not pks[K_d] or event.key == K_d and not pks[K_RIGHT]
                    left_key = event.key == K_LEFT and not pks[K_a] or event.key == K_a and not pks[K_LEFT]
                    if right_key:
                        player.go_right()
                    elif left_key:
                        player.go_left()
                    elif event.key in (pygame.K_ESCAPE, pygame.K_p):
                        paused = False
                    elif event.key == K_m:
                        return 'Main Menu'
                    elif event.key == K_SPACE:
                        return 'Resume'
                    elif event.key == K_q:
                        sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    click = True
                elif event.type == KEYUP:
                    if event.key in (K_d, K_RIGHT, K_a, K_LEFT):
                        player.stop(pygame.key.get_pressed())
                        player.facing_right = facing_left
            if self.button('R E S U M E', *self.button_layout_4[0], click):
                return 'Resume'
            if self.button('M A I N  M E N U', *self.button_layout_4[1], click):
                self.main_menu()
            if self.button('S E T T I N G S', *self.button_layout_4[2], click):
                self.settings_menu()
                self.pause_menu_setup(background)
            elif self.button('Q U I T  G A M E', *self.button_layout_4[3], click):
                sys.exit()
            pygame.display.update(self.button_layout_4)
            self.clock.tick(60)
        return 'Resume'

    def end_game_setup(self, score, surface_copy=None):
        if surface_copy is not None:
            self.SCREEN.blit(surface_copy, (0, 0))
        else:
            background = pygame.Surface(
                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA, 32)
            background.fill((255, 255, 255, 160))
            self.SCREEN.blit(background, (0, 0))
            text_surf, text_rect = self.text_objects(
                'Game Over', self.MENU_TEXT)
            text_rect.center = ((self.SCREEN_WIDTH // 2),
                                (self.SCREEN_HEIGHT // 4))
            self.SCREEN.blit(text_surf, text_rect)
            text_surf, text_rect = self.text_objects(
                f'You scored {score}', self.LARGE_TEXT)
            text_rect.center = ((self.SCREEN_WIDTH // 2),
                                (self.SCREEN_HEIGHT * 8 // 21))
            self.SCREEN.blit(text_surf, text_rect)
            surface_copy = pygame.display.get_surface().copy()
        pygame.display.update()
        return surface_copy

    def end_game(self, score):
        self.show_mouse()
        view_hs = False
        end_screen_copy = self.end_game_setup(score)
        if self.save_score(score):
            pass  # Show "You got a high score!"
        button_layout_3 = [(self.button_x_start, self.SCREEN_HEIGHT * 6 // 13, self.BUTTON_WIDTH, self.BUTTON_HEIGHT),
                           (self.button_x_start, self.SCREEN_HEIGHT * 7 //
                            13, self.BUTTON_WIDTH, self.BUTTON_HEIGHT),
                           (self.button_x_start, self.SCREEN_HEIGHT * 8 // 13, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)]
        while True:
            click, pressed_keys = False, pygame.key.get_pressed()
            for event in pygame.event.get():
                alt_f4 = (event.type == KEYDOWN and event.key == pygame.K_F4
                          and (pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]))
                if event.type == QUIT or alt_f4:
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_m):
                    return 'Main Menu'
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_r):
                    return 'Restart'
                elif event.type == KEYDOWN and (event.key == K_v or event.key == K_h):
                    view_hs = True
                elif event.type == MOUSEBUTTONDOWN:
                    click = True
            if self.button('R E S T A R T', *button_layout_3[0], click):
                return 'Restart'
            if self.button('M A I N  M E N U', *button_layout_3[1], click):
                return 'Main Menu'
            elif self.button('V I E W  H I G H S C O R E S', *button_layout_3[2], click) or view_hs:
                self.view_high_scores()
                view_hs = False
                self.end_game_setup(score, end_screen_copy)
            pygame.display.update(button_layout_3)
            self.clock.tick(60)

    def get_gap_position(self):
        gap_x1 = self.SCREEN_WIDTH/2
        gap_x2 = self.SCREEN_WIDTH/2
        height_above = 80

        # get blocks directly above player
        all_blocks = self.world.platform_list.sprites()

        if self.player.on_ground or len(self.blocks_above_1) == 0 or len(self.blocks_above_2) == 0:
            self.blocks_above_1 = np.array([])
            self.blocks_above_2 = np.array([])
            for block in all_blocks:
                if block.rect.left == 0 or block.rect.left == 750:
                    continue
                if block.rect.top > self.player.rect.top - height_above and block.rect.top < self.player.rect.top:
                    self.blocks_above_1 = np.append(
                        self.blocks_above_1, block.rect.left)
                if block.rect.top > self.player.rect.top - (height_above * 3) and block.rect.top < self.player.rect.top - height_above:
                    self.blocks_above_2 = np.append(
                        self.blocks_above_2, block.rect.left)

        size = len(self.blocks_above_1)
        for i, block in enumerate(self.blocks_above_1):
            if i != size - 1:
                dif = self.blocks_above_1[i+1] - block
                if dif > 47:
                    # start of the block + 47 to get to actual gap
                    gap_x1 = block + 47
                    break

        size = len(self.blocks_above_2)
        for i, block in enumerate(self.blocks_above_2):
            if i != size - 1:
                dif = self.blocks_above_2[i+1] - block
                if dif > 47:
                    # start of the block + 47 to get to actual gap
                    gap_x2 = block + 47
                    break

        return gap_x1, gap_x2

    def draw_gap(self, gap_x, y_dist):
        marker = pygame.draw.rect(self.SCREEN, (255, 0, 0), pygame.Rect(
            gap_x, self.player.rect.top - y_dist, 100, 30))
        pygame.display.update(marker)

    def get_jump_status(self):
        player_y = self.player.rect.top
        cur_on_ground = self.player.on_ground
        status = ""
        if not cur_on_ground and self.prev_on_ground:  # if player went from ground to air
            self.player_y_before_jump = player_y
            status = "ascending"
        elif not cur_on_ground and not self.prev_on_ground:  # if player is on air
            status = "on_air"
        elif cur_on_ground and not self.prev_on_ground:  # if player came from air to ground
            # print(player_y, self.player_y_before_jump)
            # print(abs(player_y - self.player_y_before_jump))
            # if player is one platform up
            if player_y < self.player_y_before_jump and abs(player_y - self.player_y_before_jump) > 35:
                status = "climbed"
            else:
                status = "landed"
            self.player_y_before_jump = player_y
        else:  # if player stayed on the ground
            status = "on_ground"
        self.prev_on_ground = cur_on_ground
        return status

    def run_logic(self, action):
        if not pygame.mouse.get_focused():
            if self.music_playing:
                pygame.mixer.Channel(0).pause()
                self.music_playing = False
            if self.game_config['background_music']:
                if pygame.mixer.Channel(0).get_busy():
                    pygame.mixer.Channel(0).unpause()
                else:
                    pygame.mixer.Channel(0).play(self.MUSIC_SOUND, loops=-1)
                    pygame.mixer.Channel(0).set_volume(0)
                self.music_playing = True

        # on utilise 'self' pour accéder également aux variables qui n'appartiennent pas à Player.
        # ainsi, 'self' représente l'instance de la classe ClimberGame, et non seulement Player.
        self.inputs.handle(self)
        
        # aprés vérifier les entrées, on déclanche un evenement que répresent les changements de score
        event = Event(self.score)
        self.notify(event)
        
        # react to commands from agent
        if action == 0:
            self.player.go_right()
        elif action == 1:
            self.player.go_left()
        elif action == 2:
            self.player.jump(self.game_config['jump_sound'])
        self.player.update()

        jump_status = self.get_jump_status()

        if self.score > 0:
            if jump_status == "climbed":
                self.climb_count += 1
        else:
            # avoid computing multiple jumps if you keep going back and forth on the 1st platform
            if jump_status == "climbed":
                self.climb_count = 1

        self.current_time = datetime.datetime.now()
        self.time_elapsed = (self.current_time -
                             self.time_game_started).total_seconds()

        if self.player.rect.top > self.SCREEN_HEIGHT + self.player.rect.height // 2:
            if self.music_playing:
                pygame.mixer.Channel(0).stop()
                self.music_playing = False
            return self.end_game(self.score)

        self.clock.tick(60)
        self.render()

        return -1

    def render(self):
        self.player.update()
        if self.world_shift_speed:
            for _ in range(self.world_shift_speed):
                self.world.shift_world(1)
                self.SCREEN.fill(BACKGROUND)
                self.player.draw(self.SCREEN)
                # some grass appears in front of player
                self.world.draw(self.SCREEN)
            self.score += 1
            if self.score > 1000 * self.world_shift_speed + (self.world_shift_speed - 1) * 1000:
                self.world_shift_speed = min(
                    self.world_shift_speed + self.speed_increment, self.MAX_SPEED)
        else:
            self.SCREEN.fill(BACKGROUND)
            self.player.draw(self.SCREEN)
            # some grass appears in front of player
            self.world.draw(self.SCREEN)
            if self.player.rect.top < self.shift_threshold - 200:
                self.world_shift_speed = self.speed_increment
        if self.game_config['DEBUG']:
            custom_text = f'Platform Sprites: {len(self.world.platform_list)}'
            custom_bg, custom_rect = self.create_hud_text(custom_text, RED)
            custom_rect.topleft = 50, -5
            self.SCREEN.blit(custom_bg, custom_rect)
        if self.game_config['show_fps']:
            fps_bg, fps_rect = self.create_hud_text(
                str(round(self.clock.get_fps())), YELLOW)
            fps_rect.topleft = -2, -5
            self.SCREEN.blit(fps_bg, fps_rect)
        if self.game_config['show_score']:
            score_bg, score_rect = self.create_hud_text(str(self.score), WHITE)
            score_rect.topright = self.SCORE_ANCHOR
            self.SCREEN.blit(score_bg, score_rect)
        pygame.display.update()

    def main(self):
        self.game_config = {'DEBUG': False, 'jump_sound': True, 'background_music': True, 'show_fps': False, 'show_score': True,
                            'high_scores': [0, 0, 0, 0, 0, 0, 0, 0, 0]}
        self.music_playing = False
        self.blocks_above_1 = np.array([])
        self.prev_on_ground = True
        self.climb_count = 0

        # original config file added by the dev
        game_config = self.load_configs()
        for k, v in self.game_config.items():
            self.game_config[k] = game_config[k]

        # Initialization
        if platform.system() == 'Windows':
            from ctypes import windll
            windll.user32.SetProcessDPIAware()
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # center display
        pygame.mixer.init(frequency=44100, buffer=512)
        self.MUSIC_SOUND = pygame.mixer.Sound(
            'assets/audio/background_music.ogg')
        pygame.init()

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.SCREEN = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.BUTTON_WIDTH = int(self.SCREEN_WIDTH * 0.625 // 3)
        self.BUTTON_HEIGHT = int(self.SCREEN_HEIGHT * 5 // 81)
        self.button_x_start = (self.SCREEN_WIDTH - self.BUTTON_WIDTH) // 2
        self.button_layout_4 = [(self.button_x_start, self.SCREEN_HEIGHT * 5 // 13, self.BUTTON_WIDTH, self.BUTTON_HEIGHT),
                                (self.button_x_start, self.SCREEN_HEIGHT * 6 //
                                 13, self.BUTTON_WIDTH, self.BUTTON_HEIGHT),
                                (self.button_x_start, self.SCREEN_HEIGHT * 7 //
                                 13, self.BUTTON_WIDTH, self.BUTTON_HEIGHT),
                                (self.button_x_start, self.SCREEN_HEIGHT * 8 // 13, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)]
        self.TOGGLE_WIDTH = int(self.BUTTON_WIDTH * 0.875)
        self.TOGGLE_ADJ = int(self.BUTTON_WIDTH * 0.075)
        self.SCORE_ANCHOR = self.SCREEN_WIDTH - 8, -5
        self.MENU_TEXT = pygame.font.Font(
            FONT_LIGHT, int(110 / 1080 * self.SCREEN_HEIGHT))
        self.LARGE_TEXT = pygame.font.Font(
            FONT_REG, int(40 / 1080 * self.SCREEN_HEIGHT))
        self.MEDIUM_TEXT = pygame.font.Font(
            FONT_LIGHT, int(35 / 1440 * self.SCREEN_HEIGHT))
        self.SMALL_TEXT = pygame.font.Font(
            FONT_BOLD, int(25 / 1440 * self.SCREEN_HEIGHT))
        self.HUD_TEXT = pygame.font.Font(
            FONT_REG, int(40 / 1440 * self.SCREEN_HEIGHT))

        with open('icon', 'r') as fp:
            ICON = fp.read()
            ICON = pygame.image.load(io.BytesIO(base64.b64decode(ICON)))
            pygame.display.set_icon(ICON)

        if len(self.buildno) > 0:
            pygame.display.set_caption('Jungle Climb, ' + self.buildno)
        else:
            pygame.display.set_caption('Jungle Climb')

        self.clock = pygame.time.Clock()
        self.ticks = 0

        from src.world import World
        from src.player import Player
        self.hide_mouse()
        if not self.music_playing and self.game_config['background_music']:
            pygame.mixer.Channel(0).play(self.MUSIC_SOUND, loops=-1)
            self.music_playing = True
        self.world = World(self.max_gaps)
        self.player = Player(self.world)
        self.player.force_stop()
        self.world.set_player(self.player)
        self.world_shift_speed = 0
        self.speed_increment = 1 * self.shift_speed
        self.MAX_SPEED = self.speed_increment * 3
        self.score = 0
        self.prev_score = 0
        self.time_game_started = datetime.datetime.now()
        self.time_elapsed = 0
        self.shift_threshold = 0.75 * self.SCREEN_HEIGHT
        self.player_y_before_jump = self.player.rect.top