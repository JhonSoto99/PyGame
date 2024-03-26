from enum import Enum

import pygame
import random
import sys

# Dimensiones de la pantalla
WIDTH = 700
HEIGHT = 700

# Colores
class Color(Enum):
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    GREEN = (0, 200, 0)

# Velocidad del juego
GAME_SPEED = 55

# Velocidad del jugador
PLAYER_SPEED = 7

# Cantidad de modenas y enemigos
NUMBER_COINS = 10
NUMBER_ENEMIES = 5

# Definición de la clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Crear la imagen del jugador
        self.image = pygame.Surface((50, 50))
        self.image.fill(Color.GREEN.value)
        # Obtener el rectángulo del jugador
        self.rect = self.image.get_rect()
        # Posicionar al jugador en el centro de la pantalla
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        # Velocidad del jugador
        self.speed = PLAYER_SPEED

    def update(self):
        # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()
        # Mover al jugador según las teclas presionadas
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        # Mantener al jugador dentro de la pantalla
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.height, self.rect.y))

# Definición de la clase de la moneda
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Crear la imagen de la moneda
        self.image = pygame.Surface((25, 25))
        self.image.fill(Color.YELLOW.value)
        # Obtener el rectángulo de la moneda
        self.rect = self.image.get_rect()
        # Posicionar la moneda en una posición aleatoria en la pantalla
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

# Definición de la clase del enemigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Crear la imagen del enemigo
        self.image = pygame.Surface((30, 30))
        self.image.fill(Color.RED.value)
        # Obtener el rectángulo del enemigo
        self.rect = self.image.get_rect()
        # Posicionar al enemigo en una posición aleatoria en la pantalla
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        # Velocidad del enemigo
        self.speed_x = random.choice([-3, 3])
        self.speed_y = random.choice([-3, 3])

    def update(self):
        # Mover al enemigo y cambiar de dirección si alcanza los límites de la pantalla
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y *= -1

# Función principal del juego
def main():
    # Inicia Pygame
    pygame.init()

    # Crea la pantalla del juego con ciertas especificaciones
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Recolecta Monedas")
    clock = pygame.time.Clock()

    # Crear grupos de sprites para el jugador, las monedas y los enemigos
    all_sprites = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Crear al jugador y agregarlo al grupo de todos los sprites
    player = Player()
    all_sprites.add(player)

    # Crear monedas y enemigos y agregarlos a los grupos correspondientes
    for i in range(NUMBER_COINS):
        coin = Coin()
        coins.add(coin)
        all_sprites.add(coin)

    for i in range(NUMBER_ENEMIES):
        enemy = Enemy()
        enemies.add(enemy)
        all_sprites.add(enemy)

    # Bucle principal del juego
    running = True
    score = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizar todos los sprites
        all_sprites.update()

        # Captura la la cantidad de monedas recolectadas
        # por cada moneda recolectada selecciona una nueva
        hits = pygame.sprite.spritecollide(player, coins, True)
        for hit in hits:
            score += 1
            # Crea una nueva moneda y la agrega al grupo de monedas y de todos los sprites
            coin = Coin()
            coins.add(coin)
            all_sprites.add(coin)

        # Comprobar si el jugador es atrapado por un enemigo
        # de ser así se finaliza el juego.
        if pygame.sprite.spritecollideany(player, enemies):
            running = False

        # Renderizar la pantalla
        screen.fill(Color.BLACK.value)
        all_sprites.draw(screen)
        pygame.display.flip()
        # Velocidad del juego
        clock.tick(GAME_SPEED)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
