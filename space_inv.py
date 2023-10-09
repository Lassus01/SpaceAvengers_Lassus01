import pygame as pg
import random

# Инициализация Pygame
pg.init()

# Размеры экрана
screen_width, screen_height = 900, 600

# Настройки игры
FPS = 24  # Количество кадров в секунду
clock = pg.time.Clock()

# Загрузка изображений
bg_img = pg.image.load('src/background.png')
icon_img = pg.image.load('src/ufo.png')
player_img = pg.image.load('src/player.png')
bullet_img = pg.image.load('src/bullet.png')
enemy_img = pg.image.load('src/enemy.png')
strong_enemy_img = pg.image.load('src/enemy2.png')

# Создание окна
display = pg.display.set_mode((screen_width, screen_height))
pg.display.set_icon(icon_img)
pg.display.set_caption('Космическое вторжение')

# Шрифты
sys_font = pg.font.SysFont('arial', 34)
font = pg.font.Font('src/04B_19.TTF', 48)

# Игровые параметры
player_width, player_height = player_img.get_size()
player_gap = 10
player_velocity = 10
player_dx = 0
player_x = screen_width/2 - player_width/2
player_y = screen_height - player_height - player_gap

bullet_width, bullet_height = bullet_img.get_size()
bullet_dy = -5
bullet_x = 0
bullet_y = 0
bullet_alive = False

enemy_width, enemy_height = enemy_img.get_size()
strong_enemy_width, strong_enemy_height = strong_enemy_img.get_size()
enemy_dx = 0
enemy_dy = 1
enemy_x = 0
enemy_y = 0
enemy_health = 1  # Здоровье врага (2 попадания для усиленного врага)
strong_enemy_health = 2  # Здоровье усиленного врага

score = 0  # Счетчик очков

# Флаги игры
game_over = False
game_paused = False

# Функции

def check_collision():
    "Проверка столкновения игрока и врага."
    global game_over
    player_rect = pg.Rect(player_x, player_y, player_width, player_height)
    enemy_rect = pg.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    if player_rect.colliderect(enemy_rect):
        game_over = True

def create_enemy():
    """Создает врага или усиленного врага в случайном месте вверху окна."""
    global enemy_x, enemy_y, enemy_health
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = 0
    enemy_health = random.choice([1, 2])  # Случайное здоровье врага (1 или 2)

def player_model():
    """Обновляет положение игрока."""
    global player_x
    player_x += player_dx
    if player_x < 0:
        player_x = 0
    elif player_x > screen_width - player_width:
        player_x = screen_width - player_width

def bullet_model():
    """Обновляет положение пули."""
    global bullet_y, bullet_alive
    bullet_y += bullet_dy
    if bullet_y < 0:
        bullet_alive = False

def create_bullet():
    """Создает пулю."""
    global bullet_y, bullet_x, bullet_alive
    bullet_alive = True
    bullet_x = player_x + player_width/2 - bullet_width/2
    bullet_y = player_y - bullet_height

def enemy_model():
    """Обновляет положение врага и проверяет столкновение с пулей."""
    global enemy_y, enemy_health, bullet_alive, score
    enemy_y += enemy_dy
    if enemy_y > screen_height:
        create_enemy()

    if bullet_alive:
        re = pg.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        rb = pg.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
        is_crossed = re.colliderect(rb)

        if is_crossed:
            if enemy_health == 2:
                enemy_health = 1  # Усиленный враг получает урон
            else:
                create_enemy()  # Обычный враг уничтожается
                score += 1  # Увеличение счетчика очков
            bullet_alive = False

def display_redraw():
    """Перерисовывает экран игры."""
    display.blit(bg_img, (0, 0))
    display.blit(player_img, (player_x, player_y))
    if bullet_alive:
        display.blit(bullet_img, (bullet_x, bullet_y))
    if enemy_health == 2:
        display.blit(strong_enemy_img, (enemy_x, enemy_y))
    else:
        display.blit(enemy_img, (enemy_x, enemy_y))

    score_text = sys_font.render('Score: ' + str(score), True, (255, 255, 255))
    display.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render('Game Over', True, (255, 0, 0))
        restart_text = sys_font.render('Press "R" to restart', True, (255, 255, 255))
        display.blit(game_over_text, (screen_width/2 - game_over_text.get_width()/2, screen_height/2 - game_over_text.get_height()/2))
        display.blit(restart_text, (screen_width/2 - restart_text.get_width()/2, screen_height/2 + game_over_text.get_height()))

    if game_paused:
        pause_text = font.render('Paused', True, (255, 255, 0))
        display.blit(pause_text, (screen_width/2 - pause_text.get_width()/2, screen_height/2 - pause_text.get_height()/2))

    pg.display.update()

# Создание врага при запуске игры
create_enemy()

# Игровой цикл
running = True
while running:
    # Обработка событий
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                player_dx = -player_velocity
            elif event.key == pg.K_RIGHT:
                player_dx = player_velocity
            elif event.key == pg.K_SPACE and not bullet_alive:
                create_bullet()
            elif event.key == pg.K_r and game_over:
                # Перезапуск игры
                game_over = False
                score = 0
                player_x = screen_width / 2 - player_width / 2
                create_enemy()
            elif event.key == pg.K_p:
                game_paused = not game_paused  # Переключение флага паузы

        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                player_dx = 0

    if not game_over and not game_paused:
        # Моделирование игровых объектов
        player_model()
        bullet_model()
        enemy_model()
        check_collision()

    # Перерисовка экрана
    display_redraw()

    # Ограничение FPS
    clock.tick(FPS)

# Завершение Pygame
pg.quit()
