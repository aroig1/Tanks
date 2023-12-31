import pygame
import math
from tank import Tank
from settings import Settings
from block import Block

class StillEnemyTank(Tank):
    def __init__(self, x, y, blocks):
        super().__init__(x, y, blocks)

        # Defined further is subclass
        self.bulletTimer = 0
        self.bulletTimerMax = 75
        self.image = 0
        self.turret = 0
        self.turretX = 0
        self.turretY = 0
        self.width = 0
        self.height = 0

    def getTurret(self, player_x, player_y):

        width = player_x - (self.x + (self.image.get_width() / 2))
        height = player_y - (self.y + (self.image.get_height() / 2))

        if height == 0:
            height = 1

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
    
    
    def shoot(self, player_x, player_y):
        self.bulletTimer += 1
        if self.bulletTimer == self.bulletTimerMax:
            self.bulletTimer = 0
            return True
        return False
    
    def move(self, player_x, player_y, matrix):
        return

    def display(self, screen, player_x, player_y):
        # display enemy tank base
        screen.blit(self.image, (self.x, self.y))
        # displat enemy tank turret
        turret_img, turret_rect = self.getTurret(player_x, player_y)
        screen.blit(turret_img, turret_rect.topleft)