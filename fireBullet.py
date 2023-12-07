import pygame
import math
from bullet import Bullet
from settings import Settings
from block import Block

class FireBullet(Bullet):
    def __init__(self, x, y, player_x, player_y):

        super().__init__(x, y)

        self.bulletSpeed = 15
        self.bounceMax = 0
        self.type = "enemy"

        self.originalImage = pygame.image.load('SpriteImages/Projectiles/fireBullet.bmp')
        self.image = self.originalImage

        width = player_x - (self.x + (self.image.get_width() / 2))
        height = player_y - (self.y + (self.image.get_height() / 2))

        angle = self.rotateImage(width, height)

        if angle >= 0:
            self.xVelocity = self.bulletSpeed * math.cos(math.radians(angle))
            self.yVelocity = -1 * self.bulletSpeed * math.sin(math.radians(angle))
        elif angle >= -90:
            self.xVelocity = self.bulletSpeed * math.cos(math.radians(angle))
            self.yVelocity = -1 * self.bulletSpeed * math.sin(math.radians(angle))
        elif angle >= -180:
            self.xVelocity = self.bulletSpeed * math.cos(math.radians(angle))
            self.yVelocity = -1 * self.bulletSpeed * math.sin(math.radians(angle))
        else:
            self.xVelocity = self.bulletSpeed * math.cos(math.radians(angle))
            self.yVelocity = -1 * self.bulletSpeed * math.sin(math.radians(angle))

        self.x += 8 * self.xVelocity
        self.y += 8 * self.yVelocity