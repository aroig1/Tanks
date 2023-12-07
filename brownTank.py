import pygame
import math
from stillEnemyTank import StillEnemyTank
from settings import Settings
from brownBullet import BrownBullet
from block import Block

class BrownTank(StillEnemyTank):
    def __init__(self, x, y, blocks):
        super().__init__(x, y, blocks)

        self.bulletTimer = 0
        self.bulletTimerMax = 75

        self.image = pygame.image.load('SpriteImages/BrownTank/BrownTank.bmp')
        self.turret = pygame.image.load('SpriteImages/BrownTank/BrownTurret.bmp')

        self.turretX = self.x + (self.image.get_width() / 2) - (self.turret.get_width() / 2)
        self.turretY = self.y + (self.image.get_height() / 2) - 80

        self.width = (self.image.get_width() / 2)
        self.height = (self.image.get_height() / 2)