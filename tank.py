import pygame
from settings import Settings

class Tank:
    def __init__(self, x, y, blocks):
        self.x = x
        self.y = y

        self.bullets = []

        self.hit = False

        self.blocks = blocks

        self.settings = Settings()

        self.explodeImages = [pygame.image.load('SpriteImages/Projectiles/explosion1.png'), pygame.image.load('SpriteImages/Projectiles/explosion2.png'),
                           pygame.image.load('SpriteImages/Projectiles/explosion3.png'), pygame.image.load('SpriteImages/Projectiles/explosion4.png'),
                           pygame.image.load('SpriteImages/Projectiles/explosion5.png'), pygame.image.load('SpriteImages/Projectiles/explosion6.png'),
                           pygame.image.load('SpriteImages/Projectiles/explosion7.png'), pygame.image.load('SpriteImages/Projectiles/explosion8.png')]
        self.explodeCount = 0
        self.explodeMax = 8

    def checkHit(self, bullets, bombs):
        if self.hit and self.explodeCount == self.explodeMax:
            return True
        # Explosion animation
        elif self.hit and self.explodeCount < self.explodeMax:
            self.image = self.explodeImages[self.explodeCount]
            self.turret = self.explodeImages[self.explodeCount]
            self.x -= 10
            self.y -= 5
            self.explodeCount += 1
            return False
        
        for bullet in bullets:
            if (self.x < bullet.x < self.x + self.image.get_width()) and (self.x < bullet.x + bullet.image.get_width() < self.x + self.image.get_width()):
                if self.y < bullet.y < self.y + self.image.get_height() or self.y < bullet.y + bullet.image.get_height() < self.y + self.image.get_height():
                    self.hit = True
                    bullets.remove(bullet)
                    return False
                
        for bomb in bombs:
            if bomb.countdown == 0:
                if (self.x < bomb.x < self.x + self.image.get_width()) and (self.x < bomb.x + bomb.image.get_width() < self.x + self.image.get_width()):
                    if self.y < bomb.y < self.y + self.image.get_height() or self.y < bomb.y + bomb.image.get_height() < self.y + self.image.get_height():
                        self.hit = True
                        return False
            
        return False