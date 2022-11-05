import pygame
from settings import *
from Player import *
from Monster import *
from Props import *
from settings import *
from Maze import *


def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True
    MainSurface = pygame.display.set_mode(((MAZE_X * 2 + 1) * CellSize, (MAZE_Y * 2 + 1) * CellSize))  # main surface

    '''Maze'''
    maze = Maze()
    maze.SummonMaze()
    wall_group = pygame.sprite.Group()

    '''Player'''
    player = Player(60, 60)

    while running:
        clock.tick(60)
        InputManager.update()
        if InputManager.keyDownList.__contains__(pygame.K_ESCAPE) or InputManager.keyDownList.__contains__(pygame.K_q):
            running = False
        if InputManager.quit:
            pygame.quit()
        if pygame.K_UP in InputManager.keyPressList:
            up = True
        else:
            up = False

        if pygame.K_DOWN in InputManager.keyPressList:
            down = True
        else:
            down = False

        if pygame.K_LEFT in InputManager.keyPressList:
            left = True
        else:
            left = False

        if pygame.K_RIGHT in InputManager.keyPressList:
            right = True
        else:
            right = False

        if pygame.K_SPACE in InputManager.keyDownList:
            space = True
            # print("space")
        else:
            space = False

        '''Maze'''
        maze.draw(MainSurface)

        '''Player'''
        player.update(space, up, down, left, right, wall_group)
        player.draw(MainSurface)

        pygame.display.flip()


if __name__ == "__main__":
    main()
