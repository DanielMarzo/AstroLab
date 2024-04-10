import pygame
import math
import planet
from config import Config


class Rocket:
    def __init__(self, x, y, vx=0, vy=0):
        # Data based on Saturn V, the most powerful rocket.
        # mass = 2822000 kg
        # Second Cosmic Velocity = 11.2 km/s = 11200 m/s
        # This is the speed for rocket escape from the earth and fly to other planets
        self.still_moving = True
        self.mass = 2822000
        self.x = x
        self.y = y
        self.x_velocity = vx
        self.y_velocity = vy
        self.radius = 3
        self.touching = None
        self.color = (255, 0, 0)

    @staticmethod
    def create_rocket(start_x, start_y, target_x, target_y, speed=11200 * 4):
        dx, dy = target_x - start_x, target_y - start_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0:
            distance = 1
        dx, dy = dx / distance, dy / distance
        vx, vy = dx * speed, dy * speed
        return Rocket(start_x, start_y, vx, vy)

    def draw(self, win, ofx, ofy):
        x_screen = self.x * Config.get_scale() + Config.WIDTH / 2 + ofx
        y_screen = self.y * Config.get_scale() + Config.HEIGHT / 2 + ofy
        pygame.draw.circle(win, self.color, (int(x_screen), int(y_screen)), self.radius)

    def attraction(self, other):
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        force = Config.G * self.mass * other.mass / distance ** 2

        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        if self.still_moving:
            total_fx = total_fy = 0
            for p in planets:
                fx, fy = self.attraction(p)
                total_fx += fx
                total_fy += fy
                if self.isTouching(p.x, p.y,p):
                    if p.radius != 16:
                        self.touching = p
                        self.still_moving = False
                        break
        if self.still_moving:
            self.x_velocity += total_fx / self.mass * Config.get_timestep()
            self.y_velocity += total_fy / self.mass * Config.get_timestep()

            self.x += self.x_velocity * Config.get_timestep()
            self.y += self.y_velocity * Config.get_timestep()

        else:
            self.x = self.touching.x
            self.y = self.touching.y

    def isTouching(self, _x, _y, planet):

        if math.sqrt((_x - self.x) ** 2 + (_y - self.y) ** 2) < planet.adj_radius*Config.AU/180:
            return True
        return False

