import numpy as np
import math

from src.utils.constants import GRAVITY, FUEL_DENSITY
from src.models.engines import RocketEngine
from src.models.atmosphere import air_density, terminal_velocity

class Rocket:
    def __init__(self, x: float, y: float, yaw: int, engine: RocketEngine) -> None:
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
        self.yaw = yaw
        self.angular_velocity = 5

    def launch(self):
        if not self.launched:
            self.engine.active = True
            self.launched = True
            self.update()

    def swap_active(self):
        if self.engine.active:
            self.engine.deactivate()
        else:
            self.engine.activate()

    def _get_mass(self):
        return self.mass + (self.engine.fuel * FUEL_DENSITY)

    def _get_weight(self) -> np.ndarray:
        angle = math.radians(self.yaw)  # Usando math.radians em vez de deg_to_rad
        return np.array([math.cos(angle), math.sin(angle)]) * self._get_mass() * GRAVITY

    def _get_viscosity(self) -> np.ndarray:
        # Calcula a viscosidade conforme a resistencia do ar
        return -self.vel * air_density(self.pos[1] - self.initial_pos[1])

    def _get_terminal_velocity(self) -> float:
        # Calcula a velocidade terminal do foguete
        return terminal_velocity(self._get_mass(), self.width, self.height, self.pos[1])

    def _get_drag(self) -> np.ndarray:
        # Calcula a força de arrasto baseada na velocidade e altitude
        velocity_magnitude = np.linalg.norm(self.vel)  # Magnitude da velocidade
        if velocity_magnitude == 0:
            return np.array([0.0, 0.0])  # Se a velocidade for zero, não há arrasto

        altitude = self.pos[1]  # Altitude do foguete
        rho = air_density(altitude)  # Densidade do ar baseada na altitude
        mu = 1.81e-5  # Viscosidade dinâmica do ar a 15°C (Pa.s)
        L = self.width  # Largura do foguete

        # Cálculo do número de Reynolds
        Re = (rho * velocity_magnitude * L) / mu

        # Evita a divisão por zero
        if Re == 0:
            Cd = 0.5  # Valor padrão para fluxo laminar ou em repouso
        elif Re < 2000:
            # Para fluxo laminar (Re < 2000)
            Cd = 24 / Re
        else:
            # Para fluxo turbulento (Re >= 2000)
            Cd = 0.75  # Valor típico de Cd para um foguete retangular

        # Área frontal do foguete (m²)
        A = self.width * self.height

        # Fórmula do arrasto
        drag_force = 0.5 * Cd * rho * A * velocity_magnitude**2

        # Aceleração devido ao arrasto
        drag_acceleration = drag_force / self._get_mass()  # Aceleração devido ao arrasto
        drag_vector = -drag_acceleration * (self.vel / velocity_magnitude)  # Direção oposta à velocidade

        return drag_vector

    def _get_resultant_force(self) -> np.ndarray:
        thrust = self.engine.get_thrust(self.yaw)
        weight = self._get_weight()
        drag = self._get_drag()
        return - thrust + weight + drag

    def _get_acceleration(self) -> np.ndarray:
        force = self._get_resultant_force()
        total_mass = self._get_mass()
        acceleration = force / total_mass
        return np.array([math.cos(math.radians(self.yaw)), math.sin(math.radians(self.yaw))]) * acceleration

    def check_landing(self):
        # Ajusta condições do pouso
        self.landed = True
        self.pos = self.initial_pos

        # Usa a vel terminal para verificar pouso
        tvel = self._get_terminal_velocity()

        if self.vel[0] >= tvel:
            self.crashed = True
            return False

        return True

    def update(self) -> None:
        if self.launched and not self.landed:
            self.acc = self._get_acceleration()
            self.vel += self.acc  # Atualizando a velocidade com a aceleração
            self.pos += self.vel  # Atualizando a posição com a velocidade

            # Calculando a velocidade terminal
            tvel = self._get_terminal_velocity()

            print(self.vel[0], tvel)

            # Limitar a velocidade máxima a uma margem da velocidade terminal
            if self.vel[0] > tvel:
                direction = self.vel / np.linalg.norm(self.vel)  # Normaliza a direção da velocidade
                self.vel = direction * tvel  # Limita a velocidade
