import pygame
import math
from tank import Tank
from settings import Settings
from block import Block
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class MovingEnemyTank(Tank):
    def __init__(self, x, y, blocks):
        super().__init__(x, y, blocks)

        self.moveTimer = 0
        self.moveTimerMax = 200
        self.moveStep = 0
        self.path = []
        self.speed = 1

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
        if self.moveTimer <= 0:
            grid = Grid(matrix = matrix)

            start = grid.node(self.x // 75, self.y // 75)
            end = grid.node(int(player_x) // 75, int(player_y) // 75)

            finder = AStarFinder()

            self.path, runs = finder.find_path(start, end, grid)

            self.moveTimer = self.moveTimerMax
            self.moveStep = 0

            print("NEW PATH")

            grid.cleanup()

        if self.x < self.path[self.moveStep].x * 75:
            self.x += self.speed
        elif self.x > self.path[self.moveStep].x * 75:
            self.x -= self.speed
        elif self.y < self.path[self.moveStep].y * 75:
            self.y += self.speed
        elif self.y > self.path[self.moveStep].y * 75:
            self.y -= self.speed
        else:
            self.moveStep += 1

        print(f'{self.moveStep}: ({self.path[2].x}, {self.path[2].y})')

        self.moveTimer -= 1
        

    def display(self, screen, player_x, player_y):
        # display enemy tank base
        screen.blit(self.image, (self.x, self.y))
        # displat enemy tank turret
        turret_img, turret_rect = self.getTurret(player_x, player_y)
        screen.blit(turret_img, turret_rect.topleft)