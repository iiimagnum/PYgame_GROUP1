import pygame
import  numpy
import  random
import  InputManager as Inp
MazeSize_Width=15
MazeSize_Height=10
BlockSize=20
def Aldous_Broder():
    Maze=numpy.zeros((MazeSize_Width*2+1,MazeSize_Height*2+1),dtype=int)

    VisitedCell=[]
    curX=random.randint(0,MazeSize_Width-1)
    curY=random.randint(0,MazeSize_Height-1)
    Maze[curX*2+1,curY*2+1]=1
    VisitedCell.append(curY*MazeSize_Width+curX)
    while len(VisitedCell)<MazeSize_Width*MazeSize_Height:
        (nextX,nextY)=GetNeighbour(curX,curY)
        if nextX==-1:
            curX = random.randint(0, MazeSize_Width - 1)
            curY = random.randint(0, MazeSize_Height - 1)
            continue
        if not VisitedCell.__contains__(nextY*MazeSize_Width+nextX):
            Maze[nextX+curX+1,nextY+curY+1]=1
            Maze[nextX*2+1,nextY*2+1]=1
            VisitedCell.append(nextY*MazeSize_Width+nextX)
            pass
        curX=nextX
        curY=nextY
        pass
    return  Maze
    pass

def Prim():
    maze=numpy.zeros((MazeSize_Width*2+1,MazeSize_Height*2+1),dtype=int)
    wallList=[]
    x=random.randint(0,MazeSize_Width-1)*2+1
    y=random.randint(0,MazeSize_Height-1)*2+1
    maze[x,y]=1
    if x-1>0:
        wallList.append((x-1,y))
    if x+1<MazeSize_Width*2:
        wallList.append((x+1,y))
    if y-1>0:
        wallList.append((x,y-1))
    if y+1<MazeSize_Height*2:
        wallList.append((x,y+1))

    while len(wallList)>0:
        (wallX,wallY)=random.choice(wallList)
        wallList.remove((wallX,wallY))
        if wallX%2==1:#Vertical Wall,  check Y
            if maze[wallX,wallY-1]+ maze[wallX,wallY+1]==1:
                maze[wallX,wallY]=1
                if maze[wallX, wallY - 1]==0:
                    maze[wallX, wallY - 1]=1
                    x=wallX
                    y=wallY-1
                    if x-1>0:
                        wallList.append((x-1,y))
                    if x+1<MazeSize_Width*2:
                        wallList.append((x+1,y))
                    if y-1>0:
                        wallList.append((x,y-1))
                    if y+1<MazeSize_Height*2:
                        wallList.append((x,y+1))

                else:
                    maze[wallX, wallY + 1]=1
                    x=wallX
                    y=wallY+1
                    if x-1>0:
                        wallList.append((x-1,y))
                    if x+1<MazeSize_Width*2:
                        wallList.append((x+1,y))
                    if y-1>0:
                        wallList.append((x,y-1))
                    if y+1<MazeSize_Height*2:
                        wallList.append((x,y+1))

            pass

        else:#Horizontal wall,check X
            if maze[wallX-1,wallY]+maze[wallX+1,wallY]==1:
                maze[wallX, wallY] = 1
                if maze[wallX-1, wallY] == 0:
                    maze[wallX - 1, wallY] = 1
                    x = wallX - 1
                    y = wallY
                    if x - 1 > 0:
                        wallList.append((x - 1, y))
                    if x + 1 < MazeSize_Width * 2:
                        wallList.append((x + 1, y))
                    if y - 1 > 0:
                        wallList.append((x, y - 1))
                    if y + 1 < MazeSize_Height * 2:
                        wallList.append((x, y + 1))

                else:
                    maze[wallX+ 1, wallY ] = 1
                    x = wallX+ 1
                    y = wallY
                    if x - 1 > 0:
                        wallList.append((x - 1, y))
                    if x + 1 < MazeSize_Width * 2:
                        wallList.append((x + 1, y))
                    if y - 1 > 0:
                        wallList.append((x, y - 1))
                    if y + 1 < MazeSize_Height * 2:
                        wallList.append((x, y + 1))
            pass
    return  maze
    pass

