import pygame
import math
import rocket
import sys
from config import Config
from planet import Planet
from moon import Moon
from UI import Slider

pygame.init()

WIDTH, HEIGHT = Config.WIDTH, Config.HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AstroLab")

slider = Slider(20, 100, 500, 30, 1, 24)
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

# font
pygame.font.init()
font = pygame.font.SysFont("comicsans", 30)

# New variables for zoom control
zoom_factor = 0.05  # How much each scroll zooms in or out

def main_menu():
    font = pygame.font.SysFont("comicsans", 60)
    running = True
    while running:
        WIN.fill((0, 0, 0))  # Black background or choose another color
        mouse_pos = pygame.mouse.get_pos()

        # Main Menu Text
        text = font.render("AstroLab", True, (255, 255, 255))
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, 150))

        # Start Button
        start_btn = pygame.Rect(WIDTH // 2 - 100, 300, 200, 100)
        pygame.draw.rect(WIN, (0, 255, 0), start_btn)  # Green start button

        # Exit Button
        exit_btn = pygame.Rect(WIDTH // 2 - 100, 400, 200, 100)
        pygame.draw.rect(WIN, (255, 0, 0), exit_btn)  # Red exit button

        # Button Texts
        start_text = font.render("Start", True, (255, 255, 255))
        WIN.blit(start_text, (start_btn.x + (start_btn.width - start_text.get_width()) // 2, start_btn.y + 5))
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

        pygame.display.update()


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

    while running:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

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
                    if(Config.get_scale() >= ((100/Config.AU)*.1)):
                        Config.set_scale(Config.get_scale() / (1 + Config.get_zoom_factor()))
                        ofx /= (1 + Config.get_zoom_factor())
                        ofy /= (1 + Config.get_zoom_factor())
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0] and not keys[pygame.K_LSHIFT]:
                ofx = pygame.mouse.get_pos()[0] - currx
                ofy = pygame.mouse.get_pos()[1] - curry

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                scale_x = (mouse_x - Config.WIDTH / 2 - ofx) / Config.get_scale()
                scale_y = (mouse_y - Config.HEIGHT / 2 - ofy) / Config.get_scale()
                new_rocket = rocket.Rocket.create_rocket(scale_x, scale_y)
                temp_rockets.append(new_rocket)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                if paused:
                    paused = False
                    Config.TIMESTEP = 0
                else:
                    paused = True
                    Config.TIMESTEP = 3600 * 24

            slider.handle_event(event)

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN, ofx, ofy)

        moon.update_position(None)
        moon.draw(WIN, ofx, ofy)

        for temp_rocket in temp_rockets:
            temp_rocket.update_position(planets)
            temp_rocket.draw(WIN, ofx, ofy)

        days_passed += Config.get_timestep() / (3600 * 24)
        days_text = font.render(f"Days passed: {int(days_passed)} Days", True, (255, 255, 255))
        WIN.blit(days_text, (10, 10))
        zoom_text = font.render(f"Zoom Factor: {round(Config.get_scale()/(100/Config.AU),4)} x", True, (255, 255, 255))
        WIN.blit(zoom_text, (750, 10))
        slider.draw(WIN)

        pygame.display.update()

    pygame.quit()


main_menu()
