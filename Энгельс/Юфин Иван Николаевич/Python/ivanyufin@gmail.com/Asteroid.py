import pygame
import Common
import random

class AsteroidObject(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Common.asteroid_img
        self.rect = self.image.get_rect()
        self.rect.width = 20
        self.rect.center = (Common.screen_width - random.randint(0, 100), random.randint(0, Common.screen_height - 25))
        self.speed = random.randint(1, 4)

    def update(self):
        global lives
        if self.rect.x >= 0:
            self.rect.x -= self.speed
        else:
            Common.all_sprites.remove(self)
            Common.remove_asteroid(self)
            Common.add_asteroid()
            Common.lives -= 1