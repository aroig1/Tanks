import pygame
import math

class BlueTank:
    def __init__(self):

        self.sprites = [pygame.image.load('SpriteImages/BlueTank/BlueTank1.bmp'), pygame.image.load('SpriteImages/BlueTank/BlueTank2.bmp'),
                   pygame.image.load('SpriteImages/BlueTank/BlueTank3.bmp'), pygame.image.load('SpriteImages/BlueTank/BlueTank4.bmp')]
        self.image = self.sprites[0]
        self.x = 600
        self.y = 400

        self.turret = pygame.image.load('SpriteImages/BlueTank/BlueTurret2.bmp')
        self.turretX = self.x + (self.image.get_width() / 2) - (self.turret.get_width() / 2)
        self.turretY = self.y + (self.image.get_height() / 2) - 80


    def move(self, x, y):
        self.x += x
        self.y += y
        self.turretX = self.x + (self.image.get_width() / 2) - (self.turret.get_width() / 2)
        self.turretY = self.y + (self.image.get_height() / 2) - 80

    def getTurret(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        width = mouse_x - (self.x + (self.image.get_width() / 2))
        height = mouse_y - (self.y + (self.image.get_height() / 2))

        if height != 0:
            angle = math.atan2(width, height)
            angle = math.degrees(angle)
            angle += 180

            # print(f'width: {width} \t height: {height} \t angle: {angle}')
            # print(f'mouse x: {mouse_x} \t mouse y: {mouse_y}')
            # print(f'tank x: {self.x} \t tank y: {self.y}')
            # print(self.image.get_height())
            
            # Rotate turret
            rotatedTurret = pygame.transform.rotate(self.turret, angle)

            # Adjust the position of the rotated turret
            turret_rect = rotatedTurret.get_rect()
            center_x = self.x + (self.image.get_width() / 2)
            center_y = self.y + (self.image.get_height() / 2)

            # Calculate the new top left position based on the anchor point
            turret_rect.center = (center_x, center_y)

            return rotatedTurret, turret_rect
        
        else:
            return self.turret, self.turret.get_rect()