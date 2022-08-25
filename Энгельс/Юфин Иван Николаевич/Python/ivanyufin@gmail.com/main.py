import pygame
import random
import database
import Player
import Common

database.create_table()


# Создаем игру и окно
pygame.init()
screen = pygame.display.set_mode((Common.screen_width, Common.screen_height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Функция вывода текста на экран
def print_text(message, x, y, font_type=pygame.font.SysFont('Times new roman', 30), font_size=30, font_color=Common.WHITE):
    font_type = pygame.font.SysFont('Times new roman', font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))

start_game = False
running = False
end_game = False

hello_text = 'Введите Ваше имя:'
user_name = ''
prompt_text = ''
end_game_text = 'Конец игры'
top5_text = 'Топ-5 игроков:'
prompt = False

# Показывается меню ввода имени
while not start_game:
    clock.tick(Common.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_game = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Если сейчас показывается подсказка и нажали Enter, то запустить игру
                if prompt:
                    if len(user_name) > 0:
                        start_game = True
                        running = True
                else:
                    # Иначе показать подсказку
                    prompt = True
            elif event.key == pygame.K_BACKSPACE:
                user_name = user_name[:-1]
                if len(user_name) == 0:
                    prompt_text = ''
            else:
                if len(user_name) > -1:
                    prompt_text = 'Для продолжения нажмите кнопку Enter...'
                user_name += event.unicode

    screen.fill(Common.WHITE)
    screen.blit(Common.background_img, (0, 0))
    # Если показывается меню ввода имени
    if not prompt:
        print_text(hello_text, Common.center_width - Common.half_font_size * (len(hello_text) / 2), Common.center_height - 100)
        print_text(user_name, Common.center_width - Common.half_font_size * (len(user_name) / 2), Common.center_height - 60)
        print_text(prompt_text, Common.center_width - Common.half_font_size * (len(prompt_text) / 2), Common.center_height - 15)
    else:
        # Если показывается подсказка
        prompt_text = 'Правила игры:'
        print_text(prompt_text, Common.center_width - Common.half_font_size * (len(prompt_text) / 2), Common.center_height - Common.font_size * 3)
        prompt_text = 'Управление - стрелками. Для выстрела нажмите пробел'
        print_text(prompt_text, Common.center_width - Common.half_font_size * (len(prompt_text) / 2), Common.center_height - Common.font_size * 2)
        prompt_text =  'Чтобы выиграть - нужно набрать 1000 очков'
        print_text(prompt_text, Common.center_width - Common.half_font_size * (len(prompt_text) / 2),
                   Common.center_height - Common.font_size)
        prompt_text = 'Астероид залетел за корабль - минус жизнь'
        print_text(prompt_text, Common.center_width - Common.half_font_size * (len(prompt_text) / 2),
                   Common.center_height)
        prompt_text = 'Для начала игры нажмите кнопку Enter...'
        print_text(prompt_text, Common.center_width - Common.half_font_size * (len(prompt_text) / 2),
                   Common.center_height + Common.font_size)

    pygame.display.flip()


# Создаем игрока и астероиды
player = Player.PlayerObject()
count_asteroid = random.randint(3, 6)
for i in range(count_asteroid):
    Common.add_asteroid()
Common.all_sprites.add(player)


# Цикл игры
while running:
    # Держим цикл на правильной скорости
    clock.tick(Common.FPS)

    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Common.bullets.append([player.rect.right - 10, player.rect.centery])

    # Выбирается в какую сторогу двигаться
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.goUp()
    elif keys[pygame.K_DOWN]:
        player.goDown()
    elif keys[pygame.K_LEFT]:
        player.goLeft()
    elif keys[pygame.K_RIGHT]:
        player.goRight()

    # Движение снарядов вправо
    for bul in Common.bullets:
        if bul[0] >= Common.screen_width:
            Common.bullets.remove(bul)
        else:
            bul[0] += 5

    # Уничтожение астероида
    for asteroid in Common.asteroids:
        for bul in Common.bullets:
            if bul[0] >= asteroid.rect.left and bul[1] >= asteroid.rect.top - 10 and bul[
                1] <= asteroid.rect.bottom + 10:
                Common.remove_asteroid(asteroid)
                Common.add_asteroid()
                Common.bullets.remove(bul)
                Common.score += 5

    # Рендеринг
    screen.fill(Common.WHITE)
    screen.blit(Common.background_img, (Common.background1X, 0))
    screen.blit(Common.background_img2, (Common.background2X, 0))
    Common.all_sprites.draw(screen)
    for bul in Common.bullets:
        pygame.draw.rect(screen, Common.GREEN, (bul[0], bul[1], 15, 5))
    for health in range(Common.lives):
        screen.blit(Common.health_img, (Common.center_width - Common.health_img.get_rect().width * health + Common.health_img.get_rect().width, 0))

    print_text(str(Common.score), Common.screen_width - Common.half_font_size * (len(str(Common.score))), 0)
    print_text(user_name, 0, 0)

    # Обновление
    Common.all_sprites.update()
    pygame.display.update()

    # Зацикливаем движение заднего фона
    Common.background1X -= Common.backgroundSpeed
    Common.background2X -= Common.backgroundSpeed
    if Common.background2X == 0:
        Common.background1X = Common.background_img2.get_rect().right
    if Common.background1X == 0:
        Common.background2X = Common.background_img.get_rect().right

    # Если закончились жизни или достигли максимального количества очков
    if Common.lives == 0 or Common.score == 1000:
        running = False
        end_game = True
        database.insert_user_score(user_name, Common.score)
        while end_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_game = False

            if Common.score == 1000:
                end_game_text = 'Вы выиграли!'
            # Отображается надпись конца игры
            print_text(end_game_text, Common.center_width - Common.half_font_size * (len(end_game_text) / 2), Common.indent_user_score)
            print_text(top5_text, Common.center_width - Common.half_font_size * (len(top5_text) / 2), Common.indent_user_score + Common.font_size)
            # Выводится топ-5 игроков
            user_scores = database.get_users_score()
            i = 1
            for user_score in user_scores:
                print_text(user_score[0], Common.center_width - Common.half_font_size * (len(user_score[0]) / 2) * 2,
                           (Common.indent_user_score + Common.font_size * 2) + i * Common.font_size)
                print_text(str(user_score[1]),
                           Common.center_width - Common.half_font_size * (len(str(user_score[1])) / 2) * 2 + Common.font_size * 2,
                           (Common.indent_user_score + Common.font_size * 2) + i * Common.font_size)
                i += 1

            pygame.display.update()

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
