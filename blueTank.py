import pygame
import math
from settings import Settings
from bullet import Bullet
from bomb import Bomb

class BlueTank:
    def __init__(self, x=200, y=300):

        self.x = x
        self.y = y

        self.bullets = []
        self.bulletCount = 0

        self.bombs = []
        self.bombCount = 0

        self.settings = Settings()

        self.sprites = [pygame.image.load('SpriteImages/BlueTank/BlueTank1.bmp'), pygame.image.load('SpriteImages/BlueTank/BlueTank2.bmp'),
                        pygame.image.load('SpriteImages/BlueTank/BlueTank3.bmp'), pygame.image.load('SpriteImages/BlueTank/BlueTank4.bmp')]
        self.image = self.sprites[0]

        self.turret = pygame.image.load('SpriteImages/BlueTank/BlueTurret2.bmp')
        self.turretX = self.x + (self.image.get_width() / 2) - (self.turret.get_width() / 2)
        self.turretY = self.y + (self.image.get_height() / 2) - 80

        self.width = (self.image.get_width() / 2)
        self.height = (self.image.get_height() / 2)


    def getTurret(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        width = mouse_x - (self.x + (self.image.get_width() / 2))
        height = mouse_y - (self.y + (self.image.get_height() / 2))

        if height != 0:
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
        
        else:
            return self.turret, self.turret.get_rect()
        

    def move(self, x, y):
        self.x += x
        self.y += y
        self.turretX = self.x + (self.image.get_width() / 2) - (self.turret.get_width() / 2)
        self.turretY = self.y + (self.image.get_height() / 2) - 80

    def shoot(self):
        if pygame.mouse.get_pressed()[0] and self.bulletCount <= self.settings.maxBullets:
            self.bullets.append(Bullet(self.x + self.width, self.y + self.height))
            self.bulletCount += 1

    def plantBomb(self, keys):
        if keys[pygame.K_SPACE] and self.bombCount <= self.settings.maxBombs:
            self.bombs.append(Bomb(self.x + self.width, self.y + self.height))
            self.bombCount += 1

    def updateBullets(self):
        for i in range(len(self.bullets)):
            try:
                self.bullets[i].updatePos()
                if self.bullets[i].bounceCount > self.bullets[i].bounceMax:
                    self.bullets.pop(i)
                    self.bulletCount -= 1
                    i -= 1
            except:
                continue

    def updateBombs(self):
        for i in range(len(self.bombs)):
            try:
                self.bombs[i].update()
                if self.bombs[i].explodeCount >= self.bombs[i].explodeMax:
                    self.bombs.pop(i)
                    self.bombCount -= 1
                    i -= 1
            except:
                continue

    def display(self, screen):
        # display bombs
        for bomb in self.bombs:
            screen.blit(bomb.image, (bomb.x, bomb.y))
        # display tank base
        screen.blit(self.image, (self.x, self.y))
        # display bullets
        for bullet in self.bullets:
            screen.blit(bullet.image, (bullet.x, bullet.y))
        # display tank turret
        turret_img, turret_rect = self.getTurret()
        screen.blit(turret_img, turret_rect.topleft)