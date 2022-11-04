import pygame
from settings import *


class Prop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = None
        self.rect = None

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Soil(Prop):
    def __init__(self, x, y):
        Prop.__init__(self, x, y)
        self.image = pygame.image.load('../images/props/soil_water.png').convert()
        self.image.convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self, monster, player):
        if self.rect.colliderect(monster.rect):
            monster.speed = 0.5
