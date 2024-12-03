import numpy as np
import math

from src.utils.constants import GRAVITY, FUEL_DENSITY
from src.models.engines import RocketEngine
from src.models.atmosphere import air_density, terminal_velocity

class Rocket:
    def __init__(self, x: float, y: float, engine: RocketEngine) -> None:
        self.width: int = 126
        self.height: int = 126
        self.initial_pos = np.array([float(x), float(y)])
        self.pos = np.array([float(x), float(y)])
        self.vel = np.array([0.0, 0.0])
        self.acc = np.array([0.0, 0.0])
        self.mass = 50  # Massa do foguete sem combustível
        self.engine = engine
        self.launched = False
        self.landed = False
        self.crashed = False
        self.lifted = False
        self.dir = 1 # Começa apontando para cima: dir = 1 (positivo), dir = -1 (negativo)

    def launch(self) -> None:
        if not self.launched:
            self.engine.active = True
            self.launched = True
            self.update()

    def swap_active(self) -> None:
        if self.engine.active:
            self.engine.deactivate()
        else:
            self.engine.activate()

    def _get_mass(self):
        return self.mass + (self.engine.fuel * FUEL_DENSITY)

    def _get_weight(self) -> np.ndarray:
        return np.array([-1, 0]) * self._get_mass() * GRAVITY

    def _get_viscosity(self) -> np.ndarray:
        # Calcula a viscosidade conforme a resistencia do ar
        return -self.vel * air_density(self.pos[1] - self.initial_pos[1])

    def _get_terminal_velocity(self) -> float:
        # Calcula a velocidade terminal do foguete
        return terminal_velocity(self._get_mass(), self.width, self.height, self.pos[1])

    def _get_drag(self, thrust: float) -> np.ndarray:
        """
        Calculates the vertical drag force based on the vertical velocity and altitude.
        Drag force naturally opposes motion and scales with velocity squared.
        """

        altitude = self.pos[0]  # Current altitude of the rocket
        max = 0.7*thrust
        min = 0
        vertical_velocity = self.vel[0]

        # If the rocket is stationary in the vertical axis, there is no drag
        if vertical_velocity == 0:
            return np.array([0.0, 0.0])

        # Calculate air density based on altitude
        rho = air_density(altitude)  # kg/m³
        Cd = 0.75  # Drag coefficient (typical for rockets)
        A = self.width * self.height  # Frontal area of the rocket in m²

        # Calculate the drag force
        drag_force_magnitude = 0.5 * Cd * rho * A * vertical_velocity**2

        drag_force_magnitude = np.clip(drag_force_magnitude, min, max)

        # Return drag force as a vector
        return np.array([(-1)*self.dir, 0.0]) * drag_force_magnitude

    def _get_resultant_force(self) -> np.ndarray:
        thrust = self.engine.get_thrust()
        weight = self._get_weight()
        drag = self._get_drag(thrust[0])
        return thrust + weight + drag

    def _get_acceleration(self) -> np.ndarray:
        force = self._get_resultant_force()
        total_mass = self._get_mass()
        acceleration = force / total_mass

        if (acceleration[0] + self.acc[0]) < 0:
            self.dir = -1
        else:
            self.dir = 1
        
        return np.array([1, 0]) * acceleration

    def check_landing(self) -> bool:
        # Ajusta condições do pouso
        self.landed = True
        self.pos = self.initial_pos

        vmin = 200 # Velocidade mínima para explodir

        if self.vel[0] < -vmin:
            self.crashed = True
            return False

        return True

    def update(self) -> None:
        if self.launched and not self.landed:
            self.acc = self._get_acceleration()
            
            self.vel += self.acc  # Atualizando a velocidade com a aceleração
            self.pos += self.vel  # Atualizando a posição com a velocidade


