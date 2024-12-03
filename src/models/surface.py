"""
Arquivo para a classe da superfície
"""

# Importando biblioteca
import numpy as np

"""
Criando a class da superfície
"""
class Surface:
    def __init__(self, x, y, width, height, color):
        self.pos = np.array([x, y])
        self.width = width
        self.height = height
        self.color = color

    