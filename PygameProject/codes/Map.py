from settings import *
import heapq

def heuristic(ax, ay, bx, by):
# Manhattan (or taxicab) distance on a square grid
    return abs(ax - bx) + abs(ay - by)

class Block:
    def __init__(self):
        self.has_user = False
        self.is_wall = False
        self.has_monster = False
        self.cost = 1
    
    def become_wall(self):
        self.is_wall = True
        self.cost = 1000

class Map:
    """ A class that break the map into several blocks for monster navigation.
    """
    def __init__(self):
        self.block_map = [ [Block() for j in range(MAZE_ROWS)] for i in range(MAZE_COLS)]
        self.player_block_index = None
        self.monster_block_index = None
    
    def add_wall(self, pos):
        col, row = pos
        self.block_map[col][row].become_wall()
    
    def update_user(self, start_block_index, end_block_index):
        if start_block_index:
            s_col, s_row = start_block_index
            self.block_map[s_col][s_row].has_user = False
            self.player_block_index = None
        if end_block_index:
            e_col, e_row = end_block_index
            self.block_map[e_col][e_row].has_user = True
            self.player_block_index = end_block_index
    
    def update_monster(self, start_block_index, end_block_index):
        if start_block_index:
            s_col, s_row = start_block_index
            self.block_map[s_col][s_row].has_monster = False
            self.monster_block_index = None
        if end_block_index:
            e_col, e_row = end_block_index
            self.block_map[e_col][e_row].has_monster = True
            self.monster_block_index = end_block_index

    def neighbors(self, block_index):
        col, row = block_index
        neighbors_list = []
        if col > 0:
            neighbors_list.append((col - 1, row))
        if row > 0:
            neighbors_list.append((col, row - 1))
        if col < MAZE_COLS - 1:
            neighbors_list.append((col + 1, row))
        if row < MAZE_ROWS - 1:
            neighbors_list.append((col, row + 1))
        return neighbors_list


    def find_path(self, start, target):
        target_col, target_row = target
        frontier = [ ]
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
            for neighbor in self.neighbors(current):
                col, row = neighbor
                neighbor_block = self.block_map[col][row]

                new_cost = cost_so_far[current] + neighbor_block.cost
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
        return path[:-1]


# test
if __name__ == "__main__":
    m = Map()

    m.add_wall((0, 1))
    m.add_wall((1, 2))
    m.update_user(None, (0, 0))
    m.update_monster(None, (0, 10))
    print(m.find_path((0, 10), (0, 0)))

