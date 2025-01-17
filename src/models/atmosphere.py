"""
Arquivo com as funções relacionadas à atmosfera, cada um dos seus níveis, densidades, etc
"""

# Importando bibliotecas
import numpy as np
import math
from src.utils.constants import GRAVITY, R, T0, P0, L_tropo, T_tropo

'''
Essas funções foram geradas usando inteligência artificial e adaptadas
para atender as necessidades do projeto.
Usando o chatGPT, os prompts foram:
    - como calcular a densidade do ar em cada altitude?

    - preciso de uma função em python para calcular a resistencia do ar 
        (será usada na viscosidade) do meu foguete. o foguete tem valocidade, pos, etc

    - considerando um foguete com design retangular, sem pontas. Como determinar o 
        coeficiente de arrasto? Esse valor pode ser encontrado assim? Considere que 
        o foguete também tem os atributos width e heigth

    - considerando uma densidade do ar variável, como podemos obter esse valor?

    - e como lidar com valores maiores que a troposfera? Realize o ajuste para valores maiores tbm
'''

"""
Função que calcula a densidade do ar para cada uma das altitudes, até 86 km

- altitude: altitude do foguete em metros
- return: densidade do ar
"""
def air_density(altitude):
    # Troposfera: 0 a 11 km
    if altitude <= 11000:
        T = T0 - L_tropo * altitude
        P = P0 * (1 - (L_tropo * altitude) / T0) ** (GRAVITY / (R * L_tropo))

    # Estratosfera inferior: 11 a 20 km (temperatura constante)
    elif 11000 < altitude <= 20000:
        T = T_tropo
        P11 = P0 * (1 - (L_tropo * 11000) / T0) ** (g / (R * L_tropo))
        P = P11 * math.exp(-GRAVITY * (altitude - 11000) / (R * T))

    # Estratosfera superior: 20 a 47 km (temperatura aumenta linearmente)
    elif 20000 < altitude <= 47000:
        L_strato = 0.001  # Gradiente térmico na estratosfera superior (K/m)
        T = T_tropo + L_strato * (altitude - 20000)
        P20 = P11 * math.exp(-GRAVITY * (20000 - 11000) / (R * T_tropo))
        P = P20 * (1 + L_strato * (altitude - 20000) / T_tropo) ** (-g / (R * L_strato))

    # Mesosfera inferior: 47 a 86 km (temperatura decresce linearmente)
    elif 47000 < altitude <= 86000:
        L_meso = -0.00299  # Gradiente térmico na mesosfera (K/m)
        T = 282.65 + L_meso * (altitude - 47000)
        P47 = P20 * (1 + L_strato * (47000 - 20000) / T_tropo) ** (-GRAVITY / (R * L_strato))
        P = P47 * (1 + L_meso * (altitude - 47000) / 282.65) ** (-GRAVITY / (R * L_meso))

    # Termosfera: acima de 86 km (densidade aproximada)
    elif altitude > 86000:
        # Valores aproximados baseados em tabelas empíricas
        T = 186.87  # Temperatura mínima constante (K)
        P = 0  # Pressão quase zero a partir dessa altitude
        density = 1e-6  # Densidade muito baixa (kg/m³)

    else:
        raise ValueError("Altitude fora do intervalo esperado.")

    # Para altitudes dentro da faixa modelada, calcular densidade
    if altitude <= 86000:
        density = P / (R * T)

    return density

"""
Função que estima o coeficiente de arrasto (C_d) para um foguete, consideramos um modelo retangular para facilitar os cálculos

- width: largura do foguete
- height: altura do foguete
- return: coeficiente de arrasto estimado
"""
def drag_coefficient(width, height):
    base_cd = 1.2  # C_d base para formas retangulares básicas.
    aspect_ratio = width / height
    additional_cd = 0.5 * aspect_ratio
    return base_cd + additional_cd

"""
Função que calcula a força de resistência do ar para um foguete em função da altitude

- altitude: altitude do foguete
- velocity: velocidade do foguete
- width: largura do foguete
- height: altura do foguete
- return: força de arrasto do foguete
"""
def air_resistance(altitude, velocity, width, height):
    density = air_density(altitude)
    drag_coefficient = drag_coefficient(width, height)
    frontal_area = width * height
    drag_force = 0.5 * density * velocity**2 * drag_coefficient * frontal_area
    return drag_force

"""
Função que calcula a velocidade terminal como vetor

- mass: massa do foguete
- width: largura do foguete
- height: altura do foguete
- altitude: altitude do foguete
- return: velocidade terminal do foguete
"""
def terminal_velocity(mass, width, height, altitude):
    A = width * height /200 # Área frontal do foguete (m²)
    
    # Obter densidade do ar (ρ)
    rho = air_density(altitude)
    
    # Calcular coeficiente de arrasto (C_d)
    Cd = drag_coefficient(width, height)
    
    if rho <= 0 or Cd <= 0:
        raise ValueError("Parâmetros inválidos para densidade ou coeficiente de arrasto.")
    
    # Fórmula da velocidade terminal
    return math.sqrt((2 * mass * GRAVITY) / (Cd * rho * A))
    