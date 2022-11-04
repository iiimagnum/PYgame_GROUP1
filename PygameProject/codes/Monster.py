import pygame
import math
from settings import *


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 3
        self.x = x
        self.y = y
        self.image = pygame.image.load('../images/monster/0.png').convert()
        self.image.convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self, player):
        des_x = player.rect.centerx
        des_y = player.rect.centery
        # print(str(des_x) + " " + str(des_y))
        delta_x = des_x - self.rect.centerx
        delta_y = des_y - self.rect.centery
        distance = math.sqrt(delta_y**2 + delta_x**2)
        if distance != 0 and distance <= MONSTER_VIEW_DISTANCE:
            self.x = self.x + (delta_x / distance) * self.speed
            self.y = self.y + (delta_y / distance) * self.speed
        self.rect.center = (self.x, self.y)
        self.speed = 3

    def draw(self, surface):
        surface.blit(self.image, self.rect)