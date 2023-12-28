import pygame
import math
import random
from movingEnemyTank import MovingEnemyTank
from settings import Settings
from brownBullet import BrownBullet
from block import Block

class PurpleTank(MovingEnemyTank):
    def __init__(self, x, y, blocks):
        super().__init__(x, y, blocks)

        self.color = 'purple'

        self.bulletTimer = random.randint(80, 99)
        self.bulletTimerMax = 100

        self.images = [pygame.image.load('SpriteImages/PurpleTank/PurpleTank.bmp'), pygame.image.load('SpriteImages/PurpleTank/PurpleTank2.bmp')]
        self.image = self.images[0]
        self.turret = pygame.image.load('SpriteImages/PurpleTank/PurpleTurret.bmp')

        self.turretX = self.x + (self.image.get_width() / 2) - (self.turret.get_width() / 2)
        self.turretY = self.y + (self.image.get_height() / 2) - 80

        self.width = (self.image.get_width() / 2)
        self.height = (self.image.get_height() / 2)