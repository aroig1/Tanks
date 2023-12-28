import pygame
import math
import random
from movingEnemyTank import MovingEnemyTank
from settings import Settings
from brownBullet import BrownBullet
from block import Block

class RedTank(MovingEnemyTank):
    def __init__(self, x, y, blocks):
        super().__init__(x, y, blocks)

        self.color = 'red'

        self.bulletTimer = random.randint(50,74)
        self.bulletTimerMax = 75

        self.images = [pygame.image.load('SpriteImages/RedTank/RedTank.bmp'), pygame.image.load('SpriteImages/RedTank/RedTank2.bmp')]
        self.image = self.images[0]
        self.turret = pygame.image.load('SpriteImages/RedTank/RedTurret.bmp')

        self.turretX = self.x + (self.image.get_width() / 2) - (self.turret.get_width() / 2)
        self.turretY = self.y + (self.image.get_height() / 2) - 80

        self.width = (self.image.get_width() / 2)
        self.height = (self.image.get_height() / 2)