def DFS():
    maze = numpy.zeros((MazeSize_Width * 2 + 1, MazeSize_Height * 2 + 1), dtype=int)
    stack=[]
    x=random.randint(0,MazeSize_Width-1)*2+1
    y=random.randint(0,MazeSize_Height-1)*2+1
    maze[x,y]=1
    stack.append((x,y))
    while len(stack)>0:
        (x,y)=stack.pop()
        neighbourList=[]
        if x-2>0:
            if maze[x-2,y]==0:
                neighbourList.append((x-2,y))
        if x+2<MazeSize_Width*2:
            if maze[x + 2, y] == 0:
                neighbourList.append((x+2,y))
        if y-2>0:
            if maze[x, y - 2] == 0:
                neighbourList.append((x,y-2))
        if y+2<MazeSize_Height*2:
            if maze[x, y + 2] == 0:
                neighbourList.append((x,y+2))

        if len(neighbourList)>0:
            stack.append((x,y))
            (nx,ny)=random.choice(neighbourList)
            maze[nx,ny]=1
            maze[int( (nx+x)/2),int((ny+y)/2)]=1
            stack.append((nx,ny))


    return  maze
    pass

def DrawMaze(maze):
    drawSurface=pygame.Surface(((MazeSize_Width*2+1)*BlockSize,(MazeSize_Height*2+1)*BlockSize))
    for y in range(MazeSize_Height*2):
        for x in range(MazeSize_Width*2):
            if maze[x,y]==1:
                pygame.draw.rect(drawSurface,(255,255,255),(x*BlockSize,y*BlockSize,BlockSize,BlockSize))
                pass
            else:
                pygame.draw.rect(drawSurface, (0, 0, 0), (x * BlockSize, y * BlockSize, BlockSize, BlockSize))
                pass
            pass
        pass
    return drawSurface
    pass

def GetNeighbour(x,y):
    list=[]
    if x-1>=0:
        list.append((x-1,y))
    if x+1<MazeSize_Width:
        list.append((x+1,y))
    if y-1>=0:
        list.append((x,y-1))
    if y+1<MazeSize_Height:
        list.append((x,y+1))
    if len(list)>0:
        return random.choice(list)
    else:
        return (-1,-1)
    pass

def RemoveWall(Maze,RemoveNum):
    while RemoveNum>0:
        x=random.randint(1,MazeSize_Width-1)*2
        y=random.randint(1,MazeSize_Height-1)*2
        if Maze[x,y]==0:
            if Maze[x-1,y]+Maze[x+1,y]==2 or Maze[x,y-1]+Maze[x,y+1]==2:
                Maze[x,y]=1
                RemoveNum-=1
    return  Maze
    pass

def RemoveWallAreaVersion(Maze,RemoveNum):
    delta=int(((2*MazeSize_Width-1)*(2*MazeSize_Height-1)/RemoveNum))
    #print(f"delta is {delta}")
    for i in range(RemoveNum):
        while True:
            id=random.randint(i*delta,(i+1)*delta)
            x=id%(2*MazeSize_Width-1)
            y=int( id/(2*MazeSize_Width-1))
            #print(f"Test X{x} Y{y}")
            if Maze[x, y] == 0:
                if Maze[x - 1, y] + Maze[x + 1, y] == 2 or Maze[x, y - 1] + Maze[x, y + 1] == 2:
                    Maze[x, y] = 1
                    RemoveNum -= 1
            break

    return  Maze
    pass

