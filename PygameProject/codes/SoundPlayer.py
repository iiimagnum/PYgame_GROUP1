import pygame

class Sound():
    def __init__(self, file):
        self.playing = False
        self.file = file
        self.sound = pygame.mixer.Sound(file)
    
    def play(self):
        if not self.playing:
            self.sound.play()