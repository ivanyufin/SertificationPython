import pygame
import Common


class PlayerObject(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Common.spaceship_img
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.centery = Common.center_height

    def goUp(self):
        if self.rect.top >= 0:
            self.rect.y -= 5

    def goDown(self):
        if self.rect.bottom <= Common.screen_height:
            self.rect.y += 5

    def goLeft(self):
        if self.rect.left >= 0:
            self.rect.x -= 5

    def goRight(self):
        if self.rect.right <= Common.screen_width:
            self.rect.x += 5