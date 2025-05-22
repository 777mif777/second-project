import pygame
import time

pygame.init()

#Глобальные переменные (настройки)
window_width = 800
window_height = 600
fon="fon.png" #изображение должно быть в том же каталоге, что и код на питоне

#Звук
window = pygame.display.set_mode((window_width, window_height)) #создаем окно указанных размеров
pygame.display.set_caption("Игра v1.0") #устанавливаем название окна программы

speed = 0 #текущая скорость перемещения
sdvig_fona = 0 #сдвиг фона

imgl = pygame.image.load(fon) #загружаем фоновый рисунок
back_fon = pygame.transform.scale(imgl, (window_width, window_height)) #размер картинки back - те же, что и у окна

running=True
while running:
    for event in pygame.event.get(): #примем ли событие нажатие на крестик
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN: #примем ли событие нажатие на крестик
            if event.key==pygame.K_LEFT:
                speed=5
            if event.key==pygame.K_RIGHT: #добавляем движение фона влево при нажатии стрелки вправо
                speed=-5
        if event.type==pygame.KEYUP: #если клавиша отпущена
            if event.key==pygame.K_LEFT:
                speed=0
            if event.key==pygame.K_RIGHT:
                speed=0

    sdvig_fona = (sdvig_fona+speed) % window_width
    window.blit(back_fon, (sdvig_fona, 0))
    if sdvig_fona != 0:
        window.blit(back_fon, (sdvig_fona - window_width, 0)) #рисуем такой же фон слева от сдвига

    pygame.display.update() #обновляем следующее окно, теперь видно последнее состояние экранной поверхности
    time.sleep(0.02)

pygame.quit() # закрыть окно крестиком
