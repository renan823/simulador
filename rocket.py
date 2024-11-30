from settings import GRAVITY, VISCOSITY, FUEL_DENSITY
from engines import RocketEngine
from utils import deg_to_rad
import numpy as np
import math

class Rocket:
    def __init__(self, x: float, y: float, yaw: int, engine: RocketEngine) -> None:
        self.width: int = 20
        self.height: int = 100
        self.pos = np.array([float(x), float(y)])
        self.vel = np.array([0.0, 0.0])
        self.acc = np.array([0.0, 0.0])
        self.mass = 50  # Massa do foguete sem combustível
        self.engine = engine
        self.yaw = yaw

    def get_thrust(self, yaw: int) -> np.ndarray:
        if self.fuel <= 0:
            return np.array([0.0, 0.0])

        angle = deg_to_rad(yaw)
        thrust = np.array([math.cos(angle), math.sin(angle)]) * self.fuel_ejection * self.burn_rate * (self.fuel / 900)
        self.fuel = max(0, self.fuel - self.burn_rate)
        return thrust

    def _get_weight(self) -> np.ndarray:
        angle = deg_to_rad(self.yaw)
        total_mass = self.mass + (self.engine.fuel * FUEL_DENSITY)
        return np.array([math.cos(angle), math.sin(angle)]) * total_mass * GRAVITY

    def _get_viscosity(self) -> np.ndarray:
        return -self.vel * VISCOSITY

    def _get_resultant_force(self) -> np.ndarray:
        thrust = self.engine.get_thrust(self.yaw)
        weight = self._get_weight()
        viscosity = self._get_viscosity()
        return - thrust + weight + viscosity

    def _get_acceleration(self) -> np.ndarray:
        force = self._get_resultant_force()
        total_mass = self.mass + (self.engine.fuel * FUEL_DENSITY)
        acceleration = force / total_mass
        return acceleration

    def update(self, dt: float) -> None:
        self.acc = self._get_acceleration()
        print(self.vel)
        self.vel += self.acc * dt
        print(self.vel)
        self.pos += self.vel * dt

