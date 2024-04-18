import pygame
import random
import textwrap
from config import Config

# Colors
GRAY = (200, 200, 200)
BLUE = (0, 120, 255)


class Slider:
    def __init__(self, x, y, w, h, min_val, max_val):
        self.rect = pygame.Rect(x, y, w, h)  # The track
        self.handle_rect = pygame.Rect(x, y, 20, h)  # The handle
        self.min_val = min_val
        self.max_val = max_val
        self.val = max_val  # Current value
        self.dragging = False
        Config.TIMESTEP = 3600 * self.max_val

        position_ratio = (self.max_val - self.min_val) / (self.max_val - self.min_val)
        new_handle_x = self.rect.x + position_ratio * (self.rect.width - self.handle_rect.width)
        self.handle_rect.x = new_handle_x

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLUE, self.handle_rect)

    def handle_event(self, event):
        keys = pygame.key.get_pressed()
        if event.type == pygame.MOUSEBUTTONDOWN and keys[pygame.K_LSHIFT]:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_rect.x = max(self.rect.x, min(event.pos[0], self.rect.right - self.handle_rect.width))
            self.val = ((self.handle_rect.x - self.rect.x) / (self.rect.width - self.handle_rect.width)) * (
                    self.max_val - self.min_val) + self.min_val
            Config.TIMESTEP = 3600 * self.val


class HelpWindow:
    def __init__(self, screen, font, position=(0, 0), size=(1080, 800), bg_color=(200, 200, 200), transparency=128):
        self.screen = screen
        self.font = font
        self.position = position
        self.size = size
        self.bg_color = bg_color
        self.transparency = transparency
        self.is_visible = True

        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)

    def toggle_visibility(self):
        self.is_visible = not self.is_visible

    def draw(self):
        if self.is_visible:
            self.surface.fill((*self.bg_color, self.transparency))

            # h_ for help page
            h_days = self.font.render('* A factor to indicate the days passed', True, (0, 0, 0))
            h_factor1 = self.font.render('* A factor to indicate', True, (0, 0, 0))
            h_factor2 = self.font.render('* the current zoom in/out', True, (0, 0, 0))
            h_slider1 = self.font.render('* Pressing "Shift" key and drag the bar', True, (0, 0, 0))
            h_slider2 = self.font.render('  to control the time speed', True,
                                         (0, 0, 0))
            h_help_page = self.font.render('* Press "F1" key to open/close the help page', True, (0, 0, 0))

            h_launch1 = self.font.render('* Right click to enter aiming mode', True, (0, 0, 0))
            h_launch2 = self.font.render('* In the aiming mode, press "space bar" to launch', True, (0, 0, 0))
            h_launch3 = self.font.render('* In the aiming mode, right click again to cancel the launch', True,
                                         (0, 0, 0))
            h_delete_rocket1 = self.font.render('* Press "R" to delete', True, (0, 0, 0))
            h_delete_rocket2 = self.font.render('  the current rocket', True, (0, 0, 0))
            h_control_rocket = self.font.render('* "W,A,S,D" to control the rocket after launch', True, (0, 0, 0))

            h_dragging_window = self.font.render('* Pressing left click and drag to moving the window', True, (0, 0, 0))
            h_zoom_in1 = self.font.render('* Use the scroll wheel', True, (0, 0, 0))
            h_zoom_in2 = self.font.render('  to zoom in/out', True, (0, 0, 0))

            self.surface.blit(h_days, (10, 50))
            self.surface.blit(h_factor1, (700, 50))
            self.surface.blit(h_factor2, (700, 100))
            self.surface.blit(h_slider1, (10, 150))
            self.surface.blit(h_slider2, (10, 200))
            self.surface.blit(h_help_page, (10, 700))

            self.surface.blit(h_launch1, (10, 300))
            self.surface.blit(h_launch2, (10, 350))
            self.surface.blit(h_launch3, (10, 400))
            self.surface.blit(h_delete_rocket1, (10, 500))
            self.surface.blit(h_delete_rocket2, (10, 550))
            self.surface.blit(h_delete_rocket2, (10, 550))
            self.surface.blit(h_control_rocket, (10, 650))
            self.surface.blit(h_zoom_in1, (700, 150))
            self.surface.blit(h_zoom_in2, (700, 200))
            self.surface.blit(h_dragging_window, (10, 250))

            self.screen.blit(self.surface, self.position)


