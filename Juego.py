import pygame
import random
import time
# Inicializar Pygame
pygame.init()

# Configuración de la ventana
largo=pygame.display.Info().current_w
ancho=pygame.display.Info().current_h
screen = pygame.display.set_mode((largo, ancho), pygame.NOFRAME)
pygame.display.set_caption("Juego Transparente")
screen.set_alpha(0)

# Colores
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Clase para las entidades
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 780)
        self.rect.y = random.randint(0, 580)
        self.speed = 2

    def update(self, target_pos):
        dx, dy = target_pos[0] - self.rect.x, target_pos[1] - self.rect.y
        dist = (dx**2 + dy**2) ** 0.5
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

# Clase para los disparos
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=pos)
        self.speed = 5
        self.direction = direction

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        if self.rect.x < 0 or self.rect.x > ancho or self.rect.y < 0 or self.rect.y > largo:
            self.kill()

# Grupos de sprites
entities = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Crear entidades
for _ in range(10):
    entities.add(Entity())

# Bucle principal
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                bullets.add(Bullet(pygame.mouse.get_pos(), (0, -1)))
            elif event.key == pygame.K_s:
                bullets.add(Bullet(pygame.mouse.get_pos(), (0, 1)))
            elif event.key == pygame.K_a:
                bullets.add(Bullet(pygame.mouse.get_pos(), (-1, 0)))
            elif event.key == pygame.K_d:
                bullets.add(Bullet(pygame.mouse.get_pos(), (1, 0)))

    # Actualizar entidades y disparos
    entities.update(pygame.mouse.get_pos())
    bullets.update()

    # Colisiones
    for bullet in bullets:
        hit_entities = pygame.sprite.spritecollide(bullet, entities, True)
        if hit_entities:
            bullet.kill()

    # Dibujar
    screen.fill((0, 0, 0, 0))
    entities.draw(screen)
    bullets.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
