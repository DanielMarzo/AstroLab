import pygame
import math
import rocket
import sys
from config import Config
from planet import Planet
from moon import Moon
from UI import Slider
from UI import HelpWindow

pygame.init()

WIDTH, HEIGHT = Config.WIDTH, Config.HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AstroLab")

# font
#pygame.font.init()
#font = pygame.font.SysFont("comicsans", 30)
font_path = '../assets/data/pixel.ttf'
font = pygame.font.Font(font_path, 30)

# UI
slider = Slider(20, 100, 500, 30, 1, 24)
help_window = HelpWindow(WIN, font)
# constant
Config.G = 6.67428e-11
AU = 149.6e6 * 1000

# variables
# SCALE = 100 / AU  # 100 / AU is 1AU = 100 pixels. Adjust the scale if needed
# Config.TIMESTEP = 3600 * 24  # 3600 * 24 = 1 day per frame. Adjust the timestep to slow down the simulation

# colors
c_sun = (255, 255, 0)
c_earth = (100, 149, 237)
c_mars = (188, 39, 50)
c_mercury = (80, 78, 81)
c_venus = (255, 255, 255)
c_jupiter = (255, 165, 0)
c_saturn = (204, 204, 102)
c_uranus = (173, 216, 230)
c_neptune = (65, 105, 225)
c_moon = (145, 163, 176)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)

# New variables for zoom control
zoom_factor = 0.05  # How much each scroll zooms in or out

background_image = pygame.image.load('../assets/data/background.jpeg').convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

main_menu_image = pygame.image.load('../assets/data/main_menu_bg.jpg').convert()
main_menu_image = pygame.transform.scale(main_menu_image, (WIDTH, HEIGHT))

def pause():
    if not Config.isPaused:  # Pause only if the game is currently running
        Config.isPaused = True
        Config.pausedTime = Config.TIMESTEP  # Save the current timestep
        Config.set_timestep(0)  # Stop the timestep progression


def resume():
    if Config.isPaused:  # Resume only if the game is currently paused
        Config.isPaused = False
        Config.set_timestep(Config.pausedTime)  # Restore the original timestep


