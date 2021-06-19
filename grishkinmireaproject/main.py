
import random
from os import path
import pygame  # библиотека pygame предназначена для создания игр
import keyboard

WIDTH = 480
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLUEWIETE = (0, 255, 255)
YELLOW = (255, 255, 0)

img_dir = path.join(path.dirname(__file__), 'Sprite')  # папка с спрайтами
background = pygame.image.load(path.join(img_dir, 'Ekran.png'))  # задний фон
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "prototyp.png"))
meteorit_img = pygame.image.load(path.join(img_dir, "asteroid2.png"))  # нарисованные мною спрайты напоминают печенье
bullet_img = pygame.image.load(path.join(img_dir, "puli.png"))  # данный спрайт не используется так как я
# не подогнал его под нужный формат в соответствии с чем он выдаёт ошибку так как вылезает за пределы поля

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PythonGame")
clock = pygame.time.Clock()
bullets = pygame.sprite.Group()

font_name = pygame.font.match_font('arial ')

# это для цикла меню
# инициировать Pygame и дать разрешение
# использовать функциональность Pygame.
pygame.init()
# определить значение RGB для белого,
# зеленый, синий цвет. 
green = (0, 255, 0)
blue = (0, 0, 128)
# присваивание значений переменной X и Y
X = 480
Y = 600
# создать объект отображаемой поверхности
# определенного размера..e (X, Y).
display_surface = pygame.display.set_mode((X, Y))
# установить имя окна Pygame
pygame.display.set_caption('Menu')
# создать объект шрифта.
# 1-й параметр - это файл шрифта
# который присутствует в пигме.
# 2-й параметр - размер шрифта
font = pygame.font.Font('freesansbold.ttf', 20)
# создать текстовый объект suface,
# на котором нарисован текст.
text = font.render('Нажмите "a" чтобы начать игру', True, blue, BLACK)
# создать прямоугольный объект для
# текстовая поверхность объекта
textRect = text.get_rect()
# установить центр прямоугольного объекта.
textRect.center = (X // 2, Y // 2)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)  # Игнорирование чёрного цвета
        self.rect = self.image.get_rect()
        self.radius = 35
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8

        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.height > HEIGHT:
            self.rect.height = HEIGHT
        if self.rect.height < 0:
            self.rect.height = 0


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteorit_img
        self.image = pygame.transform.scale(meteorit_img, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .95 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)  # вращение
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            # self.image = pygame.transform.rotate(self.image, self.rot_speed)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
        # вращение спрайтов


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(BLUEWIETE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
asteroid = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


def newmob():
    m = Asteroid()
    all_sprites.add(m)
    asteroid.add(m)


for i in range(8):
    newmob()
score = 0


menu = True
running = True
while running:  # игровой цикл

    while menu:
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        # копирование объекта текстовой поверхности
        # к объекту отображения поверхност
        # в центральной координате.
        display_surface.blit(text, textRect)
        # перебирать список объектов Event
        # который был возвращен методом pygame.event.get ().
        for event in pygame.event.get():
            # если тип объекта события QUIT
            # затем выход из игры
            # и запрограммируйте оба.
            if event.type == pygame.QUIT:
                # деактивирует библиотеку pygame
                pygame.quit()
                # выйти из программы.
                quit()
            # Рисует поверхность объекта на экране.
            pygame.display.update()

            key = 'a'       # прожать для старта
            if keyboard.is_pressed(key):
                menu = False

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    all_sprites.update()  # обновление

    hits = pygame.sprite.spritecollide(player, asteroid, False,
                                       pygame.sprite.collide_circle)  # (обработка столкновения игра с астероидом)
    for hit in hits:
        player.shield -= 2
        newmob()
        if player.shield <= 0:
            running = False  # если здоровье <= 0 игра завершается

    hits = pygame.sprite.groupcollide(asteroid, bullets, True, True)  # проверка столкновения пули и астероид  а
    for hit in hits:
        score += 1
        newmob()

    screen.fill(BLACK)
    screen.blit(background, background_rect)  # фон был взят с картинок в инете
    all_sprites.draw(screen)
    draw_text(screen, str(score), 20, WIDTH / 2, 14)
    draw_shield_bar(screen, 5, 5, player.shield)
    pygame.display.flip()


pygame.quit()
