import pygame
import math
from settings import Settings
from block import Block

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bounceCount = 0

        self.settings = Settings()

        # Defined better in subclasses
        self.originalImage = 0
        self.xVelocity = 0
        self.yVelocity = 0


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
        if self.x <= 30 or self.x + self.image.get_width() >= self.settings.screenSize[0] - 30:
            self.xVelocity *= -1
            self.rotateImage(self.xVelocity, self.yVelocity)
            self.bounceCount += 1
        elif self.y <= 35 or self.y + self.image.get_height() >= self.settings.screenSize[1] - 30:
            self.yVelocity *= -1
            self.rotateImage(self.xVelocity, self.yVelocity)
            self.bounceCount += 1
        for block in blocks:
            if block.type != 'hole':
                if (abs(self.x - block.x + self.image.get_width()) <= self.settings.bulletSpeed) and (block.y < self.y < block.y + block.size): # Left border bounce
                    self.xVelocity *= -1
                    self.rotateImage(self.xVelocity, self.yVelocity)
                    self.bounceCount += 1
                elif (abs((block.x + block.size) - self.x) <= self.settings.bulletSpeed) and (block.y < self.y < block.y + block.size): # Right border bounce
                    self.xVelocity *= -1
                    self.rotateImage(self.xVelocity, self.yVelocity)
                    self.bounceCount += 1
                elif (abs(self.y - block.y + self.image.get_height()) <= self.settings.bulletSpeed) and (block.x < self.x < block.x + block.size): # Top border bounce
                    self.yVelocity *= -1
                    self.rotateImage(self.xVelocity, self.yVelocity)
                    self.bounceCount += 1
                elif (abs((block.y + block.size) - self.y) <= self.settings.bulletSpeed) and (block.x < self.x < block.x + block.size): # Bottom border bounce
                    self.yVelocity *= -1
                    self.rotateImage(self.xVelocity, self.yVelocity)
                    self.bounceCount += 1
                elif block.x < self.x < block.x + block.size or block.x < self.x + self.image.get_width() < block.x + block.size:
                    if block.y < self.y < block.y + block.size or block.y < self.y + self.image.get_height() < block.y + block.size:
                        self.bounceCount += 1

