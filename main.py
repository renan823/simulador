import pygame
import sys

from settings import colors
from rocket import Rocket

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulador")

r = Rocket(400, 290)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    screen.fill(colors["lightblue"])  

    pygame.draw.rect(screen, colors["white"], (r.pos.x, r.pos.y, r.width, r.height))
    pygame.display.flip()
