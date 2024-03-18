import pygame
import math
from config import Config

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

    def draw(self, win, ofx, ofy):
        AU = 149.6e6 * 1000

        x = self.x * Config.get_scale() + Config.WIDTH / 2
        y = self.y * Config.get_scale() + Config.HEIGHT / 2

        if len(self.orbit) > 100:
            self.orbit.pop(0)
            self.orbit.pop(0)

        if len(self.orbit) > 2:
            updated_points = [(point[0] * Config.get_scale() + Config.WIDTH / 2 + ofx,
                               point[1] * Config.get_scale() + Config.HEIGHT / 2 + ofy) for point in
                              self.orbit]
            pygame.draw.lines(win, (201, 201, 201), False, updated_points, 1)

        pygame.draw.circle(win, self.color, (int(x) + ofx, int(y) + ofy), self.radius * Config.get_scale() * AU / 200)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = Config.G * self.mass * other.mass / distance ** 2

        theta = math.atan2(distance_y, distance_x)  # theta is the angle
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        if not self.sun:
            total_fx = total_fy = 0
            for planet in planets:
                if self == planet:
                    continue

                fx, fy = self.attraction(planet)
                total_fx += fx
                total_fy += fy

            self.x_velocity += total_fx / self.mass * Config.get_timestep()
            self.y_velocity += total_fy / self.mass * Config.get_timestep()

            self.x += self.x_velocity * Config.get_timestep()
            self.y += self.y_velocity * Config.get_timestep()
            self.orbit.append((self.x, self.y))
