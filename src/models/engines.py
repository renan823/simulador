import numpy as np
import math

from src.utils.constants import GRAVITY, FUEL_DENSITY, ENGINE_NAMES

class RocketEngine:
    def __init__(self, burn_rate: float, mass: float, fuel: float, name: str, fuel_ejection: float, thrust_level: float) -> None:
        self.burn_rate = burn_rate  # Taxa de queima de combustível
        self.mass = mass  # Massa do motor
        self.fuel = fuel  # Combustível inicial
        self.active = False  # Motor inativo por padrão
        self.name = name  # Nome do motor
        self.fuel_ejection = fuel_ejection  # Velocidade de ejeção de combustível (empuxo máximo por unidade de combustível)
        self.thrust_level = thrust_level

    def activate(self) -> None:
        """Ativa o motor"""
        self.active = True

    def deactivate(self) -> None:
        """Desativa o motor"""
        self.active = False

    def _get_total_mass(self) -> float:
        """Retorna a massa total do foguete (motor + combustível restante)"""
        return self.mass + (self.fuel * FUEL_DENSITY)

    def get_thrust(self) -> np.ndarray:
        """
        Calcula o empuxo baseado no combustível restante e taxa de queima.
        O empuxo diminui continuamente conforme o combustível vai sendo consumido.
        """
        # Se não houver mais combustível, não há empuxo
        if self.fuel <= 0 or not self.active:
            return np.array([0.0, 0.0])

        # Empuxo gerado é a combinação da velocidade de ejeção e a taxa de queima
        # A força é proporcional à quantidade de combustível restante
        thrust = np.array([0, 1]) * self.fuel_ejection * self.burn_rate * (self.fuel / self.thrust_level)  # ajuste no thrust_level para controlar o empuxo

        # Reduzindo o combustível com base na taxa de queima, respeitando que não pode ficar negativo
        self.fuel = max(0, self.fuel - self.burn_rate)

        return thrust

class EngineModel1(RocketEngine):
    def __init__(self, fuel):
        super().__init__(0.5, 200, fuel, ENGINE_NAMES[0], 10791, 1000)

class EngineModel2(RocketEngine):
    def __init__(self, fuel):
        super().__init__(0.9, 215, fuel, ENGINE_NAMES[1], 5995, 1000)

class EngineModel3(RocketEngine):
    def __init__(self, fuel):
        super().__init__(3.1, 250, fuel, ENGINE_NAMES[2], 7689, 1000)
