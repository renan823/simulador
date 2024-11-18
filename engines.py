from settings import GRAVITY, FUEL_DENSITY, FUEL_EJECTION, ENGINE_NAMES
from utils import deg_to_rad
import numpy as np
import math

class RocketEngine:
    def __init__(self, burn_rate, mass, fuel, name):
        self.burn_rate = burn_rate
        self.mass = mass
        self.fuel = fuel
        self.active = False
        self.name = name

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def _get_total_mass(self):
        return self.mass + (self.fuel * FUEL_DENSITY)

    def _get_weight(self, angle):
        total = self._get_total_mass()

        return np.array([math.cos(angle), math.sin(angle)]) * total * GRAVITY

    def get_thrust(self, yaw):
        angle = deg_to_rad(yaw)

        weight = self._get_weight(angle) 

        if self.fuel < self.burn_rate:
            return weight

        velocity = np.array([math.cos(angle), math.sin(angle)]) * FUEL_EJECTION * self.burn_rate
        self.fuel -= self.burn_rate

        return velocity - weight


class EngineModel1(RocketEngine):
    def __init__(self, fuel):
        super().__init__(0.5, 200, fuel, ENGINE_NAMES[0])

class EngineModel2(RocketEngine):
    def __init__(self, fuel):
        super().__init__(0.9, 215, fuel, ENGINE_NAMES[1])

class EngineModel3(RocketEngine):
    def __init__(self, fuel):
        super().__init__(1.2, 250, fuel, ENGINE_NAMES[2])