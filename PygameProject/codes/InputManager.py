import pygame
import pygame.locals
import pygame.time
import copy


class InputManager:
    keyDownList = []
    keyPressList = []
    keyUpList = []
    _lastKeyDownList_ = []
    quit = False

    @staticmethod
    def update():
        InputManager._lastKeyDownList_ = copy.deepcopy(InputManager.keyDownList)
        InputManager.keyDownList.clear()
        InputManager.keyUpList.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                InputManager.quit = True
            if event.type == pygame.KEYUP:
                InputManager.keyUpList.append(event.key)

            if event.type == pygame.KEYDOWN:
                InputManager.keyDownList.append(event.key)

        for key in InputManager.keyUpList:
            if InputManager.keyPressList.__contains__(key):
                InputManager.keyPressList.remove(key)
        for key in InputManager._lastKeyDownList_:
            if not InputManager.keyPressList.__contains__(key):
                InputManager.keyPressList.append(key)