def RemoveWallDistanceVersion(maze,RemoveNum):
    distanceMaze=numpy.zeros((MazeSize_Width*2+1,MazeSize_Height*2+1),dtype=int)
    distanceMaze.fill(999999)
    visitedList=[]
    wallList=[]
    #using BFS to set the distance
    stack=[]
    x = random.randint(1, MazeSize_Width - 1) * 2
    y = random.randint(1, MazeSize_Height - 1) * 2
    visitedList.append((x,y))
    maze[x,y]=0
    stack.append((x,y))
    while len(stack):
        (x,y)=stack.pop()
        if y-1>0:#上
            if maze[x,y-1]==1 :
                maze[x,y-1]=min(maze[x,y-1],maze[x,y]+1)
                if not visitedList.__contains__((x,y-1)):
                    stack.append((x,y-1))
                    visitedList.append((x,y-1))
            else:
                if not wallList.__contains__((x,y-1)):
                    wallList.append((x,y-1))
        if y-1<MazeSize_Height*2+1:
            if maze[x,y+1]==1:
                maze[x,y+1]=min(maze[x,y+1],maze[x,y]+1)
                if not visitedList.__contains__((x,y+1)):
                    stack.append((x,y+1))
                    visitedList.append((x, y +1))
                else:
                 if not wallList.__contains__((x,y+1)):
                     wallList.append((x,y+1))
        if x-1>0:
            if maze[x-1,y]==1:
                maze[x-1,y]=min(maze[x-1,y],maze[x,y]+1)
                if not visitedList.__contains__((x-1,y)):
                    stack.append((x-1,y))
                    visitedList.append((x-1, y))
                else:
                    if not wallList.__contains__((x-1,y)):
                        wallList.append((x-1,y))
        if x+1<MazeSize_Width*2+1:
            if maze[x+1,y]==1:
                maze[x+1,y]=min(maze[x+1,y],maze[x,y]+1)
                if not visitedList.__contains__((x+1,y)):
                    stack.append((x+1,y))
                    visitedList.append((x+1, y))
                else:
                    if not wallList.__contains__((x+1,y)):
                        wallList.append((x+1,y))
        pass
    #End bfs
    while RemoveNum>0 and len(wallList)>0:
        wallX=-1
        wallY=-1
        maxDistance=-1
        for (x,y) in wallList:
            if x%2==1:
                dis=abs(distanceMaze[x,y-1]-distanceMaze[x,y+1])
                if dis>maxDistance:
                    maxDistance=dis
                    wallX=x
                    wallY=y
                pass
            else:
                dis = abs(distanceMaze[x-1, y] - distanceMaze[x+1, y])
                if dis>maxDistance:
                    maxDistance=dis
                    wallX=x
                    wallY=y
        if maxDistance>-1:
            wallList.remove((wallX,wallY))
            print(f"Remove {(wallX,wallY)}")
            for i in range(4):
                for j in range(4):
                    if (wallX+i-2>0 and wallX+i-2<MazeSize_Width*2) and (wallY+j-2>0 and wallY+j-2<MazeSize_Height*2) and wallList.__contains__((wallX+i-2,wallY+j-2)):
                        wallList.remove((wallX+i-2,wallY+j-2))

            RemoveNum-=1
            maze[wallX,wallY]=1

    print(f"Now removed {RemoveNum}")
    return  maze
    pass

def main():
    pygame.init()
    MainSurface=pygame.display.set_mode([(MazeSize_Width*2+1)*BlockSize,(MazeSize_Height*2+1)*BlockSize])
    MazeInfo=numpy.zeros((MazeSize_Width,MazeSize_Height),dtype=int)
    #MazeInfo[1,2]=1
    MazeInfo = DFS()
    MazeInfo= RemoveWallDistanceVersion(MazeInfo,30)
    while True:
        Inp.InputManager.update()
        if Inp.InputManager.keyDownList.__contains__(pygame.K_ESCAPE) or Inp.InputManager.keyDownList.__contains__(pygame.K_q):
            break
            pass
        if Inp.InputManager.keyDownList.__contains__(pygame.K_1):
            MazeInfo = Aldous_Broder()
            MazeInfo= RemoveWallDistanceVersion(MazeInfo,30)
        if Inp.InputManager.keyDownList.__contains__(pygame.K_2):
            MazeInfo = Prim()
            MazeInfo = RemoveWallDistanceVersion(MazeInfo, 30)
        if Inp.InputManager.keyDownList.__contains__(pygame.K_3):
            MazeInfo = DFS()
            MazeInfo = RemoveWallDistanceVersion(MazeInfo, 30)

        drawSurface=DrawMaze(MazeInfo)
        MainSurface.blit( drawSurface,drawSurface.get_rect())

        pygame.display.flip()
        pass
    pass
if __name__ == '__main__':
    main()
    pass
