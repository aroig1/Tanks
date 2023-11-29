import pygame
from settings import Settings

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.countdown = 50
        self.color = 0

        self.images = [pygame.image.load('SpriteImages/Projectiles/bombYellow.bmp'), pygame.image.load('SpriteImages/Projectiles/bombRed.bmp')]
        self.image = self.images[0]

        self.explodeImages = [pygame.image.load('SpriteImages/Projectiles/explosion1.png'), pygame.image.load('SpriteImages/Projectiles/explosion2.png'),
                           pygame.image.load('SpriteImages/Projectiles/explosion3.png'), pygame.image.load('SpriteImages/Projectiles/explosion4.png'),
                           pygame.image.load('SpriteImages/Projectiles/explosion5.png'), pygame.image.load('SpriteImages/Projectiles/explosion6.png'),
                           pygame.image.load('SpriteImages/Projectiles/explosion7.png'), pygame.image.load('SpriteImages/Projectiles/explosion8.png')]
        self.explodeCount = 0
        self.explodeMax = 8

        self.settings = Settings()

    def update(self):
        self.timer += 1
        if self.countdown == 0 and self.explodeCount < self.explodeMax:
            self.image = self.explodeImages[self.explodeCount]
            self.x -= 10
            self.y -= 5
            self.explodeCount += 1
        elif self.timer == 5 and self.color % 2 == 1:
            self.color += 1
            self.image = self.images[self.color % 2]
            self.timer = 0
        elif self.timer == self.countdown and self.countdown <= 10:
            self.color += 1
            self.image = self.images[self.color % 2]
            self.timer = 0
            self.countdown -= 1
        elif self.timer == self.countdown:
            self.color += 1
            self.image = self.images[self.color % 2]
            self.timer = 0
            self.countdown -= 10

