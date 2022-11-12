import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    move = [False, False, False, False]

    def __init__(self, x, y, health=100):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.frame = 0  # frame counter
        self.state = 0
        self.change = 0
        self.power = 100
        self.health = health
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
                img = pygame.image.load(path).convert_alpha()
                #img.set_colorkey((255, 255, 255))
                collect.append(img)
            self.images.append(collect)
            self.image = self.images[0][0]
            self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self, space, up, down, left, right, wallMask):
        '''
        update the player's pos
        '''
        if space and self.power >= 1:
            # print("run")
            PLAYER_SPEED = 4
            self.power -= 1
            # print(self.power)
        elif space and self.power == 0:
            PLAYER_SPEED = 2
        else:
            PLAYER_SPEED = 2
            if self.power < 100:
                self.power += 0.1
            # print(self.power)

        '''
        if self.state == 0:
                if self.rect.centery >= self.rect.height / 2 + PLAYER_DASH_SPEED:
                    self.y -= PLAYER_DASH_SPEED
                    self.rect.center = (self.x, self.y)
                else:
                    self.y = self.rect.height / 2
                    self.rect.center = (self.x, self.y)
            if self.state == 1:
                if self.rect.centery + PLAYER_DASH_SPEED <= WIN_SIZE_Y - self.rect.height / 2:
                    self.y += PLAYER_DASH_SPEED
                    self.rect.center = (self.x, self.y)
                else:
                    self.y = WIN_SIZE_Y - self.rect.height / 2
                    self.rect.center = (self.x, self.y)
            if self.state == 2:
                if self.rect.centerx >= self.rect.width / 2 + PLAYER_DASH_SPEED:
                    self.x -= PLAYER_DASH_SPEED
                    self.rect.center = (self.x, self.y)
                else:
                    self.x = self.rect.width / 2
                    self.rect.center = (self.x, self.y)
            if self.state == 3:
                if self.rect.centerx + PLAYER_DASH_SPEED <= WIN_SIZE_X - self.rect.width / 2:
                    self.x += PLAYER_DASH_SPEED
                    self.rect.center = (self.x, self.y)
                else:
                    self.x = WIN_SIZE_X - self.rect.width / 2
                    self.rect.center = (self.x, self.y) 
        '''



        if up:  # up
            if self.rect.centery >= self.rect.height / 2:
                self.y -= PLAYER_SPEED
                self.rect.center = (self.x, self.y)
                offset = wallMask.get_rect().x - self.rect.topleft[0], wallMask.get_rect().y - self.rect.topleft[1]
                pos = self.getMask().overlap(wallMask, offset)
                if pos is not None:
                    #print(f"collide pos is {pos[0], pos[1]}")                #if len(pygame.sprite.spritecollide(self, walls, False)):
                    self.y += PLAYER_SPEED
            self.state = 0
            self.change += 1
            if self.change == Frame_update:
                self.frame = (self.frame + 1) % 4
                self.change = 0
            self.image = self.images[self.state][self.frame]

        if down:  # down
            if self.rect.centery <= WIN_SIZE_Y - self.rect.height / 2:
                self.y += PLAYER_SPEED
                self.rect.center = (self.x, self.y)
                offset = wallMask.get_rect().x - self.rect.topleft[0], wallMask.get_rect().y - self.rect.topleft[1]
                pos = self.getMask().overlap(wallMask, offset)
                if pos is not None:
                    #print(f"collide pos is {pos[0], pos[1]}")                #if len(pygame.sprite.spritecollide(self, walls, Fase)):
                    self.y -= PLAYER_SPEED
            self.state = 1
            self.change += 1
            if self.change == Frame_update:
                self.frame = (self.frame + 1) % 4
                self.change = 0
            self.image = self.images[self.state][self.frame]

        if left:  # left
            if self.rect.centerx >= self.rect.width / 2:
                self.x -= PLAYER_SPEED
                self.rect.center = (self.x, self.y)
                offset = wallMask.get_rect().x - self.rect.topleft[0], wallMask.get_rect().y - self.rect.topleft[1]
                pos=self.getMask().overlap(wallMask,offset)
                if pos is not None:
                    #print(f"collide pos is {pos[0], pos[1]}")                #collided_walls = pygame.sprite.spritecollide(self, walls, False)
                #if len(collided_walls):
                    self.x += PLAYER_SPEED
            self.state = 2
            self.change += 1
            if self.change == Frame_update:
                self.frame = (self.frame + 1) % 4
                self.change = 0
            self.image = self.images[self.state][self.frame]

        if right:  # right
            if self.rect.centerx <= WIN_SIZE_X - self.rect.width / 2:
                self.x += PLAYER_SPEED
                self.rect.center = (self.x, self.y)
                offset = wallMask.get_rect().x - self.rect.topleft[0], wallMask.get_rect().y - self.rect.topleft[1]
                pos = self.getMask().overlap(wallMask, offset)
                if pos is not None:
                    #print(f"collide pos is {pos[0], pos[1]}")                #if len(pygame.sprite.spritecollide(self, walls, False)):
                    self.x -= PLAYER_SPEED
            self.state = 3
            self.change += 1
            if self.change == Frame_update:
                self.frame = (self.frame + 1) % 4
                self.change = 0
            self.image = self.images[self.state][self.frame]
        self.rect.center = (self.x, self.y)


    def draw(self, surface):
        surface.blit(self.image, self.rect)
        health_percent = self.health / 100 if self.health >= 0 else 0
        power_percent = self.power / 100 if self.power >= 0 else 0
        pygame.draw.rect(surface, [0, 255, 0], [20, 575, 300 * health_percent, 10], 0)
        pygame.draw.rect(surface, [255, 0, 0], [350, 575, 300 * power_percent, 10], 0)

        # for debugging: display the boundary of the player
        '''
        img = pygame.Surface(self.rect.size)
        img.fill((128,128,128))
        surface.blit(img, self.rect)
        '''

    def getMask(self):
        return  pygame.mask.from_surface(self.image)