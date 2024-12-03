import random
from src.utils.misc import colors

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 6)
        self.color = random.choice([colors["orange"], colors["amber"], colors["dark-orange"]])
        self.speed_x = random.uniform(-1.3, 1.3)  
        self.speed_y = random.uniform(1, 4)
        self.lifetime = random.randint(20, 40)  

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1


class ExplosionParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice([colors["orange"], colors["amber"], colors["dark-orange"]])
        self.size = random.randint(80, 120)
        self.lifetime = random.randint(50, 90) 
        self.vel_x = random.uniform(-2, 2)  
        self.vel_y = random.uniform(-1, -3)  
        self.alpha = 255  

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

        self.vel_y += 0.01

        self.alpha -= 1

        self.lifetime -= 1

    def is_alive(self):
        return self.alpha > 0 and self.lifetime > 0