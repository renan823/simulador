from settings import GRAVITY, VISCOSITY
from engines import RocketEngine
from utils import deg_to_rad
import numpy as np
import math

class Rocket:
    def __init__(self, x: int, y: int, yaw: int, engine: RocketEngine) -> None:
        self.width: int = 20
        self.height: int = 100
        self.pos = np.array([x, y])
        self.vel = np.array([0, 0])
        self.acc = np.array([0, 0])
        self.mass = 500
        self.engine = engine
        self.yaw = yaw

    def _get_weight(self) -> float:
        angle = deg_to_rad(self.yaw)

        return np.array([math.cos(angle), math.sin(angle)]) * self.mass * GRAVITY

    def _get_viscosity(self) -> float:
        return self.vel * VISCOSITY

    def _get_resultant_force(self) -> float:
        thrust = self.engine.get_thrust(self.yaw)
        weight = self._get_weight()
        viscosity = self._get_viscosity()

        return thrust - weight - viscosity

    def _get_acceleration(self) -> float:
        force = self._get_resultant_force()
        return force / self.mass

    def update(self, dt: float) -> None:
        self.acc = self._get_acceleration()
        self.vel += self.acc * dt
        self.pos += self.vel * dt