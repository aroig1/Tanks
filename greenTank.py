import pygame
import math
import random
from stillEnemyTank import StillEnemyTank
from settings import Settings
from brownBullet import BrownBullet
from block import Block

class GreenTank(StillEnemyTank):
    def __init__(self, x, y, blocks):
        super().__init__(x, y, blocks)

        self.color = 'green'

        self.bulletTimer = random.randint(80, 99)
        self.bulletTimerMax = 100

        self.image = pygame.image.load('SpriteImages/GreenTank/GreenTank.bmp')
        self.turret = pygame.image.load('SpriteImages/GreenTank/GreenTurret.bmp')

        self.turretX = self.x + (self.image.get_width() / 2) - (self.turret.get_width() / 2)
        self.turretY = self.y + (self.image.get_height() / 2) - 80

        self.width = (self.image.get_width() / 2)
        self.height = (self.image.get_height() / 2)