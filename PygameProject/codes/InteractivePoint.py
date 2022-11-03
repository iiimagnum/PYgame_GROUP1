import pygame
from settings import  *
from  enum import  Enum
class InteractPoint:
    resourcePath="../images/interactPoint/"
    def __init__(self,position,type,imgPath):
        self.x=position[1]
        self.y=position[0]
        self.type=type
        self.img=pygame.image.load(InteractPoint.resourcePath+imgPath).convert_alpha()
        self. img.set_colorkey(self.img.get_at((0,0)))
        self.img=pygame.transform.scale(self.img,(CellSize,CellSize))
        self.rect=self.img.get_rect()
        self.rect.topleft=(self.x*CellSize,self.y*CellSize)
    def draw(self,surface):
        surface.blit(self.img,self.rect)
        pass

    def Interact(self):
        """Used to overwrite. """
        pass
pass

class ExitPoint(InteractPoint):
    def __init__(self,position):
        InteractPoint.__init__(self,position,InteractType['Exit'],"Exit.png")

    def Interact(self):
        pass

class Treasure(InteractPoint):
    def __init__(self,position):
        InteractPoint.__init__(self,position,InteractType['Treasure'],"Coin.png")

    def Interact(self):
        pass


class InteractType(Enum):
    Exit=1
    Treasure=2
    Item=3
