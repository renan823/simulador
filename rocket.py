from settings import GRAVITY, VISCOSITY
from engines import RocketEngine
from utils import deg_to_rad
import numpy as np
import math

class Rocket:
    def __init__(self, x, y, yaw, engine: RocketEngine):
        self.width = 20
        self.height = 100
        self.pos = np.array([x, y])
        self.vel = np.array([0, 0])
        self.acc = np.array([0, 0])
        self.mass = 500
        self.engine = engine
        self.yaw = yaw

    def _get_weight(self):
        angle = deg_to_rad(self.yaw)

        return np.array([math.cos(angle), math.sin(angle)]) * self.mass * GRAVITY

    def _get_viscosity(self):
        return self.vel * VISCOSITY

    def _get_resultant_force(self):
        thrust = self.engine.get_thrust(self.yaw)
        weight = self._get_weight()
        viscosity = self._get_viscosity()

        return thrust - weight - viscosity

    def _get_acceleration(self):
        force = self._get_resultant_force()
        return force / mass

    def update(self, dt):
        self.acc = self._get_acceleration()
        self.vel += self.acc * dt
        self.pos += self.vel * dt