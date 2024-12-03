import pygame

from src.utils.misc import fonts, colors
from src.utils.constants import ENGINE_NAMES, WIDTH, HEIGHT

CARD_WIDTH, CARD_HEIGHT = 250, 350

def menu(screen):
    # Tela inicial
    screen.fill(colors["black"])

    # Titulo
    title = fonts["title"].render("Simulador de foguete!", True, colors["white"])
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 7 - title.get_height() // 2))

    # Instruções
    subtitle = fonts["subtitle"].render("Escolha o motor para seu foguete", True, colors["white"])
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

        # Escreve a tecla para pressionar
        instruction = fonts["message"].render(f"Aperte {i + 1}", True, colors["white"])
        text_x = x + (CARD_WIDTH - instruction.get_width()) // 2
        text_y = y + (CARD_HEIGHT - instruction.get_height()) - 20

        screen.blit(instruction, (text_x, text_y))

    pygame.display.flip()