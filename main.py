import pygame
import sys

from settings import colors
from rocket import Rocket
from engines import EngineModel1, EngineModel2

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulador")

e = EngineModel1(900)
r = Rocket(400, 290, 90, e)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    screen.fill(colors["lightblue"])  

    pygame.draw.rect(screen, colors["white"], (r.pos[0], r.pos[0], r.width, r.height))
    pygame.display.flip()
