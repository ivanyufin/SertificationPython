import pygame
import os
import Asteroid


# Необходимые параметры
screen_width = 800
screen_height = 650
center_width = screen_width / 2
center_height = screen_height / 2
FPS = 60
score = 0
lives = 5
background1X = 0
background2X = 0
backgroundSpeed = 2
font_size = 30
half_font_size = font_size / 2
indent_user_score = center_height - font_size * 3


# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


screen = pygame.display.set_mode((screen_width, screen_height))
# Настройка папки ассетов
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
# 2 заднего фона для того, чтобы сделать "бесконечный" фон
background_img = pygame.image.load(os.path.join(img_folder, 'background.jpg'))
background_img2 = pygame.image.load(os.path.join(img_folder, 'background.jpg'))
asteroid_img = pygame.image.load(os.path.join(img_folder, 'asteroid50.png')).convert_alpha()
health_img = pygame.image.load(os.path.join(img_folder, 'health.png')).convert_alpha()
spaceship_img = pygame.image.load(os.path.join(img_folder, 'rocket.png')).convert_alpha()

background2X = background_img.get_rect().width

asteroids = list()
bullets = list()
all_sprites = pygame.sprite.Group()


def add_asteroid():
    asteroid = Asteroid.AsteroidObject()
    all_sprites.add(asteroid)
    asteroids.append(asteroid)


def remove_asteroid(asteroid):
    all_sprites.remove(asteroid)
    asteroids.remove(asteroid)