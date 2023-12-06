import pygame
import math
from settings import Settings
from bullet import Bullet
from bomb import Bomb

class BlueTank:
    def __init__(self, x, y, blocks):

        self.x = x
        self.y = y

        self.bullets = []
        self.bulletCount = 0

        self.bombs = []
        self.bombCount = 0

        self.hit = False

        self.explodeImages = [pygame.image.load('SpriteImages/Projectiles/explosion1.png'), pygame.image.load('SpriteImages/Projectiles/explosion2.png'),
                           pygame.image.load('SpriteImages/Projectiles/explosion3.png'), pygame.image.load('SpriteImages/Projectiles/explosion4.png'),
                           pygame.image.load('SpriteImages/Projectiles/explosion5.png'), pygame.image.load('SpriteImages/Projectiles/explosion6.png'),
                           pygame.image.load('SpriteImages/Projectiles/explosion7.png'), pygame.image.load('SpriteImages/Projectiles/explosion8.png')]
        self.explodeCount = 0
        self.explodeMax = 8

        self.blocks = blocks

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
        if self.x <= 0:
            self.x = 0
        elif self.x >= self.settings.screenSize[0] - self.image.get_width():
            self.x = self.settings.screenSize[0] - self.image.get_width()
        elif self.y <= 0:
            self.y = 0
        elif self.y >= self.settings.screenSize[1] - self.image.get_height():
            self.y = self.settings.screenSize[1] - self.image.get_height()
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
            self.bullets.append(Bullet(self.x + self.width, self.y + self.height))
            self.bulletCount += 1

    def plantBomb(self, keys):
        if keys[pygame.K_SPACE] and self.bombCount <= self.settings.maxBombs:
            self.bombs.append(Bomb(self.x + self.width, self.y + self.height))
            self.bombCount += 1

    def updateBullets(self):
        for i in range(len(self.bullets)):
            try:
                self.bullets[i].updatePos(self.blocks)
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

    def checkHit(self, enemies):
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
        
        for bullet in self.bullets:
            if (self.x < bullet.x < self.x + self.image.get_width()) and (self.y < bullet.y < self.y + self.image.get_height()):
                self.hit = True
                return False
        for enemy in enemies:
            for bullet in enemy.bullets:
                if (self.x < bullet.x < self.x + self.image.get_width()) and (self.y < bullet.y < self.y + self.image.get_height()):
                    self.hit = True
                    return False
        return False

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