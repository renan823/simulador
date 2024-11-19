import pygame
import sys

from settings import colors, ENGINE_NAMES, INITIAL_FUEL
from rocket import Rocket
import engines

pygame.init()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador")

MENU = "menu"
GAME = "game"
SCREEN = MENU

fonts = {
    'title': pygame.font.Font(None, 74),
    'subtitle': pygame.font.Font(None, 36),
    'message': pygame.font.Font(None, 24)
}

'''
Inicialização dos objetos rocket e engine.
Eles sõ serão criados após o menu inicial.
'''
engine = None
rocket = None


'''
Definição da tela MENU
No menu, o jogar pode escolher o tipo de motor que vai usar
'''
CARD_WIDTH, CARD_HEIGHT = 250, 350

def menu():
    # Tela inicial
    screen.fill(colors["black"]) 

    # Titulo
    title = fonts["title"].render("Rocket Simulator", True, colors["white"])
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 7 - title.get_height() // 2))

    # Instruções
    subtitle = fonts["subtitle"].render("Choose your rocket's engine!", True, colors["white"])
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 5 - subtitle.get_height() // 2))

    # Loop para criar os seletores de motor
    spacing = (WIDTH - 3 * CARD_WIDTH) // 4
    for i, name in enumerate(ENGINE_NAMES):
        x = spacing + i * (CARD_WIDTH + spacing)
        y = (HEIGHT - CARD_HEIGHT) // 2

        # Desenha o card
        pygame.draw.rect(screen, colors["magenta"], (x, y, CARD_WIDTH, CARD_HEIGHT))

        # Escreve o texto/nome 
        card_text = fonts["subtitle"].render(name, True, colors["white"])
        text_x = x + (CARD_WIDTH - card_text.get_width()) // 2
        text_y = y + (CARD_HEIGHT - card_text.get_height()) // 2

        screen.blit(card_text, (text_x, text_y))

        # Escreve a tecla pra pressinoar
        instruction = fonts["message"].render(f"Press {i+1}", True, colors["white"])
        text_x = x + (CARD_WIDTH - instruction.get_width()) // 2
        text_y = y + (CARD_HEIGHT - instruction.get_height()) - 20

        screen.blit(instruction, (text_x, text_y))


    pygame.display.flip()
    
def game():
    # Tela do jogo
    screen.fill(colors["lightblue"])  

    # Escreve informações na tela
    positions = fonts["message"].render(f"X: {rocket.pos[0]}  Y: {rocket.pos[1]}", True, colors["black"])
    screen.blit(positions, (20, 20))

    # Escreve nome do motor
    positions = fonts["message"].render(f"{rocket.engine.name} engine", True, colors["black"])
    screen.blit(positions, (20, 40))

    # Desenha o tanque de combustivel
    pygame.draw.rect(screen, colors["gray"], (WIDTH - 40, HEIGHT - 480, 20, 450))

    # Desenha a barra de combustivel (proporcional)
    bar_height = 440
    fuel_bar_height = int(bar_height * rocket.engine.fuel / INITIAL_FUEL)
    bar_y = HEIGHT - 475 + (bar_height - fuel_bar_height)
    pygame.draw.rect(screen, colors["green"], (WIDTH - 35, bar_y, 10, fuel_bar_height))

    # Escreve a porcentagem de combustivel 
    fuel_amount = fonts["message"].render(f"{rocket.engine.fuel / INITIAL_FUEL * 100 : .1f}%", True, colors["black"])
    text_x = WIDTH - 35 - (fuel_amount.get_width() // 2) + 5 
    screen.blit(fuel_amount, (WIDTH - 60, HEIGHT - 20))

    # Desenha o foguete
    pygame.draw.rect(screen, colors["white"], (rocket.pos[0], rocket.pos[1], rocket.width, rocket.height))
    pygame.display.flip()

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

    # Mudança de tela
    if engine != None:
        rocket = Rocket(WIDTH // 2 - 10, HEIGHT - 150, 0, engine)
        SCREEN = GAME

    if SCREEN == MENU:
        menu()
    
    elif SCREEN == GAME:
        # Controla a mudança de tela
        if engine != None and rocket != None:
            game()
        else:
            SCREEN = MENU