import pygame

from src.utils.misc import fonts, colors
from src.utils.constants import WIDTH, HEIGHT, INITIAL_FUEL
from src.models.surface import Surface
from src.models.particle import Particle, ExplosionParticle

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

rocket_image = pygame.image.load("./assets/rocket.png")
rocket_image = pygame.transform.scale(rocket_image, (126, 126))
exploded = False

def game(engine, rocket, ground, particles, explosion, screen):
    global exploded
    
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
    pygame.draw.rect(screen, colors["brown"], (ground.pos[0], HEIGHT - ground.height - camera_offset_y, ground.width, ground.height + 300))

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
    if rocket.launched and rocket.engine.fuel > 0 and rocket.engine.active and not rocket.crashed:
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
            explosion.append(ExplosionParticle(WIDTH // 2 - 10, HEIGHT - ground.height - camera_offset_y))

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
    if rocket.launched and (rocket.pos[0] + rocket.height >= HEIGHT - ground.height) and not rocket.landed:
        if rocket.check_landing():
            message = fonts["subtitle"].render("Pouso bem-sucedido!", True, colors["green"])
        else:
            # Velocidade muito alta não pode pousar!
            message = fonts["subtitle"].render("Você explodiu!", True, colors["red"])

        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))

    pygame.display.flip()