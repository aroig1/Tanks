import pygame
import math
from tank import Tank
from settings import Settings
from brownBullet import BrownBullet
from block import Block

class BrownTank(Tank):
    def __init__(self, x, y, blocks):
        super().__init__(x, y, blocks)

        self.bulletTimer = 0

        self.image = pygame.image.load('SpriteImages/BrownTank/BrownTank.bmp')
        self.turret = pygame.image.load('SpriteImages/BrownTank/BrownTurret.bmp')

        self.turretX = self.x + (self.image.get_width() / 2) - (self.turret.get_width() / 2)
        self.turretY = self.y + (self.image.get_height() / 2) - 80

        self.width = (self.image.get_width() / 2)
        self.height = (self.image.get_height() / 2)

    def getTurret(self, player_x, player_y):

        width = player_x - (self.x + (self.image.get_width() / 2))
        height = player_y - (self.y + (self.image.get_height() / 2))

        if height != 0:
            angle = math.atan2(width, height)
            angle = math.degrees(angle)
            angle += 180
            
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
        
    
    def shoot(self, player_x, player_y):
        self.bulletTimer += 1
        if self.bulletTimer == 75:
            self.bulletTimer = 0
            return True
        return False

    def checkHit(self, bullets):
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
            if (self.x < bullet.x < self.x + self.image.get_width()) and (self.y < bullet.y < self.y + self.image.get_height()):
                self.hit = True
                return False
            
        return False

    def display(self, screen, player_x, player_y):
        # display enemy tank base
        screen.blit(self.image, (self.x, self.y))
        # displat enemy tank turret
        turret_img, turret_rect = self.getTurret(player_x, player_y)
        screen.blit(turret_img, turret_rect.topleft)