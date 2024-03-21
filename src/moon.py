import pygame
import math
from config import Config
from planet import Planet


class Moon(Planet):
    def __init__(self, host_planet, radius, color, mass, distance_from_planet):
        super().__init__(host_planet.x, host_planet.y, radius, color, mass)
        self.host_planet = host_planet
        self.distance_from_planet = distance_from_planet
        self.angle = 0
        self.days_per_orbit = 27.3
        self.radians_per_day = (2 * math.pi) / self.days_per_orbit

    def update_position(self, _):
        self.angle += self.radians_per_day * (Config.get_timestep() / 86400)
        self.angle %= 2 * math.pi
        self.x = self.host_planet.x + math.cos(self.angle) * self.distance_from_planet
        self.y = self.host_planet.y + math.sin(self.angle) * self.distance_from_planet
        self.orbit.append((self.x, self.y))
