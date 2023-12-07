import pygame
import math
from bullet import Bullet
from settings import Settings
from block import Block

class BlueBullet(Bullet):
    def __init__(self, x, y):

        super().__init__(x, y)

        self.bounceMax = 1
        self.type = "player"

        self.originalImage = pygame.image.load('SpriteImages/Projectiles/bullet.bmp')
        self.image = self.originalImage

        mouse_x, mouse_y = pygame.mouse.get_pos()

        width = mouse_x - (self.x + (self.image.get_width() / 2))
        height = mouse_y - (self.y + (self.image.get_height() / 2))

        angle = self.rotateImage(width, height)

        if angle >= 0:
            self.xVelocity = self.settings.bulletSpeed * math.cos(math.radians(angle))
            self.yVelocity = -1 * self.settings.bulletSpeed * math.sin(math.radians(angle))
        elif angle >= -90:
            self.xVelocity = self.settings.bulletSpeed * math.cos(math.radians(angle))
            self.yVelocity = -1 * self.settings.bulletSpeed * math.sin(math.radians(angle))
        elif angle >= -180:
            self.xVelocity = self.settings.bulletSpeed * math.cos(math.radians(angle))
            self.yVelocity = -1 * self.settings.bulletSpeed * math.sin(math.radians(angle))
        else:
            self.xVelocity = self.settings.bulletSpeed * math.cos(math.radians(angle))
            self.yVelocity = -1 * self.settings.bulletSpeed * math.sin(math.radians(angle))

        self.x += 15 * self.xVelocity
        self.y += 15 * self.yVelocity
