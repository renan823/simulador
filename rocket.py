from settings import GRAVITY, FUEL_DENSITY
from engines import RocketEngine
from atmosphere import air_density, terminal_velocity
from utils import deg_to_rad
import numpy as np
import math

class Rocket:
    def __init__(self, x: float, y: float, yaw: int, engine: RocketEngine) -> None:
        self.width: int = 20
        self.height: int = 100
        self.initial_pos = np.array([float(x), float(y)])
        self.pos = np.array([float(x), float(y)])
        self.vel = np.array([0.0, 0.0])
        self.acc = np.array([0.0, 0.0])
        self.mass = 50  # Massa do foguete sem combustível
        self.engine = engine
        self.launched = False
        self.landed = False
        self.crashed = False
        self.yaw = yaw

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

    def _get_weight(self) -> np.ndarray:
        angle = deg_to_rad(self.yaw)
        total_mass = self.mass + (self.engine.fuel * FUEL_DENSITY)
        return np.array([math.cos(angle), math.sin(angle)]) * total_mass * GRAVITY

    def _get_viscosity(self) -> np.ndarray:
        # Calcula a viscosidade conforme a resistencia do ar
        return -self.vel * air_density(self.pos[1] - self.initial_pos[1])

    def _get_terminal_velocity(self) -> float:
        # Calcula a velocidade terminal do foguete
        return terminal_velocity(self.mass, self.width, self.height, self.pos[1])

    # Função gerada por IA
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
        drag_acceleration = drag_force / (self.mass + (self.engine.fuel * FUEL_DENSITY))  # Aceleração devido ao arrasto
        drag_vector = -drag_acceleration * (self.vel / velocity_magnitude)  # Direção oposta à velocidade

        return drag_vector

    def _get_resultant_force(self) -> np.ndarray:
        thrust = self.engine.get_thrust(self.yaw)
        weight = self._get_weight()
        drag = self._get_drag()
        return - thrust + weight + drag

    def _get_acceleration(self) -> np.ndarray:
        force = self._get_resultant_force()
        total_mass = self.mass + (self.engine.fuel * FUEL_DENSITY)
        acceleration = force / total_mass
        return acceleration

    def update(self) -> None:
        if self.crashed:
            self.engine.deactivate()

        if self.launched and not self.landed:
            self.acc = self._get_acceleration()
            self.vel += self.acc  # Atualiza a velocidade com a aceleração
            self.pos += self.vel  # Atualiza a posição com a velocidade

            # Verificar se atingiu a velocidade terminal 
            mag = np.linalg.norm(self.vel)
            tv = self._get_terminal_velocity()

            if mag > tv:
                # Limitar a velocidade 
                self.vel = (self.vel / mag) * tv
