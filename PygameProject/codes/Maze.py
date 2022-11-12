import random
from InputManager import *
import  pygame
import  numpy
from Monster import Monster
from settings import *
from InteractivePoint import  *
#using DFS to Summon the Maze

class MazeCell:

    BlockPath="../images/maze/Block/Block_"
    PathPath="../images/maze/Path/Path_"

    def __init__(self, position, type, imgID=0):
        """
        :param position=(y,x):position 中的x，y仅表示位于第几格,而非rect的坐标
        """
        self.x=position[1]
        self.y=position[0]
        self.cellType=type# 0 is wall , 1 is passage ,2 is interactPoint
        if self.cellType==0:
            self.img=pygame.image.load(MazeCell.BlockPath + str(imgID) + ".png").convert().convert_alpha()
        elif self.cellType==1:
            self.img=pygame.image.load(MazeCell.PathPath+str(imgID)+".png").convert().convert_alpha()
        self.img=pygame.transform.scale(self.img,(CellSize,CellSize))
        self.rect=self.img.get_rect()
        self.rect.topleft=(self.x*CellSize,self.y*CellSize)
    def draw(self,surface):
        surface.blit(self.img,self.rect)
    pass

class Maze:

    def __init__(self):
        self.CurrentMazeInfo=numpy.zeros((MAZE_Y * 2 + 1, MAZE_X * 2 + 1), dtype=MazeCell)
        self.InteractPointList=[]
        self.wallList=[]

    def SummonMaze(self):

        #Initialize the maze and its cells
        maze=numpy.zeros((MAZE_Y * 2 + 1, MAZE_X * 2 + 1), dtype=int)
        self.InteractPointList.clear()
        #DFS to generate the maze
        stack=[]
        x= random.randint(0, MAZE_X - 1) * 2 + 1
        y= random.randint(0, MAZE_Y - 1) * 2 + 1
        maze[y,x]=1
        stack.append((y,x))
        while len(stack)>0:
            (y,x)=stack.pop()
            neighbourList=[]
            if x-2>0:
                if maze[y,x-2]==0:
                    neighbourList.append((y,x-2))
            if x+2<MAZE_X*2:
                if maze[y,x+2]==0:
                    neighbourList.append((y,x+2))
            if y-2>0:
                if maze[y-2,x]==0:
                    neighbourList.append((y-2,x))
            if y+2<MAZE_Y*2:
                if maze[y+2,x]==0:
                    neighbourList.append((y+2,x))

            if len(neighbourList)>0:
                stack.append((y,x))
                (ny,nx)=random.choice(neighbourList)
                maze[ny,nx]=1
                maze[int((ny+y)/2),int((nx+x)/2)]=1
                stack.append((ny,nx))
            pass

        #Delete some walls
        maze=self.__RemoveWallPJVersion__(maze, 3, 3)


        # Decide the img of the cell
        for i in range(MAZE_Y * 2 + 1):
            for j in range(MAZE_X * 2 + 1):
                if maze[i,j]==1:
                    self.CurrentMazeInfo[i,j]=MazeCell((i,j),1,random.randint(1,32))
                else:
                    obstacleValue=0
                    if i == 0:  # the cell is on the first row
                        if j == 0:# cell is (0,0)
                            obstacleValue=16*abs(1-maze[i,j+1])+64*abs(1-maze[i+1,j])
                            if maze[i,j+1]==0 and maze[i+1,j]==0:
                                obstacleValue+=128*abs(1-maze[i+1,j+1])
                            self.CurrentMazeInfo[i,j]=MazeCell((i,j),0,obstacleValue)
                            continue

                        if j == MAZE_X * 2:#cell is (MAZE_COLS*2,0)
                            obstacleValue=8*abs(1-maze[i,j-1])+64*abs(1-maze[i+1,j])
                            if maze[i,j-1]==0 and maze[i+1,j]==0:
                                obstacleValue+=32*abs(1-maze[i+1,j-1])
                            self.CurrentMazeInfo[i,j]=MazeCell((i,j),0,obstacleValue)
                            continue
                        #cell is in the first row
                        powTime=3
                        for dy in range(0,2):
                            for dx in range(-1,2):
                                if dx==0 and dy==0:
                                    continue
                                if (dx==0 and dy!=0) or (dx!=0 and dy==0):
                                    #print(abs(1-maze[i+dy,j+dx]))
                                    obstacleValue +=(pow(2,powTime))*abs(1-maze[i+dy,j+dx])
                                else: #位于对角线
                                    if maze[i+dy,j]==0 and maze[i,j+dx]==0:
                                        obstacleValue +=(pow(2,powTime)) * abs(1-maze[ i + dy,j + dx])

                                powTime+=1
                        self.CurrentMazeInfo[i, j] = MazeCell((i, j), 0, obstacleValue)
                        continue

                    if i == MAZE_Y * 2:
                        if j == 0:#cell at (0,MAZE_ROWS*2)
                            obstacleValue+=2*abs(1-maze[i-1,j])+16*abs(1-maze[i,j+1])
                            if maze[i-1,j]==0 and maze[i,j+1]==0:
                                obstacleValue += 4*abs(1-maze[i-1,j+1])
                            self.CurrentMazeInfo[i,j]=MazeCell((i,j),0,obstacleValue)
                            continue
                        if j == MAZE_X * 2:#cell at right bottom
                            obstacleValue+=2*abs(1-maze[i-1,j])+8*abs(1-maze[i,j-1])
                            if maze[i-1,j]==0 and maze[i,j-1]==0:
                                obstacleValue += 1*abs(1-maze[i-1,j-1])
                            self.CurrentMazeInfo[i, j] = MazeCell((i, j), 0, obstacleValue)
                            continue
                        #Cell at last row
                        powTime = 0
                        for dy in range(-1, 1):
                            for dx in range(-1, 2):
                                if dx == 0 and dy == 0:
                                    continue
                                if (dx == 0 and dy != 0) or (dx != 0 and dy == 0):
                                    obstacleValue +=(pow(2,powTime)) * abs(1-maze[ i + dy,j + dx])
                                else:  # 位于对角线
                                    if maze[i + dy,j] == 0 and maze[i,j + dx] == 0:
                                        obstacleValue +=(pow(2,powTime)) * abs(1-maze[ i + dy,j + dx])
                                powTime += 1
                        self.CurrentMazeInfo[i, j] = MazeCell((i, j), 0, obstacleValue)
                        continue

                    #Cell.y is between (1,MAZE_ROWS*2-1)
                    if j==0:
                        obstacleValue=2*abs(1-maze[i-1,j])+16*abs(1-maze[i,j+1])+64*abs(1-maze[i+1,j])
                        if maze[i-1,j]==0 and maze[i,j+1]==0:
                            obstacleValue+=4*abs(1-maze[i-1,j+1])
                        if maze[i+1,j]==0 and maze[i,j+1]==0:
                            obstacleValue+=128*abs(1-maze[i+1,j+1])
                        self.CurrentMazeInfo[i,j]=MazeCell((i,j),0,obstacleValue)
                        continue

                    if j==MAZE_X*2:
                        obstacleValue = 2 * abs(1-maze[ i - 1,j] )+ 8 * abs(1-maze[i,j - 1]) + 64 * abs(1-maze[ i + 1,j])
                        if maze[ i - 1,j] == 0 and maze[i,j - 1] == 0:
                            obstacleValue += 1* abs(1-maze[i - 1, j - 1])
                        if maze[ i + 1,j] == 0 and maze[i,j - 1] == 0:
                            obstacleValue += 32 * abs(1-maze[i + 1, j -1])
                        self.CurrentMazeInfo[i,j]=MazeCell((i,j),0,obstacleValue)
                        continue

                    powTime=0
                    obstacleValue=0
                    for dy in range(-1,2):
                        for dx in range(-1,2):
                            if dx==0 and dy==0:
                                continue
                            if (dx==0 and dy!=0) or (dx!=0 and dy==0):#检测对角线，如果不是先加上
                                obstacleValue+=pow(2,powTime)*abs(1-maze[i+dy,j+dx])
                            elif maze[i,j+dx]==0 and maze[i+dy,j]==0:
                                obstacleValue+=pow(2,powTime)*abs(1-maze[i+dy,j+dx])
                            powTime+=1
                            self.CurrentMazeInfo[i,j]=MazeCell((i,j),0,obstacleValue)

        #Add the interact point
        self.SummonInteractPoint(3, 1, 1)

        pass

    def draw(self,surface):
        drawSurface=pygame.Surface(((MAZE_X * 2 + 1) * CellSize, (MAZE_Y * 2 + 1) * CellSize))
        for y in range(MAZE_Y * 2 + 1):
            for x in range(MAZE_X * 2 + 1):
                drawSurface.blit(self.CurrentMazeInfo[y,x].img,self.CurrentMazeInfo[y,x].rect)

        for ip in self.InteractPointList:
            if ip.type == InteractType.Soil:
                drawSurface.blit(ip.img, (ip.rect.centerx - 10, ip.rect.centery - 10))
            elif ip.type == InteractType.Fruit:
                drawSurface.blit(ip.img, (ip.rect.centerx - 15, ip.rect.centery - 15))
            else:
                drawSurface.blit(ip.img, ip.rect)
        surface.blit(drawSurface,drawSurface.get_rect())

    def __RemoveWall__(self,maze,RemoveNum):
        distanceMaze = numpy.zeros((MAZE_Y * 2 + 1, MAZE_X * 2 + 1), dtype=int)
        distanceMaze.fill(999999)
        visitedList = []
        wallList = []
        # using BFS to set the distance
        stack = []
        x = random.randint(1, MAZE_X - 1) * 2
        y = random.randint(1, MAZE_Y - 1) * 2
        visitedList.append((y,x))
        maze[y,x] = 0
        stack.append((y,x))
        while len(stack):
            (y,x) = stack.pop(0)
            if y - 1 > 0:  # 上
                if maze[ y - 1,x] == 1:
                    maze[y - 1,x] = min(maze[y - 1,x], maze[ y,x] + 1)
                    if not visitedList.__contains__(( y - 1,x)):
                        stack.append((y - 1,x))
                        visitedList.append(( y - 1,x))
                else:
                    if not wallList.__contains__(( y - 1,x)):
                        wallList.append(( y - 1,x))
            if y - 1 < MAZE_X * 2 + 1:
                if maze[ y + 1,x] == 1:
                    maze[ y + 1,x] = min(maze[ y + 1,x], maze[ y,x] + 1)
                    if not visitedList.__contains__(( y + 1,x)):
                        stack.append(( y + 1,x))
                        visitedList.append((y + 1,x))
                    else:
                        if not wallList.__contains__(( y + 1,x)):
                            wallList.append(( y + 1,x))
            if x - 1 > 0:
                if maze[y,x - 1] == 1:
                    maze[y,x - 1] = min(maze[y,x - 1], maze[y,x] + 1)
                    if not visitedList.__contains__((y,x - 1)):
                        stack.append((y,x - 1))
                        visitedList.append((y,x - 1))
                    else:
                        if not wallList.__contains__((y,x - 1)):
                            wallList.append((y,x - 1))
            if x + 1 < MAZE_Y * 2 + 1:
                if maze[y,x + 1] == 1:
                    maze[y,x + 1] = min(maze[y,x + 1], maze[y,x] + 1)
                    if not visitedList.__contains__((y,x + 1)):
                        stack.append((y,x + 1))
                        visitedList.append((y,x + 1))
                    else:
                        if not wallList.__contains__((y,x + 1)):
                            wallList.append((y,x + 1))
            pass
        # End bfs
        while RemoveNum > 0 and len(wallList) > 0:
            wallX = -1
            wallY = -1
            maxDistance = -1
            for (y,x) in wallList:
                if x % 2 == 1:
                    dis = abs(distanceMaze[ y - 1,x] - distanceMaze[ y + 1,x])
                    if dis > maxDistance:
                        maxDistance = dis
                        wallX = x
                        wallY = y
                    pass
                else:
                    dis = abs(distanceMaze[y,x - 1] - distanceMaze[y,x + 1])
                    if dis > maxDistance:
                        maxDistance = dis
                        wallX = x
                        wallY = y
            if maxDistance > -1:
                wallList.remove((wallY,wallX))
                # print(f"Remove {(wallX,wallY)}")
                for i in range(4):
                    for j in range(4):
                        if (wallX + i - 2 > 0 and wallX + i - 2 < MAZE_Y * 2) and (
                                wallY + j - 2 > 0 and wallY + j - 2 < MAZE_X * 2) and wallList.__contains__((wallY + j - 2, wallX + i - 2)):
                            wallList.remove((wallY + j - 2,wallX + i - 2))

                RemoveNum -= 1
                maze[ wallY,wallX] = 1
        # print(f"Now removed {RemoveNum}")
        return maze
        pass
    def __RemoveWallPJVersion__(self, maze, remDis, randRange):
        for x in range(1,MAZE_X-1):
            curLasting=0
            rdDis=remDis+random.randint(int(-randRange/2),randRange)
            for y in range(2,MAZE_Y*2-1):
                if maze[y,x*2]==0:
                    curLasting=curLasting+1
                    if curLasting>=rdDis and maze[y,x*2+1]+maze[y,x*2-1]==2:
                        maze[y,x*2]=1
                        curLasting=0
                else:
                    curLasting=0

        for y in range(1, MAZE_Y - 1):
            curLasting = 0
            rdDis = remDis + random.randint(int(-randRange/2), randRange)
            for x in range(2, MAZE_X * 2 - 1):
                if maze[y*2, x ] == 0:
                    curLasting = curLasting + 1
                    if curLasting >= rdDis and maze[y* 2 + 1, x ] + maze[y* 2 - 1, x ] == 2:
                        maze[y*2, x ] = 1
                        curLasting = 0
                else:
                    curLasting = 0

        for i in range(2,MAZE_Y*2):
            for j in range(2,MAZE_X*2):
                if maze[i,j]==0:
                    if maze[i-1,j]+maze[i+1,j]+maze[i,j-1]+maze[i,j+1]==4:
                        d=[(-1,0),(1,0),(0,1),(0,-1)]
                        (dx,dy)=random.choice(d)
                        maze[i+dy,j+dx]=0

        return maze

    def SummonInteractPoint(self,treasureNum,soilNum,fruitNum):
        while treasureNum>0:
            treasureNum-=1
            while True:
                x=random.randint(1,MAZE_X*2)
                y=random.randint(1,MAZE_Y*2)
                if self.CurrentMazeInfo[y,x].cellType==1:
                    self.CurrentMazeInfo[y,x].cellType=2
                    ip=Treasure((y,x))
                    self.InteractPointList.append(ip)
                    break

        while soilNum>0:
            soilNum-=1
            while True:
                x=random.randint(1,MAZE_X*2)
                y=random.randint(1,MAZE_Y*2)
                if self.CurrentMazeInfo[y,x].cellType==1:
                    self.CurrentMazeInfo[y,x].cellType=2
                    ip=Soil_ip((y,x))
                    self.InteractPointList.append(ip)
                    break

        while fruitNum>0:
            fruitNum-=1
            while True:
                x=random.randint(1,MAZE_X*2)
                y=random.randint(1,MAZE_Y*2)
                if self.CurrentMazeInfo[y,x].cellType==1:
                    self.CurrentMazeInfo[y,x].cellType=2
                    ip=Fruit_ip((y,x))
                    self.InteractPointList.append(ip)
                    break

        while True:
            x = random.randint(1, MAZE_X * 2)
            y = random.randint(1, MAZE_Y * 2)
            if self.CurrentMazeInfo[y, x].cellType == 1:
                self.CurrentMazeInfo[y, x].cellType = 2
                ex=ExitPoint((y,x))
                self.InteractPointList.append(ex)
                break
    
    def SummonMonster(self, monsterNum):
        monster_list = []
        while monsterNum > 0:
            monsterNum -= 1
            while True:
                x = random.randint(1, MAZE_X * 2)
                y = random.randint(1, MAZE_Y * 2)
                if self.CurrentMazeInfo[y, x].cellType == 1:
                    monster = Monster(x, y)
                    monster_list.append(monster)
                    break
        return monster_list

if __name__ == '__main__':
    pygame.init()
    MainSurface=pygame.display.set_mode(((MAZE_X * 2 + 1) * CellSize, (MAZE_Y * 2 + 1) * CellSize))
    maze=Maze()
    maze.SummonMaze()
    while True:
        InputManager.update()
        if InputManager.keyDownList.__contains__(pygame.K_ESCAPE) or InputManager.keyDownList.__contains__(pygame.K_q):
            break
            pass
        if InputManager.keyDownList.__contains__(pygame.K_1):
            maze.SummonMaze()
        maze.draw(MainSurface)
        pygame.display.flip()

    pass
