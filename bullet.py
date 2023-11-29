import pygame
import math
from settings import Settings

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitCount = 0

        self.settings = Settings()

        self.image = pygame.image.load('SpriteImages/Projectiles/bullet1.bmp')
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        width = mouse_x - (self.x + (self.image.get_width() / 2))
        height = mouse_y - (self.y + (self.image.get_height() / 2))

        if height != 0:
            angle = math.atan2(width, height)
            angle = math.degrees(angle)
            angle = angle - 90
        else:
            angle = 0

        self.image = pygame.transform.rotate(self.image, angle)

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

    def updatePos(self):
        self.x += self.xVelocity
        self.y += self.yVelocity