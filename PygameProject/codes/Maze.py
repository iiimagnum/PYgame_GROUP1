import  pygame
from settings import *
#using DFS to Summon the Maze

class MazeCell:
    CellSize=10
    imgList=[]
    imgPath="../images/maze/Block"
    for i in range(48):
        img=pygame.image.load(imgPath+"Block_"+i.__str__()+".png").convert()
        img.convert_alpha()
        img.set_colorkey((255, 255, 255))

    def __init__(self):
        self.CellType=0# 0 is wall , 1 is passage ,
        self.rect=pygame.Rect(0,0,MazeCell.CellSize,MazeCell.CellSize)
        self.imageList=[]


    pass