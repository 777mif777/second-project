import pygame
import time

pygame.init()

# Глобальные переменные (настройки)
window_width = 800
window_height = 600
fon = "fon.png"  # изображение должно быть в том же каталоге, что и код на питоне

# Создаем окно
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Игра v1.0")

# Загружаем и масштабируем фоновое изображение
imgl = pygame.image.load(fon)
back_fon = pygame.transform.scale(imgl, (window_width, window_height))

# Класс игрока (спрайт)
class Player(pygame.sprite.Sprite):
    def __init__(self, filename, hero_x=100, hero_y=250, x_speed=0, y_speed=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)  # загрузка героя из файла
        self.rect = self.image.get_rect()
        self.hero_x = hero_x
        self.hero_y = hero_y
        self.rect.x = self.hero_x  # установка персонажа в начальную точку (x, y)
        self.rect.y = self.hero_y
        self.x_speed = x_speed  # скорость движения спрайта по горизонтали
        self.y_speed = y_speed  # скорость движения спрайта по вертикали

    def update(self):
        # Перемещаем персонажа, учитывая текущую горизонтальную и вертикальную скорость
        self.hero_x += self.x_speed
        self.hero_y += self.y_speed
        self.rect.x = self.hero_x
        self.rect.y = self.hero_y

        # Ограничение движения персонажа в пределах окна
        if self.rect.left < 0:
            self.rect.left = 0
            self.hero_x = self.rect.x
        if self.rect.right > window_width:
            self.rect.right = window_width
            self.hero_x = self.rect.x
        if self.rect.top < 0:
            self.rect.top = 0
            self.hero_y = self.rect.y
        if self.rect.bottom > window_height:
            self.rect.bottom = window_height
            self.hero_y = self.rect.y

# Создаем игрока
filename = "valorant.png"
hero = Player(filename)
all_sprites = pygame.sprite.Group()
all_sprites.add(hero)

# Инициализация переменных
sdvig_fona = 0  # сдвиг фона
speed = 0  # скорость фона
player_speed = 5  # скорость движения игрока

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                hero.x_speed = -player_speed
            if event.key == pygame.K_RIGHT:
                hero.x_speed = player_speed
            if event.key == pygame.K_UP:
                hero.y_speed = -player_speed
            if event.key == pygame.K_DOWN:
                hero.y_speed = player_speed
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                hero.x_speed = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                hero.y_speed = 0

    # Проверяем, достиг ли спрайт границ слева или справа, чтобы двигать фон
    if hero.rect.left <= 0 and hero.x_speed < 0:
        speed = player_speed  # фон движется вправо
    elif hero.rect.right >= window_width and hero.x_speed > 0:
        speed = -player_speed  # фон движется влево
    else:
        speed = 0  # фон не движется, если персонаж не у границ

    # Обновляем сдвиг фона
    sdvig_fona = (sdvig_fona + speed) % window_width
    window.blit(back_fon, (sdvig_fona, 0))
    if sdvig_fona != 0:
        window.blit(back_fon, (sdvig_fona - window_width, 0))

    # Обновляем положение игрока
    all_sprites.update()
    all_sprites.draw(window)

    pygame.display.update()
    clock.tick(60)  # 60 FPS

pygame.quit()