from settings import GRAVITY, VISCOSITY
from pygame import math

class Rocket:
    def __init__(self, x, y):
        self.width = 20
        self.height = 100
        self.pos = math.Vector2(x, y)
        self.vel = math.Vector2(0, 0)
        self.acc = math.Vector2(0, 0)
        self.mass = 500

    def _get_thrust(self):
        # Calcular empuxo gerado
        return math.Vector2(0, 800)

    def _get_weight(self):
        return math.Vector2(0, GRAVITY * self.mass)

    def _get_viscosity(self):
        return math.Vector2(self.vel.x * VISCOSITY, self.vel.y * VISCOSITY)

    def _get_resultant_force(self):
        thrust = self._get_thrust()
        weight = self._get_weight()
        viscosity = self._get_viscosity()
        return math.Vector2(
            thrust.x - viscosity.x,
            thrust.y - weight.y - viscosity.y
        )

    def _get_acceleration(self):
        force = self._get_resultant_force()
        return pygame.math.Vector2(force.x / self.mass, force.y / self.mass)

    def update(self, dt):
        self.acc = self._get_acceleration()
        self.vel += self.acc * dt
        self.pos += self.vel * dt