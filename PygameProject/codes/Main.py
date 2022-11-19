import pygame
from settings import *
from Player import *
from Monster import *
from Props import *
from Maze import *
from Wall import *
from SoundPlayer import Sound
from WarFog import *


def switch_map_before(surface, maze, player, monster_list):
    for y in range(0, 300):
        maze.draw(surface)
        player.draw(surface)
        [m.draw(surface) for m in monster_list]
        pygame.draw.rect(surface, [0, 0, 0], [0, 0, 840, y], 0)
        pygame.draw.rect(surface, [0, 0, 0], [0, 600 - y, 840, y], 0)
        pygame.display.flip()



def switch_map_after(surface, maze, player, monster_list,fog):
    for y in range(0, 300):
        maze.draw(surface)
        player.draw(surface)
        [m.draw(surface) for m in monster_list]
        fog.draw(surface,player.rect.center)
        pygame.draw.rect(surface, [0, 0, 0], [0, 0, 840, 300 - y], 0)
        pygame.draw.rect(surface, [0, 0, 0], [0, 300 + y, 840, 300 - y], 0)
        pygame.display.flip()

def bgm_start():
    """ Play some music!
    """
    # pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()
    pygame.mixer.music.load('..\sound\BGM.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)


def main():
    bgm_start()
    health = 100
    pygame.init()
    next_level = 0
    level_passed = 0
    score = 0
    soil_count = 0
    fruit_count = 0
    fonts = pygame.font.get_fonts()
    font = pygame.font.SysFont(fonts[0], 40)
    font.bold = True
    clock = pygame.time.Clock()
    running = True
    MainSurface = pygame.display.set_mode(((MAZE_X * 2 + 1) * CellSize, (MAZE_Y * 2 + 1) * CellSize))  # main surface
    wallsSurface = pygame.Surface(((MAZE_X*2+1)* CellSize, (MAZE_X*2+1) * CellSize))
    while running:
        '''Maze'''
        next_level = 0
        maze = Maze()
        maze.SummonMaze()
        monster_list = maze.SummonMonster(int(level_passed / 5) + 1)
        maze_info = maze.CurrentMazeInfo
        wall_group = pygame.sprite.Group()
        Soils = pygame.sprite.Group()

        for i in range(MAZE_Y * 2 + 1):
            for j in range(MAZE_X * 2 + 1):
                if maze.CurrentMazeInfo[i, j].cellType == 0:
                    # print(str(i) + " " + str(j))
                    x = j * 40 + 20
                    y = i * 40 + 20
                    wall_group.add(Wall((x, y)))

        wallsSurface.set_colorkey((1, 2, 3))  # set transparent color
        wallsSurface.fill((1, 2, 3))
        wall_group.draw(wallsSurface)
        wallMask=pygame.mask.from_surface(wallsSurface)

        '''Sound'''
        sound_dash = Sound('..\sound\Dash.wav')
        sound_treasure = Sound('..\sound\Treasure.wav')
        sound_pass = Sound('..\sound\Pass.wav')

        '''Player'''
        player = Player(60, 60, health)

        '''WarFog'''
        warFog = WarFogMaze(maze)
        warFog.update(player.rect.center)

        switch_map_after(MainSurface, maze, player, monster_list,warFog)

        while running:
            accumulated_threat = 0
            clock.tick(60)
            InputManager.update()
            if InputManager.keyDownList.__contains__(pygame.K_ESCAPE) or InputManager.keyDownList.__contains__(pygame.K_q):
                running = False
            if InputManager.quit:
                pygame.quit()
            if pygame.K_UP in InputManager.keyPressList:
                up = True
                accumulated_threat += 2
            else:
                up = False

            if pygame.K_DOWN in InputManager.keyPressList:
                down = True
                accumulated_threat += 2
            else:
                down = False

            if pygame.K_LEFT in InputManager.keyPressList:
                left = True
                accumulated_threat += 2
            else:
                left = False

            if pygame.K_RIGHT in InputManager.keyPressList:
                right = True
                accumulated_threat += 2
            else:
                right = False

            if pygame.K_SPACE in InputManager.keyPressList:
                space = True
                sound_dash.play()
                sound_dash.playing = True
                accumulated_threat += 5
                # print("space")
            else:
                space = False
                sound_dash.playing = False

            if pygame.K_b in InputManager.keyDownList:
                if soil_count > 0:
                    accumulated_threat += 1000
                    Soils.add(Soil(player.rect.centerx, player.rect.centery))
                    soil_count -= 1
            if pygame.K_n in InputManager.keyDownList:
                if fruit_count > 0:
                    accumulated_threat += 1000
                    fruit_count -= 1
                    if player.health <= 80:
                        player.health += 20
                    else:
                        player.health = 100

            '''Maze'''
            maze.draw(MainSurface)
            '''soil'''
            for m in monster_list:
                Soils.update(m, player)
            '''Player'''
            player.update(space, up, down, left, right, wallMask)

            '''Monsters'''
            [m.add_threat(player, accumulated_threat) for m in monster_list]
            [m.update(player, wall_group, maze_info) for m in monster_list]

            if player.health <= 0:
                pygame.quit()

            for ip in maze.InteractPointList:
                if player.rect.colliderect(ip):
                    # print("get")
                    if ip.type == InteractType.Treasure:
                        sound_treasure.play()
                        maze.InteractPointList.remove(ip)
                        score += 1
                    elif ip.type == InteractType.Exit:
                        # print("exit")
                        next_level = 1
                        health = player.health
                        break
                    elif ip.type == InteractType.Soil:
                        maze.InteractPointList.remove(ip)
                        if soil_count < 3:
                            soil_count += 1
                    elif ip.type == InteractType.Fruit:
                        maze.InteractPointList.remove(ip)
                        if fruit_count < 3:
                            fruit_count += 1

            if next_level:
                sound_pass.play()
                level_passed += 1
                switch_map_before(MainSurface, maze, player, monster_list)
                break

            Soils.draw(MainSurface)
            player.draw(MainSurface)
            textSurface = font.render("Score: " + str(score), True, (255, 255, 255))
            width, height = font.size("Score: " + str(score))
            soil_count_surface = font.render(": " + str(soil_count), True, (255, 255, 255))
            fruit_count_surface = font.render(": " + str(fruit_count), True, (255, 255, 255))
            [m.draw(MainSurface) for m in monster_list]


            """WarFog"""
            warFog.update(player.rect.center)

            warFog.draw(MainSurface,player.rect.center)
            """Test Draw
            player.getMask()
            MainSurface.blit(wallsSurface,wallsSurface.get_rect())
            """
            MainSurface.blit(textSurface, (840 - width - 5, 5))
            img = pygame.image.load("../images/props/soil_water.png").convert_alpha()
            img.set_colorkey((255, 255, 255))
            MainSurface.blit(img, (5, 5))
            MainSurface.blit(soil_count_surface, (50, 3))
            img = pygame.image.load("../images/interactPoint/fruit_item.png").convert_alpha()
            img.set_colorkey((255, 255, 255))
            MainSurface.blit(img, (130, 7))
            MainSurface.blit(fruit_count_surface, (165, 3))
            pygame.display.flip()


if __name__ == "__main__":
    main()