class Credits:
    def __init__(self, screen, font, position=(100, 150), size=(880, 500), bg_color=(200, 200, 200), transparency=3):
        self.screen = screen
        self.font = font
        self.position = position
        self.size = size
        self.bg_color = bg_color
        self.transparency = transparency
        self.is_visible = False

        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)

    def toggle_visibility(self):
        self.is_visible = not self.is_visible

    def draw(self):
        if self.is_visible:
            self.surface.fill((*self.bg_color, self.transparency))

            team_title = self.font.render('Team Members', True, (0, 0, 0))
            bd = self.font.render('Boning Deng (Back End Developer)', True, (0, 0, 0))
            dm = self.font.render('Daniel Marzo (Front End Developer)', True, (0, 0, 0))
            el = self.font.render('Elli Ludwin (Project Manager)', True, (0, 0, 0))
            ng = self.font.render('Nikhil Giridharan (Scrum Master)', True, (0, 0, 0))
            ja = self.font.render('Professor Jeffrey Andrews (Project Advisor)', True, (0, 0, 0))
            thanks = self.font.render('Special Thanks To:', True, (0, 0, 0))

            self.surface.blit(team_title, (10, 200))
            self.surface.blit(bd, (10, 250))
            self.surface.blit(dm, (10, 300))
            self.surface.blit(el, (10, 350))
            self.surface.blit(ng, (10, 400))
            self.surface.blit(ja, (10, 100))
            self.surface.blit(thanks, (10, 50))

            self.screen.blit(self.surface, self.position)


class GameMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.back_button = pygame.Rect(420, 300, 200, 50)
        self.exit_button = pygame.Rect(440, 450, 200, 50)
        self.visible = False

    def toggle_visibility(self):
        self.visible = not self.visible

    def draw(self):
        if not self.visible:
            return
        pygame.draw.rect(self.screen, (0, 0, 0), self.back_button)
        pygame.draw.rect(self.screen, (0, 0, 0), self.exit_button)
        back_text = self.font.render('Back to Menu', True, (255, 255, 255))
        exit_text = self.font.render('Exit', True, (255, 255, 255))
        self.screen.blit(back_text, (self.back_button.x + 20, self.back_button.y + 10))
        self.screen.blit(exit_text, (self.exit_button.x + 70, self.exit_button.y + 10))

    def handle_event(self, event):
        if not self.visible:
            return None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return "main_menu"
            elif self.exit_button.collidepoint(event.pos):
                return "exit"
        return None


class TipsPlayer:
    def __init__(self, screen, font, tips_file):
        self.screen = screen
        self.font = font
        self.timer = 20000
        self.tips = self.load_tips(tips_file)
        self.current_tip_index = random.randint(0, len(self.tips) - 1)
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, self.timer)
        self.visible = False

    @staticmethod
    def load_tips(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            tips = [line.strip() for line in file if line.strip()]
        return tips

    def toggle_visibility(self):
        self.visible = not self.visible

    def get_random_tip(self):
        indices = list(range(len(self.tips)))
        if len(indices) > 1:
            indices.remove(self.current_tip_index)
        return random.choice(indices)

    def is_visible(self):
        return self.visible

    def update(self, event):
        if self.visible and event.type == self.timer_event:
            self.current_tip_index = self.get_random_tip()

    def draw(self):
        if not self.visible:
            return

        tip_title = self.font.render("Do you know: ", True, (255, 255, 255))
        title_rect = tip_title.get_rect(x=10, y=600)
        self.screen.blit(tip_title, title_rect)

        lines = textwrap.wrap(self.tips[self.current_tip_index], width=50)

        for i, line in enumerate(lines):
            tip_line = self.font.render(line, True, (255, 255, 255))
            line_rect = tip_line.get_rect(x=220, y=600 + i * (self.font.get_height()))
            self.screen.blit(tip_line, line_rect)
