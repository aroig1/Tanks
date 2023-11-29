import pygame
import math
from settings import Settings

class BrownBullet:
    def __init__(self, x, y, player_x, player_y):
        self.x = x
        self.y = y

        self.settings = Settings()

        self.bulletSpeed = 5

        self.originalImage = pygame.image.load('SpriteImages/Projectiles/bullet1.bmp')
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

        self.x += 15 * self.xVelocity
        self.y += 15 * self.yVelocity

    def rotateImage(self, width, height):
        if height != 0:
            angle = math.atan2(width, height)
            angle = math.degrees(angle)
            angle = angle - 90
        else:
            angle = 0

        self.image = pygame.transform.rotate(self.originalImage, angle)
        return angle

    def updatePos(self):
        self.x += self.xVelocity
        self.y += self.yVelocity
        if self.x <= 0 or self.x >= self.settings.screenSize[0]:
            return True
        elif self.y <= 0 or self.y >= self.settings.screenSize[1]:
            return True
        return False

