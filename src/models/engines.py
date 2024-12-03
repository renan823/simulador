"""
Arquivo que criamos a classe do motor do foguete e suas funções
"""

# Importando bibliotecas
import numpy as np
import math
from src.utils.constants import GRAVITY, FUEL_DENSITY, ENGINE_NAMES

"""
Criando a classe do motor do foguete
"""
class RocketEngine:
    def __init__(self, burn_rate: float, mass: float, fuel: float, name: str, fuel_ejection: float) -> None:
        self.burn_rate = burn_rate  # Taxa de queima de combustível
        self.mass = mass  # Massa do motor
        self.fuel = fuel  # Combustível inicial
        self.active = False  # Motor inativo por padrão
        self.name = name  # Nome do motor
        self.fuel_ejection = fuel_ejection  # Velocidade de ejeção de combustível (empuxo máximo por unidade de combustível)

    """
    Função que ativa o motor
    """
    def activate(self) -> None:
        self.active = True

    """
    Função que desativa o motor
    """
    def deactivate(self) -> None:
        self.active = False

    """
    Função que calcula a massa total do foguete (motor + combustível restante)
     
    - return: massa total do foguete
    """
    def _get_total_mass(self) -> float:
        return self.mass + (self.fuel * FUEL_DENSITY)

    """
    Função que calcula o empuxo baseado no combustível restante e taxa de queima dele. O empuxo diminue continuamente conforme 
    o combustível vai sendo consumido
    """
    def get_thrust(self, yaw: int) -> np.ndarray:
        # Se não houver mais combustível, não há empuxo
        if self.fuel <= 0 or not self.active:
            return np.array([0.0, 0.0])

        # Calculando o ângulo de direção do motor
        angle = math.radians(yaw)  # Usando math.radians em vez de deg_to_rad

        # Empuxo gerado é a combinação da velocidade de ejeção e a taxa de queima
        # A força é proporcional à quantidade de combustível restante
        thrust = np.array([math.cos(angle), math.sin(angle)]) * self.fuel_ejection * self.burn_rate * (self.fuel / 1000)  # ajuste no divisor para controlar o empuxo

        # Reduzindo o combustível com base na taxa de queima, respeitando que não pode ficar negativo
        self.fuel = max(0, self.fuel - self.burn_rate)

        return thrust

"""
Cria classe do motor 1
"""
class EngineModel1(RocketEngine):
    def __init__(self, fuel):
        super().__init__(0.5, 200, fuel, ENGINE_NAMES[0], 10791)

"""
Cria classe do motor 2
"""
class EngineModel2(RocketEngine):
    def __init__(self, fuel):
        super().__init__(0.9, 215, fuel, ENGINE_NAMES[1], 5995)

"""
Cria classe do motor 3
"""
class EngineModel3(RocketEngine):
    def __init__(self, fuel):
        super().__init__(3.1, 250, fuel, ENGINE_NAMES[2], 7689)
