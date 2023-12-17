import pygame
import math
from tank import Tank
from settings import Settings
from blueBullet import BlueBullet
from bomb import Bomb

class BlueTank(Tank):
    def __init__(self, x, y, blocks):
        super().__init__(x, y, blocks)

        self.bulletCount = 0

        self.bombCount = 0

        self.sprites = [pygame.image.load('SpriteImages/BlueTank/BlueTank1.bmp'), pygame.image.load('SpriteImages/BlueTank/BlueTank2.bmp'),
                        pygame.image.load('SpriteImages/BlueTank/BlueTank3.bmp'), pygame.image.load('SpriteImages/BlueTank/BlueTank4.bmp')]
        self.image = self.sprites[0]

        self.turret = pygame.image.load('SpriteImages/BlueTank/BlueTurret2.bmp')
        self.turretX = self.x + (self.image.get_width() / 2) - (self.turret.get_width() / 2)
        self.turretY = self.y + (self.image.get_height() / 2) - 80

        self.crosshair = pygame.image.load('SpriteImages/BlueTank/crosshair.bmp')
        self.aimDot = pygame.image.load('SpriteImages/BlueTank/aimDot.bmp')
        self.crosshairSize = self.crosshair.get_width()

        self.width = (self.image.get_width() / 2)
        self.height = (self.image.get_height() / 2)


    def getTurret(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        width = mouse_x - (self.x + (self.image.get_width() / 2))
        height = mouse_y - (self.y + (self.image.get_height() / 2))

        if height == 0:
            height = 1
            
        angle = math.atan2(width, height)
        angle = math.degrees(angle)
        angle += 180

        # print(f'width: {width} \t height: {height} \t angle: {angle}')
        # print(f'mouse x: {mouse_x} \t mouse y: {mouse_y}')
        # print(f'tank x: {self.x} \t tank y: {self.y}')
        # print(self.image.get_height())
        
        # Rotate turret
        rotatedTurret = pygame.transform.rotate(self.turret, angle)

        # Adjust the position of the rotated turret
        turret_rect = rotatedTurret.get_rect()
        center_x = self.x + (self.image.get_width() / 2)
        center_y = self.y + (self.image.get_height() / 2)

        # Calculate the new top left position based on the anchor point
        turret_rect.center = (center_x, center_y)

        return rotatedTurret, turret_rect

        
    def move(self, x, y):
        self.x += x
        self.y += y
        self.turretX = self.x + (self.image.get_width() / 2) - (self.turret.get_width() / 2)
        self.turretY = self.y + (self.image.get_height() / 2) - 80
        if self.x <= 20:
            self.x = 20
        if self.x >= self.settings.screenSize[0] - self.image.get_width() - 25:
            self.x = self.settings.screenSize[0] - self.image.get_width() - 25
        if self.y <= 30:
            self.y = 30
        if self.y >= self.settings.screenSize[1] - self.image.get_height() - 25:
            self.y = self.settings.screenSize[1] - self.image.get_height() - 25
        for block in self.blocks:
            if (block.x <= self.x + self.image.get_width() <= block.x + (block.size / 2)) and ((block.y < self.y < block.y + block.size) or (block.y < self.y + self.image.get_height() < block.y + block.size)): # Left border bounce
                self.x = block.x - self.image.get_width() - 1
                return
            elif (block.x + (block.size / 2) <= self.x <= block.x + block.size) and ((block.y < self.y < block.y + block.size) or (block.y < self.y + self.image.get_height() < block.y + block.size)): # Right border bounce
                self.x = block.x + block.size + 1
                return
            elif (block.y <= self.y + self.image.get_height() <= block.y + (block.size / 2)) and ((block.x < self.x < block.x + block.size) or (block.x < self.x + self.image.get_width() < block.x + block.size)): # Top border bounce
                self.y = block.y - self.image.get_height() - 1
                return
            elif (block.y + (block.size / 2) <= self.y <= block.y + block.size) and ((block.x < self.x < block.x + block.size) or (block.x < self.x + self.image.get_width() < block.x + block.size)): # Bottom border bounce
                self.y = block.y + block.size + 1
                return
        

    def shoot(self):
        if pygame.mouse.get_pressed()[0] and self.bulletCount <= self.settings.maxBullets:
            self.bulletCount += 1
            return True
        return False

    def plantBomb(self, keys):
        if keys[pygame.K_SPACE] and self.bombCount <= self.settings.maxBombs:
            self.bombCount += 1
            return True
        return False

    def display(self, screen):
        # Display Crosshair
        self.displayCrosshair(screen)
        # display bullets
        for bullet in self.bullets:
            screen.blit(bullet.image, (bullet.x, bullet.y))
        # display tank base
        screen.blit(self.image, (self.x, self.y))
        # display tank turret
        turret_img, turret_rect = self.getTurret()
        screen.blit(turret_img, turret_rect.topleft)

    def displayCrosshair(self, screen):
        x, y = pygame.mouse.get_pos()
        x = x - self.crosshairSize / 2
        y =  y - self.crosshairSize / 2

        screen.blit(self.crosshair, (x, y))

        for i in range(1, 8):
            tempX = ((x - self.x) / 8) * i  + self.crosshairSize / 2 + self.x
            tempY = ((y - self.y) / 8) * i  + self.crosshairSize / 2 + self.y
            screen.blit(self.aimDot, (tempX, tempY))