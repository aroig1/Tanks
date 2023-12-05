import pygame


class Block:
    def __init__(self, x, y, i):
        self.x = x
        self.y = y
        self.size = 75

        images = [pygame.image.load('mapImages/oakWood.png'), pygame.image.load('mapImages/birchWood.png'), 
                       pygame.image.load('mapImages/stone.png')]
        self.image = images[i]

    def display(self, screen):
        screen.blit(self.image, (self.x, self.y))