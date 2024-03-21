import pygame
import math
import sys
from src.UI import Slider

pygame.init()

WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AstraLab")

AU = 149.6e6 * 1000
G = 6.67428e-11

slider = Slider(20, 100, 500, 30, 1, 24)

SCALE = 100 / AU  # 100 / AU is 1AU = 100 pixels. Adjust the scale if needed
TIMESTEP = 3600 * slider.val  # 3600 * 24 = 1 day per frame. Adjust the timestep to slow down the simulation
SCALE = 100 / AU  # 100 pixels per AU. Adjust the scale if needed
TIMESTEP = 3600 * 24  # One day per frame. Adjust the timestep to slow down the simulation


Yellow = (255, 255, 0)
Blue = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
WHITE = (255, 255, 255)

pygame.font.init()
font = pygame.font.SysFont("comicsans", 30)

# New variables for zoom control
zoom_factor = 0.05  # How much each scroll zooms in or out

#Slider object


class Planet:
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_velocity = 0
        self.y_velocity = 0

    def draw(self, win):
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = [(point[0] * SCALE + WIDTH / 2, point[1] * SCALE + HEIGHT / 2) for point in self.orbit]
            pygame.draw.lines(win, DARK_GREY, False, updated_points, 1)

        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x) # theta is the angle
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_velocity += total_fx / self.mass * TIMESTEP
        self.y_velocity += total_fy / self.mass * TIMESTEP

        self.x += self.x_velocity * TIMESTEP
        self.y += self.y_velocity * TIMESTEP
        self.orbit.append((self.x, self.y))


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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(mouse_pos):
                    main()  # Start the game
                elif exit_btn.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def main():
    global SCALE  # Make SCALE modifiable globally
    running = True
    clock = pygame.time.Clock()

    # Planet definitions remain the same

    sun = Planet(0, 0, 30, Yellow, 1.98892 * 10 ** 30)  # Sun
    sun.sun = True

    mercury = Planet(0.387 * AU, 0, 8, DARK_GREY, 3.30 * 10 ** 23)  # Mercury
    mercury.y_velocity = -47.4 * 1000

    venus = Planet(0.723 * AU, 0, 14, WHITE, 4.8685 * 10 ** 24)  # Venus
    venus.y_velocity = -35.02 * 1000

    earth = Planet(-1 * AU, 0, 16, Blue, 5.9742 * 10 ** 24)  # Earth
    earth.y_velocity = 29.783 * 1000

    mars = Planet(-1.524 * AU, 0, 12, RED, 6.39 * 10 ** 23)  # Mars
    mars.y_velocity = 24.077 * 1000

    jupiter = Planet(-5.204 * AU, 0, 28, (255, 165, 0), 1.898 * 10 ** 27)
    jupiter.y_velocity = 13.06 * 1000

    saturn = Planet(9.582 * AU, 0, 30, (204, 204, 102), 5.683 * 10 ** 26)
    saturn.y_velocity = 9.68 * 1000

    uranus = Planet(19.218 * AU, 0, 32, (173, 216, 230), 8.681 * 10 ** 25)
    uranus.y_velocity = 6.80 * 1000

    neptune = Planet(30.110 * AU, 0, 34, (65, 105, 225), 1.024 * 10 ** 26)
    neptune.y_velocity = 5.43 * 1000

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    days_passed = 0
    while running:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Only access event.key here
                    running = False
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Zoom in
                if event.button == 4:
                    SCALE *= (1 + zoom_factor)
                # Zoom out
                elif event.button == 5:
                    SCALE /= (1 + zoom_factor)

            slider.handle_event(event)


        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        slider.draw(WIN)
        TIMESTEP = 3600 * slider.val
        days_passed += TIMESTEP / (3600 * 24)
        days_text = font.render(f"Days passed: {int(days_passed)} Days", True, (255, 255, 255))
        WIN.blit(days_text, (10, 10))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main_menu()
