import pygame
from Player import *
from Monster import *
from Props import *
from settings import *
from InputManager import *
from Wall import Wall


def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True
    IM = InputManager()
    surface = pygame.display.set_mode((WIN_SIZE_X, WIN_SIZE_Y))
    player = Player(25, 30)
    monster = Monster(500, 500)
    Soils = pygame.sprite.Group()
    Soils.add(Soil(700, 700))
    wall1 = Wall((200, 200))
    wall2 = Wall((300, 300))
    wall_group = pygame.sprite.Group()
    wall_group.add(wall1)
    wall_group.add(wall2)
    while running:
        clock.tick(60)
        IM.update()
        '''
        for key in IM.keyDownList:
            print(str(key) + "is Down")

        for key in IM.keyPressList:
            print(str(key) + "is Pressing")

        for key in IM.keyUpList:
            print(str(key) + "is Up")
        '''
        if IM.keyDownList.__contains__(pygame.K_ESCAPE):
            running = False
        if IM.quit:
            pygame.quit()

        if pygame.K_UP in IM.keyPressList:
            up = True
        else:
            up = False

        if pygame.K_DOWN in IM.keyPressList:
            down = True
        else:
            down = False

        if pygame.K_LEFT in IM.keyPressList:
            left = True
        else:
            left = False

        if pygame.K_RIGHT in IM.keyPressList:
            right = True
        else:
            right = False

        if pygame.K_SPACE in IM.keyPressList:
            space = True
            # print("space")
        else:
            space = False

        if pygame.K_b in IM.keyDownList:
            Soils.add(Soil(player.rect.centerx, player.rect.centery))

        surface.fill((0, 0, 0))
        Soils.update(monster, player)
        player.update(space, up, down, left, right, wall_group)
        monster.update(player)
        Soils.draw(surface)
        player.draw(surface)
        monster.draw(surface)
        wall_group.draw(surface)
        pygame.display.flip()


if __name__ == "__main__":
    main()
