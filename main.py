import pygame
import sys
import numpy as np
import time

from src.utils.constants import WIDTH, HEIGHT, INITIAL_FUEL
from src.models.rocket import Rocket
from src.models import engines, surface
from src.utils.misc import colors
from src.screens.menu import menu
from src.screens.game import game

# ------------------------------------- Inicializar -------------------------------------
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Foguetes")

MENU = "menu"
GAME = "game"
SCREEN = MENU


'''
Inicialização dos objetos rocket e engine.
Eles só serão criados após o menu inicial.
Inicializa tbm o chão
'''
engine = None
rocket = None
ground = surface.Surface(0, HEIGHT - 50, WIDTH, 50, colors["brown"])

'''
Inicialização das partículas
'''
particles = [] 
explosion = []

# -------------------------------------------- Telas --------------------------------------------

def main() -> None:
    global engine, rocket, ground, particles, explosion, screen, SCREEN

    clock = pygame.time.Clock()  # Cria um relógio para controlar o FPS
    start_time = None  # Marca o tempo inicial

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if SCREEN == MENU:
                    # Escolhe o tipo do motor (1, 2 ou 3)
                    if event.key == pygame.K_1:
                        engine = engines.EngineModel1(INITIAL_FUEL)
                    if event.key == pygame.K_2:
                        engine = engines.EngineModel2(INITIAL_FUEL)
                    if event.key == pygame.K_3:
                        engine = engines.EngineModel3(INITIAL_FUEL)

                if SCREEN == GAME:
                    if rocket is not None:
                        if event.key == pygame.K_SPACE:
                            if rocket.launched:
                                # Permite ligar/desligar o motor uma vez que ele foi iniciado
                                rocket.swap_active()
                            else:
                                rocket.launch()  # Inicia o foguete
                                start_time = pygame.time.get_ticks()  # Marca o tempo de início
    
                            if rocket.landed and not rocket.crashed:
                                rocket.landed = False
        # Mudança de tela
        if engine is not None and rocket is None:
            initial_y = HEIGHT - ground.height - 126
            initial_x = (WIDTH - 126) // 2
            rocket = Rocket(initial_y, initial_x, 0, engine)
            SCREEN = GAME

        if SCREEN == MENU:
            menu(screen)
        elif SCREEN == GAME:
            # Controla a mudança de tela
            if engine is not None and rocket is not None:
                if rocket.launched:
                    rocket.update()
                game(engine, rocket, ground, particles, explosion, screen)
            else:
                SCREEN = MENU
        clock.tick(60)

if __name__ == '__main__':
    main()
