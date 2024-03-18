import pygame
import math
import rocket
from config import Config
from planet import Planet
from moon import Moon

pygame.init()

WIDTH, HEIGHT = Config.WIDTH, Config.HEIGHT
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AstroLab")

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
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Zoom in
                if event.button == 4:
                    Config.set_scale(Config.get_scale() * (1 + Config.get_zoom_factor()))
                # Zoom out
                if event.button == 5:
                    Config.set_scale(Config.get_scale() / (1 + Config.get_zoom_factor()))
                currx = pygame.mouse.get_pos()[0] - ofx
                curry = pygame.mouse.get_pos()[1] - ofy

            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[2]:
                ofx = pygame.mouse.get_pos()[0] - currx
                ofy = pygame.mouse.get_pos()[1] - curry

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                scale_x = (mouse_x - Config.WIDTH / 2 - ofx) / Config.get_scale()
                scale_y = (mouse_y - Config.HEIGHT / 2 - ofy) / Config.get_scale()
                new_rocket = rocket.Rocket.create_rocket(scale_x, scale_y)
                temp_rockets.append(new_rocket)

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

        pygame.display.update()

    pygame.quit()


main()
