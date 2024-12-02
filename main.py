import pygame
import sys
import numpy as np

from settings import colors, ENGINE_NAMES, INITIAL_FUEL
from rocket import Rocket
from particle import Particle, ExplosionParticle
import engines

# ------------------------------------- Global Variables and pygame init -------------------------------------
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
Eles só serão criados após o menu inicial.
'''
engine = None
rocket = None

'''
Inicialização das partículas
'''
particles = [] 
explosion = []
exploded = False

'''
Definição da tela MENU
No menu, o jogador pode escolher o tipo de motor que vai usar
'''
CARD_WIDTH, CARD_HEIGHT = 250, 350

'''
Carregando imagem do foguete
'''
rocket_image = pygame.image.load("./assets/rocket.png")
rocket_image = pygame.transform.scale(rocket_image, (126, 126))
# -------------------------------------------- Functions --------------------------------------------
def interpolate_color(color1, color2, factor):
    return (
        int(color1[0] + (color2[0] - color1[0]) * factor),
        int(color1[1] + (color2[1] - color1[1]) * factor),
        int(color1[2] + (color2[2] - color1[2]) * factor)
    )

def get_background(altitude):
    if altitude <= 11000:  # Troposfera
        return colors["lightblue"]
    elif 11000 < altitude <= 20000:  # Estratosfera inferior
        factor = (altitude - 11000) / (20000 - 11000)
        return interpolate_color(colors["lightblue"], colors["darkblue1"], factor)
    elif 20000 < altitude <= 47000:  # Estratosfera superior
        factor = (altitude - 20000) / (47000 - 20000)
        return interpolate_color(colors["darkblue1"], colors["darkblue2"], factor)
    elif 47000 < altitude <= 86000:  # Mesosfera inferior
        factor = (altitude - 47000) / (86000 - 47000)
        return interpolate_color(colors["darkblue2"], colors["darkblue3"], factor)
    else:  # Termosfera
        factor = min((altitude - 86000) / 10000, 1)
        return interpolate_color(colors["darkblue3"], colors["darkblue4"], factor)


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

        # Escreve a tecla para pressionar
        instruction = fonts["message"].render(f"Press {i + 1}", True, colors["white"])
        text_x = x + (CARD_WIDTH - instruction.get_width()) // 2
        text_y = y + (CARD_HEIGHT - instruction.get_height()) - 20

        screen.blit(instruction, (text_x, text_y))

    pygame.display.flip()


def game():
    global rocket, particles, explosion, exploded

    # Calcula o offset da câmera
    camera_offset_y = rocket.pos[0] - (HEIGHT // 2 - rocket.height // 2)

    # Tela do jogo
    altitude = HEIGHT - rocket.pos[0]
    background = get_background(altitude)
    screen.fill(background)

    # Escreve informações na tela
    if altitude <= 86000:
        positions = fonts["message"].render(f"X: {round(rocket.pos[1] - 437, 2)}  Y: {round(rocket.pos[0] - HEIGHT + 150, 2) * -1}", True, colors["black"])
        vel = fonts["message"].render(f"Vel: {round(rocket.vel[0], 4) * -1}", True, colors["black"])
        acc = fonts["message"].render(f"Acc: {round(rocket.acc[0], 4) * -1}", True, colors["black"])
    else:
        positions = fonts["message"].render(f"X: {round(rocket.pos[1] - 437, 2)}  Y: {round(rocket.pos[0] - HEIGHT + 150, 2) * -1}", True,colors["white"])
        vel = fonts["message"].render(f"Vel: {round(rocket.vel[0], 4) * -1}", True, colors["white"])
        acc = fonts["message"].render(f"Acc: {round(rocket.acc[0], 4) * -1}", True, colors["white"])

    screen.blit(positions, (20, 20))
    screen.blit(vel, (20, 40))
    screen.blit(acc, (20, 60))

    # Escreve nome do motor
    if altitude <= 86000:
        positions = fonts["message"].render(f"{rocket.engine.name} engine", True, colors["black"])

    else:
        positions = fonts["message"].render(f"{rocket.engine.name} engine", True, colors["white"])
    screen.blit(positions, (20, 80))

    # Desenha o chão (só se estiver na câmera)
    ground_height = 50
    pygame.draw.rect(screen, colors["brown"], (0, HEIGHT - ground_height - camera_offset_y, WIDTH, ground_height + 300))

    # Desenha o tanque de combustível
    pygame.draw.rect(screen, colors["gray"], (WIDTH - 40, HEIGHT - 480, 20, 450))

    # Desenha a barra de combustível (proporcional)
    bar_height = 440
    fuel_bar_height = int(bar_height * rocket.engine.fuel / INITIAL_FUEL)
    bar_y = HEIGHT - 475 + (bar_height - fuel_bar_height)
    pygame.draw.rect(screen, colors["green"], (WIDTH - 35, bar_y, 10, fuel_bar_height))

    # Escreve a porcentagem de combustível
    fuel_amount = fonts["message"].render(f"{rocket.engine.fuel / INITIAL_FUEL * 100 : .1f}%", True, colors["black"])
    text_x = WIDTH - 35 - (fuel_amount.get_width() // 2) + 5
    screen.blit(fuel_amount, (WIDTH - 60, HEIGHT - 20))

    # Desenha o foguete (se ele não bateu)
    if not rocket.crashed:
        screen.blit(rocket_image, (rocket.pos[1], rocket.pos[0] - camera_offset_y))

    # Cria partículas
    if rocket.launched and rocket.engine.fuel > 0 and rocket.engine.active:
        for _ in range(5):
            particles.append(Particle(rocket.pos[1] + rocket.width // 2, rocket.pos[0] - camera_offset_y + rocket.height))

    # Desenha partículas
    for particle in particles:
        particle.move()
        pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), particle.size)

        if particle.lifetime <= 0:
            particles.remove(particle)

    if rocket.crashed and not exploded:
        # Inicia a explosão
        exploded = True
        for _ in range(30):  # Criar mais partículas de explosão
            explosion.append(ExplosionParticle(WIDTH // 2 - 10, HEIGHT - ground_height - camera_offset_y))

    # Desenha explosão
    for particle in explosion:
        particle.move()

        # Ajusta a opacidade e desenha
        particle_color = (particle.color[0], particle.color[1], particle.color[2], particle.alpha)
        pygame.draw.circle(screen, particle_color, (int(particle.x), int(particle.y)), particle.size)

        if not particle.is_alive():
            explosion.remove(particle)
    
    # Verifica se o foguete atingiu o chão
    # FALTA AJUSTAR ISSO AQUI (DO JEITO Q TÁ ELE NUNCA VAI EXPLODIR)
    if rocket.launched and (rocket.pos[0] + rocket.height >= HEIGHT - ground_height):
        if rocket.check_landing():  
            message = fonts["subtitle"].render("Pouso bem-sucedido!", True, colors["green"])
        else:
            # Velocidade muito alta não pode pousar!
            message = fonts["subtitle"].render("Você explodiu!", True, colors["red"])
        
        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))
        

    pygame.display.flip()

def main() -> None:
    global engine, rocket, SCREEN

    clock = pygame.time.Clock()  # Cria um relógio para controlar o FPS
    start_time = None  # Marca o tempo inicial
    dt = None

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

                if SCREEN == GAME and event.key == pygame.K_SPACE:
                    if rocket is not None:
                        if rocket.launched:
                            # Permite ligar/desligar o motor uma vez que ele foi iniciado
                            rocket.swap_active()
                        else:
                            rocket.launch()  # Inicia o foguete
                            start_time = pygame.time.get_ticks()  # Marca o tempo de início

        # Mudança de tela
        if engine is not None and rocket is None:
            ground_height = 50
            initial_y = HEIGHT - ground_height - 126
            initial_x = (WIDTH - 126) // 2
            rocket = Rocket(initial_y, initial_x, 0, engine)
            SCREEN = GAME
        # Calcula o delta time (tempo decorrido desde o último quadro)
        current_time = pygame.time.get_ticks()

        if rocket and rocket.launched:
            dt = (current_time - start_time) / 1000.0  # Em segundos

        if SCREEN == MENU:
            menu()
        elif SCREEN == GAME:
            # Controla a mudança de tela
            if engine is not None and rocket is not None:
                if rocket.launched:
                    rocket.update()
                game()
            else:
                SCREEN = MENU

        clock.tick(60)

if __name__ == '__main__':
    main()
