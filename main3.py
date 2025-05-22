import asyncio
import platform
import pygame
import sys
import random
import math

pygame.init()

# Настройки окна
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Игра v2.1")

# Загрузка изображений
fon = pygame.image.load("fon.png")
back_fon = pygame.transform.scale(fon, (window_width, window_height))

# Цвета для победного экрана
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Шрифт для текста
pygame.font.init()
font = pygame.font.SysFont('Arial', 48)
button_font = pygame.font.SysFont('Arial', 36)


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, filename, x=100, y=250):
        super().__init__()
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.speed = 5

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Ограничение движения в пределах окна
        self.rect.x = max(0, min(self.rect.x, window_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, window_height - self.rect.height))


# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        super().__init__()
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.change_direction_time = pygame.time.get_ticks()
        self.direction_change_interval = 1000  # Менять направление каждые 1000 мс
        self.x_direction = random.choice([-1, 1])
        self.y_direction = random.choice([-1, 1])

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.change_direction_time > self.direction_change_interval:
            # Случайное изменение направления
            self.x_direction = random.choice([-1, 0, 1])
            self.y_direction = random.choice([-1, 0, 1])
            # Нормализация скорости, чтобы враг не двигался слишком быстро по диагонали
            if self.x_direction != 0 or self.y_direction != 0:
                length = math.sqrt(self.x_direction ** 2 + self.y_direction ** 2)
                self.x_direction /= max(1, length)
                self.y_direction /= max(1, length)
            self.change_direction_time = current_time

        self.rect.x += self.speed * self.x_direction
        self.rect.y += self.speed * self.y_direction

        # Ограничение движения врагов в пределах окна с отскоком
        if self.rect.right > window_width:
            self.rect.right = window_width
            self.x_direction = -abs(self.x_direction)
        elif self.rect.left < 0:
            self.rect.left = 0
            self.x_direction = abs(self.x_direction)
        if self.rect.bottom > window_height:
            self.rect.bottom = window_height
            self.y_direction = -abs(self.y_direction)
        elif self.rect.top < 0:
            self.rect.top = 0
            self.y_direction = abs(self.y_direction)


# Класс стрелы
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.image.load("arrow.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.direction = direction  # 1 - вправо, -1 - влево

    def update(self):
        self.rect.x += self.speed * self.direction
        # Удаление стрелы при выходе за границы экрана
        if self.rect.left > window_width or self.rect.right < 0:
            self.kill()


# Создание спрайтов
hero = Player("valorant.png")
enemy1 = Enemy("skelet.png", 300, 100)
enemy2 = Enemy("skelet.png", 500, 400)

# Группы спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
arrows = pygame.sprite.Group()

all_sprites.add(hero, enemy1, enemy2)
enemies.add(enemy1, enemy2)

# Основной игровой цикл
clock = pygame.time.Clock()
FPS = 60
running = True
sdvig_fona = 0
background_speed = 0
game_won = False

# Прямоугольник для кнопки "Ура"
button_rect = pygame.Rect(window_width // 2 - 50, window_height // 2 + 50, 100, 50)


async def main():
    global running, sdvig_fona, background_speed, game_won
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_won:
                # Управление героем
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        hero.x_speed = -hero.speed
                    elif event.key == pygame.K_RIGHT:
                        hero.x_speed = hero.speed
                    elif event.key == pygame.K_UP:
                        hero.y_speed = -hero.speed
                    elif event.key == pygame.K_DOWN:
                        hero.y_speed = hero.speed
                    elif event.key == pygame.K_SPACE:
                        direction = 1 if hero.x_speed >= 0 else -1
                        arrow = Arrow(hero.rect.centerx, hero.rect.centery, direction)
                        arrows.add(arrow)
                        all_sprites.add(arrow)

                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        hero.x_speed = 0
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        hero.y_speed = 0
            else:
                # Обработка нажатия на кнопку "Ура"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect.collidepoint(event.pos):
                        running = False

        if not game_won:
            # Движение фона
            if hero.rect.left <= 0 and hero.x_speed < 0:
                background_speed = hero.speed
            elif hero.rect.right >= window_width and hero.x_speed > 0:
                background_speed = -hero.speed
            else:
                background_speed = 0

            sdvig_fona = (sdvig_fona + background_speed) % window_width

            # Обновление спрайтов
            all_sprites.update()

            # Проверка коллизий стрел с врагами
            hits = pygame.sprite.groupcollide(arrows, enemies, True, True)
            for hit in hits:
                all_sprites.remove(hit)

            # Проверка победы
            if len(enemies) == 0:
                game_won = True

        # Отрисовка
        window.blit(back_fon, (sdvig_fona, 0))
        if sdvig_fona != 0:
            window.blit(back_fon, (sdvig_fona - window_width, 0))

        # Отрисовка всех спрайтов
        all_sprites.draw(window)

        # Отрисовка победного экрана
        if game_won:
            # Полупрозрачный фон
            overlay = pygame.Surface((window_width, window_height))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            window.blit(overlay, (0, 0))

            # Текст победы
            victory_text = font.render("Победа!", True, WHITE)
            text_rect = victory_text.get_rect(center=(window_width // 2, window_height // 2 - 50))
            window.blit(victory_text, text_rect)

            # Кнопка "Ура"
            pygame.draw.rect(window, GRAY, button_rect)
            button_text = button_font.render("Ура", True, WHITE)
            button_text_rect = button_text.get_rect(center=button_rect.center)
            window.blit(button_text, button_text_rect)

        pygame.display.flip()
        await asyncio.sleep(1.0 / FPS)


if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())