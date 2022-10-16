import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    move = [False, False, False, False]

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.frame = 0  # frame counter
        self.state = 0
        self.change = 0
        self.images = []
        for i in range(0, 4):
            collect = []
            for j in range(0, 4):
                if i == 0:
                    path = "../images/player/up/" + str(j) + ".png"
                if i == 1:
                    path = "../images/player/down/" + str(j) + ".png"
                if i == 2:
                    path = "../images/player/left/" + str(j) + ".png"
                if i == 3:
                    path = "../images/player/right/" + str(j) + ".png"
                img = pygame.image.load(path).convert()
                img.convert_alpha()
                img.set_colorkey((255, 255, 255))
                collect.append(img)
            self.images.append(collect)
            self.image = self.images[0][0]
            self.rect = self.image.get_rect()

    def update(self, up, down, left, right):
        '''
        update the player's pos
        '''

        if up:  # up
            if self.rect.centery >= self.rect.height / 2:
                self.y -= PLAYER_SPEED
            self.state = 0
            self.change += 1
            if self.change == Frame_update:
                self.frame = (self.frame + 1) % 4
                self.change = 0
            self.image = self.images[self.state][self.frame]

        if down:  # down
            if self.rect.centery <= WIN_SIZE_Y - self.rect.height / 2:
                self.y += PLAYER_SPEED
            self.state = 1
            self.change += 1
            if self.change == Frame_update:
                self.frame = (self.frame + 1) % 4
                self.change = 0
            self.image = self.images[self.state][self.frame]

        if left:  # left
            if self.rect.centerx >= self.rect.width / 2:
                self.x -= PLAYER_SPEED
            self.state = 2
            self.change += 1
            if self.change == Frame_update:
                self.frame = (self.frame + 1) % 4
                self.change = 0
            self.image = self.images[self.state][self.frame]

        if right:  # right
            if self.rect.centerx <= WIN_SIZE_X - self.rect.width / 2:
                self.x += PLAYER_SPEED
            self.state = 3
            self.change += 1
            if self.change == Frame_update:
                self.frame = (self.frame + 1) % 4
                self.change = 0
            self.image = self.images[self.state][self.frame]

        self.rect.bottomleft = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

