import pygame
import math
from settings import Settings
from block import Block

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bounceCount = 0
        self.bounceMax = 1

        self.settings = Settings()

        self.originalImage = pygame.image.load('SpriteImages/Projectiles/bullet1.bmp')
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

    def rotateImage(self, width, height):
        if height != 0:
            angle = math.atan2(width, height)
            angle = math.degrees(angle)
            angle = angle - 90
        else:
            angle = 0

        self.image = pygame.transform.rotate(self.originalImage, angle)
        return angle

    def updatePos(self, blocks):
        self.x += self.xVelocity
        self.y += self.yVelocity
        if self.x <= 0 or self.x + 10 >= self.settings.screenSize[0]:
            self.xVelocity *= -1
            self.rotateImage(self.xVelocity, self.yVelocity)
            self.bounceCount += 1
        elif self.y <= 0 or self.y + 10 >= self.settings.screenSize[1]:
            self.yVelocity *= -1
            self.rotateImage(self.xVelocity, self.yVelocity)
            self.bounceCount += 1
        for block in blocks:
            if (abs(self.x - block.x + 10) <= self.settings.bulletSpeed) and (block.y < self.y < block.y + block.size): # Left border bounce
                self.xVelocity *= -1
                self.rotateImage(self.xVelocity, self.yVelocity)
                self.bounceCount += 1
            elif (abs((block.x + block.size) - self.x) <= self.settings.bulletSpeed) and (block.y < self.y < block.y + block.size): # Right border bounce
                self.xVelocity *= -1
                self.rotateImage(self.xVelocity, self.yVelocity)
                self.bounceCount += 1
            elif (abs(self.y - block.y + 10) <= self.settings.bulletSpeed) and (block.x < self.x < block.x + block.size): # Top border bounce
                self.yVelocity *= -1
                self.rotateImage(self.xVelocity, self.yVelocity)
                self.bounceCount += 1
            elif (abs((block.y + block.size) - self.y) <= self.settings.bulletSpeed) and (block.x < self.x < block.x + block.size): # Bottom border bounce
                self.yVelocity *= -1
                self.rotateImage(self.xVelocity, self.yVelocity)
                self.bounceCount += 1

