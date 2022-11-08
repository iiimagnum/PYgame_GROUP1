import pygame
from settings import *
from Player import *
from Monster import *
from Props import *
from Maze import *
from Wall import *


def switch_map_before(surface, maze, player):
    for y in range(0, 300):
        maze.draw(surface)
        player.draw(surface)
        pygame.draw.rect(surface, [0, 0, 0], [0, 0, 840, y], 0)
        pygame.draw.rect(surface, [0, 0, 0], [0, 600 - y, 840, y], 0)
        pygame.display.flip()


def switch_map_after(surface, maze, player):
    for y in range(0, 300):
        maze.draw(surface)
        player.draw(surface)
        pygame.draw.rect(surface, [0, 0, 0], [0, 0, 840, 300 - y], 0)
        pygame.draw.rect(surface, [0, 0, 0], [0, 300 + y, 840, 300 - y], 0)
        pygame.display.flip()


def main():
    health = 100
    pygame.init()
    next_level = 0
    clock = pygame.time.Clock()
    running = True
    MainSurface = pygame.display.set_mode(((MAZE_X * 2 + 1) * CellSize, (MAZE_Y * 2 + 1) * CellSize))  # main surface

    while running:
        '''Maze'''
        next_level = 0
        maze = Maze()
        maze.SummonMaze()
        wall_group = pygame.sprite.Group()
        for i in range(MAZE_Y * 2 + 1):
            for j in range(MAZE_X * 2 + 1):
                if maze.CurrentMazeInfo[i, j].cellType == 0:
                    # print(str(i) + " " + str(j))
                    x = j * 40 + 20
                    y = i * 40 + 20
                    wall_group.add(Wall((x, y)))

        '''Player'''
        player = Player(60, 60, health)
        switch_map_after(MainSurface, maze, player)
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

            if pygame.K_SPACE in InputManager.keyPressList:
                space = True
                # print("space")
            else:
                space = False

            '''Maze'''
            maze.draw(MainSurface)

            '''Player'''
            player.update(space, up, down, left, right, wall_group)

            for ip in maze.InteractPointList:
                if player.rect.colliderect(ip):
                    # print("get")
                    if ip.type == InteractType.Treasure:
                        maze.InteractPointList.remove(ip)
                    elif ip.type == InteractType.Exit:
                        # print("exit")
                        next_level = 1
                        break

            if next_level:
                switch_map_before(MainSurface, maze, player)
                break
            player.draw(MainSurface)

            pygame.display.flip()


if __name__ == "__main__":
    main()
