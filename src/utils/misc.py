"""
Configurações e constantes do estilo do jogo, como cores e fontes
"""
import pygame

pygame.init()

colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "cyan": (0, 255, 255),
    "lightblue": (86, 156, 228),
    "darkblue1": (2, 121, 213),
    "darkblue2": (35, 89, 159),
    "darkblue3": (23, 66, 117),
    "darkblue4": (11, 38, 67),
    "magenta": (255, 0, 255),
    "green": (0, 255, 0),
    "gray": (130, 130, 130),
    "brown": (155, 103, 60),
    "red": (255, 0, 0),
    "orange": (249,115,22),
    "yellow": (255, 255, 0),
    "dark-orange": (194,65,12),
    "amber": (245,158,11),
}

fonts = {
    'title': pygame.font.Font(None, 74),
    'subtitle': pygame.font.Font(None, 36),
    'message': pygame.font.Font(None, 24)
}