def main_menu():
    #WIN.fill((0, 0, 0))
    WIN.blit(main_menu_image, (0, 0))

    font_path = '../assets/data/pixel.ttf'
    font = pygame.font.Font(font_path, 50)
    running = True
    while running:
        #WIN.fill((0, 0, 0))  # Black background or choose another color
        mouse_pos = pygame.mouse.get_pos()

        # Main Menu Text
        # text = font.render("AstroLab", True, (255, 255, 255))
        # WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, 150))

        # Start Button
        start_btn = pygame.Rect(850, 650, 180, 80)
        pygame.draw.rect(WIN, (9, 19, 41), start_btn)  # Green start button

        # Exit Button
        exit_btn = pygame.Rect(0, 720, 200, 100)
        pygame.draw.rect(WIN, (9, 19, 41), exit_btn)  # Red exit button

        #Credits Button
        credit_btn = pygame.Rect(860, 720, 200, 100)
        pygame.draw.rect(WIN, (9, 19, 41), credit_btn)  # Green start button

        # Button Texts
        start_text = font.render("Start", True, (255, 255, 255))
        WIN.blit(start_text, (start_btn.x + (start_btn.width - start_text.get_width()) // 2, start_btn.y + 5))
        credit_text = font.render("Credits", True, (255, 255, 255))
        WIN.blit(credit_text, (credit_btn.x + (credit_btn.width - credit_text.get_width()) // 2, credit_btn.y + 5))
        exit_text = font.render("Exit", True, (255, 255, 255))
        WIN.blit(exit_text, (exit_btn.x + (exit_btn.width - exit_text.get_width()) // 2, exit_btn.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(mouse_pos):
                    main()  # Start the game
                elif exit_btn.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif credit_btn.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                    # insert credits function here and remove the quit code right above

        pygame.display.update()


def draw_arrow(screen, start_pos, end_pos):
    dx, dy = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
    norm = math.hypot(dx, dy)
    if norm == 0:
        return
    dx, dy = dx / norm, dy / norm
    dx, dy = dx * 100, dy * 100
    line_end_pos = start_pos[0] + dx, start_pos[1] + dy
    pygame.draw.line(screen, WHITE, start_pos, line_end_pos, 5)


def main():
    running = True

    clock = pygame.time.Clock()

    temp_rockets = []

    sun = Planet(0, 0, 32, c_sun, 1.98892 * 10 ** 30)  # Sun
    sun.sun = True

    mercury = Planet(0.387 * AU, 0, 8, c_mercury, 3.30 * 10 ** 23)  # Mercury
    mercury.y_velocity = -47.4 * 1000

    venus = Planet(0.723 * AU, 0, 14, c_venus, 4.8685 * 10 ** 24)  # Venus
    venus.y_velocity = -35.02 * 1000

    earth = Planet(-1 * AU, 0, 16, c_earth, 5.9742 * 10 ** 24)  # Earth
    earth.y_velocity = 29.783 * 1000

    mars = Planet(-1.524 * AU, 0, 12, c_mars, 6.39 * 10 ** 23)  # Mars
    mars.y_velocity = 24.077 * 1000

    jupiter = Planet(-5.204 * AU, 0, 22, c_jupiter, 1.898 * 10 ** 27)
    jupiter.y_velocity = 13.06 * 1000

    saturn = Planet(-9.582 * AU, 0, 24, c_saturn, 5.683 * 10 ** 26)
    saturn.y_velocity = 9.68 * 1000

    uranus = Planet(-19.218 * AU, 0, 26, c_uranus, 8.681 * 10 ** 25)
    uranus.y_velocity = 6.80 * 1000

    neptune = Planet(30.110 * AU, 0, 34, c_neptune, 1.024 * 10 ** 26)
    neptune.y_velocity = -5.43 * 1000

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    moon = Moon(earth, 4, c_moon, 7.34767309 * 10 ** 22, 0.00257 * AU * 50)

    days_passed = 0
    ofx, ofy = 0, 0
    currx, curry = pygame.mouse.get_pos()

    arrow_start_pos = 0, 0

    while running:
        clock.tick(60)
        WIN.fill((0, 0, 0))
        WIN.blit(background_image, (0, 0))

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    help_window.toggle_visibility()

            if event.type == pygame.MOUSEBUTTONDOWN:
                currx = pygame.mouse.get_pos()[0] - ofx
                curry = pygame.mouse.get_pos()[1] - ofy
                # Zoom in
                if event.button == 4:
                    if (Config.get_scale() <= ((100 / Config.AU) * 10)):
                        Config.set_scale(Config.get_scale() * (1 + Config.get_zoom_factor()))
                        ofx *= (1 + Config.get_zoom_factor())
                        ofy *= (1 + Config.get_zoom_factor())

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Only access event.key here
                        running = False
                        pygame.quit()
                        sys.exit()
                # Zoom out
                if event.button == 5:
                    if (Config.get_scale() >= ((100 / Config.AU) * .1)):
                        Config.set_scale(Config.get_scale() / (1 + Config.get_zoom_factor()))
                        ofx /= (1 + Config.get_zoom_factor())
                        ofy /= (1 + Config.get_zoom_factor())
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] and not keys[pygame.K_LSHIFT]:
                ofx = pygame.mouse.get_pos()[0] - currx
                if ofx > Config.WIDTH * .85:
                    ofx = Config.WIDTH * .85
                if ofx < -1 * Config.WIDTH * .85:
                    ofx = -1 * Config.WIDTH * .85

                ofy = pygame.mouse.get_pos()[1] - curry
                if ofy > Config.HEIGHT * .85:
                    ofy = Config.HEIGHT * .85
                if ofy < -1 * Config.HEIGHT * .85:
                    ofy = -1 * Config.HEIGHT * .85

            earth_pos_x_pixel = (earth.x * Config.get_scale()) + WIDTH / 2 + ofx
            earth_pos_y_pixel = (earth.y * Config.get_scale()) + HEIGHT / 2 + ofy
            arrow_start_pos = (earth_pos_x_pixel, earth_pos_y_pixel)
            # Right click to enter aiming mode
            # Right click again to cancel
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if not Config.aiming_mode and len(temp_rockets) == 0:
                    Config.aiming_mode = True
                else:
                    Config.aiming_mode = False
                # the game will pause while aiming
                if Config.isPaused:
                    resume()
                else:
                    if Config.aiming_mode:
                        pause()
            # Space bar to launch if in aiming mode
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and Config.aiming_mode:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    scale_x = (mouse_x - Config.WIDTH / 2 - ofx) / Config.get_scale()
                    scale_y = (mouse_y - Config.HEIGHT / 2 - ofy) / Config.get_scale()
                    new_rocket = rocket.Rocket.create_rocket(earth.x, earth.y, scale_x, scale_y)
                    temp_rockets.append(new_rocket)
                    Config.aiming_mode = False
                    resume()
                if event.key == pygame.K_r and len(temp_rockets) != 0:
                    temp = temp_rockets[0]
                    temp_rockets.remove(temp)
                    del temp

            slider.handle_event(event)

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN, ofx, ofy)

        moon.update_position(None)
        moon.draw(WIN, ofx, ofy)

        x_acceleration = 500
        y_acceleration = 500
        for temp_rocket in temp_rockets[:]:
            if temp_rocket:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    temp_rocket.x_velocity -= x_acceleration
                if keys[pygame.K_d]:
                    temp_rocket.x_velocity += x_acceleration
                if keys[pygame.K_w]:
                    temp_rocket.y_velocity -= y_acceleration
                if keys[pygame.K_s]:
                    temp_rocket.y_velocity += y_acceleration
                temp_rocket.update_position(planets)
                if not temp_rocket.still_moving:
                    temp_rockets.remove(temp_rocket)
                    del temp_rocket
                else:
                    temp_rocket.draw(WIN, ofx, ofy)

        days_passed += Config.get_timestep() / (3600 * 24)
        days_text = font.render(f"Days passed: {int(days_passed)} Days", True, (255, 255, 255))
        WIN.blit(days_text, (10, 10))
        zoom_text = font.render(f"Zoom Factor: {round(Config.get_scale() / (100 / Config.AU), 4)} x", True,
                                (255, 255, 255))
        WIN.blit(zoom_text, (750, 10))
        help_page_text = font.render('HELP:F1', True, (255, 255, 255))
        if not help_window.is_visible:
            WIN.blit(help_page_text, (10, 700))
        slider.draw(WIN)
        help_window.draw()
        if Config.aiming_mode:
            draw_arrow(WIN, arrow_start_pos, pygame.mouse.get_pos())

        pygame.display.update()

    pygame.quit()


main_menu()
