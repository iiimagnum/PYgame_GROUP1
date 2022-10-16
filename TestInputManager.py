import sys, random
import pygame
import pygame.locals
import pygame.time
import  copy
pygame.init()
isLooping=True
surface=pygame.display.set_mode((500,500))

class InputManager:
    keyDownList=[]
    keyPressList=[]
    keyUpList=[]
    _lastKeyDownList_=[]
    @staticmethod
    def update():
        InputManager._lastKeyDownList_ = copy.deepcopy(InputManager.keyDownList)
        InputManager.keyDownList.clear()
        InputManager.keyUpList.clear()
        for event in pygame.event.get():
            if event.type==pygame.KEYUP:
                InputManager.keyUpList.append(event.key)

            if event.type==pygame.KEYDOWN:
                    InputManager.keyDownList.append(event.key)

        for key in InputManager.keyUpList:
            if  InputManager.keyPressList.__contains__(key):
                InputManager.keyPressList.remove(key)
        for key in InputManager._lastKeyDownList_:
            if not InputManager.keyPressList.__contains__(key):
                InputManager.keyPressList.append(key)


if __name__ == '__main__':
    clock = pygame.time.Clock()
    counter=0
    while isLooping:
        clock.tick(60)
        #print(counter)
        counter+=1
        InputManager.update()
        for key in InputManager.keyDownList:
            print(str(key)+"is Down")

        for key in InputManager.keyPressList:
            print(str (key)+"is Pressing")

        for key in InputManager.keyUpList:
            print(str(key) +"is Up")

        if InputManager.keyDownList.__contains__(pygame.K_ESCAPE):
            isLooping=False
