import random

from pygame import *
from Player import *
from Maze import *
import numpy as np
class WarFogCell:
    def __init__(self,position):
        self.x=position[1]
        self.y=position[0]
        self.hasVisited=False
        self.imgs=[]
        img=image.load("../images/WarFog/fog0.png").convert_alpha()
        img = pygame.transform.scale(img, (CellSize, CellSize))
        self.imgs.append(img)
        img=image.load("../images/WarFog/fog1.png").convert_alpha()
        img = pygame.transform.scale(img, (CellSize, CellSize))
        self.imgs.append(img)
        self.rect=self.imgs[0].get_rect()
        self.rect.topleft=(self.x*CellSize,self.y*CellSize)
        pass

    def draw(self,surface):
        imgID=0
        if self.hasVisited:
            imgID=1
        surface.blit(self.imgs[imgID],self.rect)
    pass

class WarFogMaze:
    ViewDistance=4
    def __init__(self,maze):
        self.fogMaze=np.zeros((MAZE_Y*2+1,MAZE_X*2+1),dtype=WarFogCell)
        for i in range(MAZE_Y*2+1):
            for j in range(MAZE_X * 2 + 1):
                self.fogMaze[i,j]=WarFogCell((i,j))

        self.mazeDis=np.zeros((MAZE_Y*2+1,MAZE_X*2+1),dtype=int)
        for i in range(MAZE_Y*2+1):
            for j in range(MAZE_X * 2 + 1):
                self.mazeDis[i,j]=19260817
        self.mazeDis[1,1]=0
        frontier=[(1,1)]
        while len(frontier)>0:
            (y,x)=random.choice(frontier)
            minValue=self.mazeDis[y,x]
            for (iy,ix) in frontier:
                if self.mazeDis[iy,ix]<minValue:
                    (y,x)=(iy,ix)
                    minValue=self.mazeDis[iy,ix]
            frontier.remove((y,x))

            dpos=[(y-1,x),(y+1,x),(y,x-1),(y,x+1)]

            for (iy,ix) in dpos:
                if maze.CurrentMazeInfo[iy,ix].cellType==1:
                   if self.mazeDis[iy,ix]==19260817:
                       self.mazeDis[iy,ix]=1+self.mazeDis[y,x]
                       frontier.append((iy,ix))

    def update(self,playerPos):
        cellX=int(playerPos[0]/CellSize+0.5)
        cellY=int(playerPos[1]/CellSize+0.5)
        for dy in range(-1*min(WarFogMaze.ViewDistance, cellY - 1), min(WarFogMaze.ViewDistance, MAZE_Y * 2 - cellY)):
            for dx in range(-1*min(WarFogMaze.ViewDistance, cellX - 1), min(WarFogMaze.ViewDistance, MAZE_X * 2 - cellX)):
                if abs(self.mazeDis[cellY+dy,cellX+dx]-self.mazeDis[cellY,cellX])<=WarFogMaze.ViewDistance:
                    self.fogMaze[cellY+dy,cellX+dx].hasVisited=True

    def draw(self,surface,playerPos):
        for y in range(MAZE_Y * 2 + 1):
            for x in range(MAZE_X * 2 + 1):
                cellX=int(playerPos[0]/CellSize+0.5)
                cellY=int(playerPos[1]/CellSize+0.5)
                if abs( self.mazeDis[cellY,cellX]-self.mazeDis[y,x])<=WarFogMaze.ViewDistance:
                    continue

                self.fogMaze[y,x].draw(surface)
