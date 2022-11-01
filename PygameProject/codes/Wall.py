import pygame

class Wall(pygame.sprite.Sprite):
    
    def  __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([64, 64])
        self.image.fill((167, 255, 100))  
        self.image.set_colorkey((255, 100, 98))
        self.rect = self.image.get_rect(center=pos) 

        
    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)