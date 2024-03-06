import pygame
import math
from config import Config


class Rocket:
    def __init__(self, x, y):
        # Data based on Saturn V, the most powerful rocket.
        # mass = 2822000 kg
        # Second Cosmic Velocity = 11.2 km/s = 11200 m/s
        # This is the speed for rocket escape from the earth and fly to other planets

        self.mass = 2822000
        self.x = x
        self.y = y
        self.x_velocity = 0
        self.y_velocity = 0

    @staticmethod
    def create_rocket(x, y):
        return Rocket(x, y)

    def draw(self, win, ofx, ofy):
        x_screen = self.x * Config.get_scale() + Config.WIDTH / 2 + ofx
        y_screen = self.y * Config.get_scale() + Config.HEIGHT / 2 + ofy
        pygame.draw.circle(win, (255, 0, 0), (int(x_screen), int(y_screen)), 5)

    def attraction(self, other):
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        force = Config.G * self.mass * other.mass / distance**2

        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_velocity += total_fx / self.mass * Config.get_timestep()
        self.y_velocity += total_fy / self.mass * Config.get_timestep()

        self.x += self.x_velocity * Config.get_timestep()
        self.y += self.y_velocity * Config.get_timestep()

    def destroyed(self, x, y):
        if self.x > Config.WIDTH or self.y > Config.HEIGHT:
            return True



