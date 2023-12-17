import pygame


class Block:
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.size = 75

        images = {'oak' : pygame.image.load('mapImages/oakWood.png'), 'birch' : pygame.image.load('mapImages/birchWood.png'), 
                'stone' : pygame.image.load('mapImages/stone.png'), 'dirt' : pygame.image.load('mapImages/dirt.png'), 
                'gravel' : pygame.image.load('mapImages/gravel.png')}
        self.image = images[texture]

    def display(self, screen):
        screen.blit(self.image, (self.x, self.y))