from numpy import block
import pygame
import math
from settings import *
import heapq
from SoundPlayer import Sound

def heuristic(ax, ay, bx, by):
# Manhattan (or taxicab) distance on a square grid
    return abs(ax - bx) + abs(ay - by)

def neighbors(block_index, max_col, max_row):
    col, row = block_index
    neighbors_list = []
    if col > 0:
        neighbors_list.append((col - 1, row))
    if row > 0:
        neighbors_list.append((col, row - 1))
    if col < max_col - 1:
        neighbors_list.append((col + 1, row))
    if row < max_row - 1:
        neighbors_list.append((col, row + 1))
    return neighbors_list

class Monster(pygame.sprite.Sprite):
    def __init__(self, block_x, block_y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = MONSTER_SPEED
        self.block_x = block_x
        self.block_y = block_y
        self.x = block_x * CellSize + CellSize  / 2
        self.y = block_y * CellSize + CellSize  / 2
        self.image = pygame.image.load('../images/monster/0.png').convert()
        self.image.convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.atk_cd = 0
        self.atk_sound = Sound('..\sound\MonsterAttack.wav')

    def find_path(self, target, maze_info):
        target_col, target_row = target
        start = (self.block_x, self.block_y)
        frontier = []
        heapq.heappush(frontier, (0, start)) # tuple of priority, cell
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        while not len(frontier) == 0:
            priority, current = heapq.heappop(frontier)
            #early exit
            if current == target:
                found_target = True
                break
            for neighbor in neighbors(current, len(maze_info[0]), len(maze_info)):
                col, row = neighbor
                neighbor_block = maze_info[row][col]
                neighbor_cost = 1000 if neighbor_block.cellType == 0 else 1

                new_cost = cost_so_far[current] + neighbor_cost
                if (neighbor not in cost_so_far or
                    new_cost < cost_so_far[neighbor]):
                    cost_so_far[neighbor] = new_cost
                    priority = heuristic(target_col, target_row,
                                            col, row)
                    priority += new_cost
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current

        path = [target]
        while path[-1]:
            path.append(came_from[path[-1]])
        # print(path)
        return path[-3] # Reverse order; -1: None, -2: current block, -3: next block



    def update(self, player, walls, maze_info):
        des_x = player.rect.centerx
        des_y = player.rect.centery
        delta_x = des_x - self.rect.centerx
        delta_y = des_y - self.rect.centery
        distance = math.sqrt(delta_y ** 2 + delta_x ** 2)
        origin_x = self.x
        origin_y = self.y

        if distance > 0 and distance <= MONSTER_VIEW_DISTANCE:
            player_block_pos = (int(des_x / CellSize), int(des_y / CellSize))
            if player_block_pos != (self.block_x, self.block_y):
                next_block_col, next_block_row = self.find_path(player_block_pos, maze_info)
                if next_block_col == self.block_x:
                    self.y += (next_block_row - self.block_y) * self.speed
                    move_along_axis = 'y'
                else:
                    self.x += (next_block_col - self.block_x) * self.speed
                    move_along_axis = 'x'
                # print('monster: '+ str((self.block_x, self.block_y)) + '      monster next:' + str((next_block_col, next_block_row)) + '      player:' + str(player_block_pos))
            self.rect.center = (self.x, self.y)
            collided_walls = pygame.sprite.spritecollide(self, walls, False)
            if len(collided_walls):
                wall = collided_walls[0]
                if move_along_axis == 'x':
                    self.x = origin_x
                    if wall.rect.centery > self.rect.centery:
                        self.y -= self.speed
                    else:
                        self.y += self.speed
                else:
                    self.y = origin_y
                    if wall.rect.centerx > self.rect.centerx:
                        self.x -= self.speed
                    else:
                        self.x += self.speed
                self.rect.center = (self.x, self.y)
            self.block_x = int(self.x / CellSize)
            self.block_y = int(self.y / CellSize)
        self.speed = MONSTER_SPEED

        # Attack!
        if self.atk_cd <= 0 and self.rect.colliderect(player.rect):
            self.atk_sound.play()
            player.health -= MONSTER_ATK_DMG
            self.atk_cd = MONSTER_ATK_CD
        self.atk_cd -= 1 if self.atk_cd > 0 else 0





    def draw(self, surface):
        surface.blit(self.image, self.rect)