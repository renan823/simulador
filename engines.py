from settings import GRAVITY, FUEL_DENSITY, FUEL_EJECTION, ENGINE_NAMES
from utils import deg_to_rad
import numpy as np
import math

class RocketEngine:
    def __init__(self, burn_rate: float, mass: float, fuel: float, name: str) -> None:
        self.burn_rate: float= burn_rate
        self.mass: float = mass
        self.fuel: float = fuel
        self.active: bool = False
        self.name: str = name

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False

    def _get_total_mass(self) -> float:
        return self.mass + (self.fuel * FUEL_DENSITY)

    def _get_weight(self, angle: int) -> float:
        total = self._get_total_mass()

        return np.array([math.cos(angle), math.sin(angle)]) * total * GRAVITY

    def get_thrust(self, yaw: int) -> float:
        angle = deg_to_rad(yaw)

        weight = self._get_weight(angle)

        velocity = np.array([math.cos(angle), math.sin(angle)]) * FUEL_EJECTION * self.burn_rate
        self.fuel -= self.burn_rate

        return velocity - weight


class EngineModel1(RocketEngine):
    def __init__(self, fuel: float):
        super().__init__(0.5, 200, fuel, ENGINE_NAMES[0])

class EngineModel2(RocketEngine):
    def __init__(self, fuel):
        super().__init__(0.9, 215, fuel, ENGINE_NAMES[1])

class EngineModel3(RocketEngine):
    def __init__(self, fuel):
        super().__init__(1.2, 250, fuel, ENGINE_NAMES[2])