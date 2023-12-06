import pygame
import math
import json
from settings import Settings
from blueTank import BlueTank
from brownTank import BrownTank
#from bullet import Bullet
from brownBullet import BrownBullet
from blueBullet import BlueBullet
from bomb import Bomb
from block import Block

class TanksGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.screenSize)
        pygame.display.set_caption("Tanks")
        self.background = pygame.image.load('mapImages/woodbackground.png')

        self.blocks = []

        self.player = 0

        self.enemies = []

        self.bullets = []

        self.gameRunning = True
        self.levelRunning = True

    def runGame(self):
        while self.gameRunning:

            self.blocks = []
            self.player = 0
            self.enemies = []
            self.bullets = []

            self.levelRunning = True
            self.loadLevel()

            while self.levelRunning and len(self.enemies) > 0:
                pygame.time.delay(5)

                keys = pygame.key.get_pressed()

                ## Movement
                if keys[pygame.K_w] and keys[pygame.K_d]:
                    self.player.image = self.player.sprites[1]
                    self.player.move(math.sqrt(self.settings.tankSpeed**2 / 2), -1 * math.sqrt(self.settings.tankSpeed**2 / 2))
                elif keys[pygame.K_d] and keys[pygame.K_s]:
                    self.player.image = self.player.sprites[3]
                    self.player.move(math.sqrt(self.settings.tankSpeed**2 / 2), math.sqrt(self.settings.tankSpeed**2 / 2))
                elif keys[pygame.K_s] and keys[pygame.K_a]:
                    self.player.image = self.player.sprites[1]
                    self.player.move(-1 * math.sqrt(self.settings.tankSpeed**2 / 2), math.sqrt(self.settings.tankSpeed**2 / 2))
                elif keys[pygame.K_a] and keys[pygame.K_w]:
                    self.player.image = self.player.sprites[3]
                    self.player.move(-1 * math.sqrt(self.settings.tankSpeed**2 / 2), -1 * math.sqrt(self.settings.tankSpeed**2 / 2))
                elif keys[pygame.K_w]:
                    self.player.image = self.player.sprites[0]
                    self.player.move(0, -1 * self.settings.tankSpeed)
                elif keys[pygame.K_d]:
                    self.player.image = self.player.sprites[2]
                    self.player.move(self.settings.tankSpeed, 0)
                elif keys[pygame.K_s]:
                    self.player.image = self.player.sprites[0]
                    self.player.move(0, self.settings.tankSpeed)
                elif keys[pygame.K_a]:
                    self.player.image = self.player.sprites[2]
                    self.player.move(-1 * self.settings.tankSpeed, 0)

            
                # Shoot bullets
                if self.player.shoot():
                    self.bullets.append(BlueBullet(self.player.x + self.player.width, self.player.y + self.player.height))

                # Place bombs
                self.player.plantBomb(keys)

                # Update enemies
                for i in range(len(self.enemies)):
                    try:
                        if self.enemies[i].shoot(self.player.x + self.player.width, self.player.y + self.player.height):
                            self.bullets.append(BrownBullet(self.enemies[i].x + self.enemies[i].width, self.enemies[i].y + self.enemies[i].height, self.player.x, self.player.y))
                        if self.enemies[i].checkHit(self.bullets):
                            self.enemies.pop(i)
                            i -= 1
                    except:
                        continue


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameRunning = False
                        self.levelRunning = False
                        break

                # Update / Remove Bullets
                self.updateBullets()

                # Update / Explode Bombs
                self.player.updateBombs()

                # Check if player hit
                self.levelRunning = not self.player.checkHit(self.bullets)
    
                self.displayScreen()
            
        pygame.quit()

    def displayScreen(self):
        # display background
        self.screen.blit(self.background, (0, 0))

        # display blocks
        for block in self.blocks:
            block.display(self.screen)

        # display bullets
        for bullet in self.bullets:
            self.screen.blit(bullet.image, (bullet.x, bullet.y))

        # display all player tank items
        self.player.display(self.screen)

        # display enemies
        for enemy in self.enemies:
            enemy.display(self.screen, self.player.x + self.player.width, self.player.y + self.player.height)

        # update display
        pygame.display.update()

    def loadLevel(self):
        with open('level1.json') as levels_file:
            data = json.load(levels_file)
            for block in data['permanentBlocks']:
                self.blocks.append(Block(block['coordinates'][0], block['coordinates'][1], block['texture']))

            for enemy in data['enemies']:
                self.enemies.append(BrownTank(enemy['coordinates'][0], enemy['coordinates'][1], self.blocks))

            player = data['player']
            self.player = BlueTank(player['coordinates'][0], player['coordinates'][1], self.blocks)

    def updateBullets(self):
        for i in range(len(self.bullets)):
            try:
                self.bullets[i].updatePos(self.blocks)
                if self.bullets[i].bounceCount > self.bullets[i].bounceMax:
                    self.bullets.pop(i)
                    i -= 1
                    if self.bullets[i].type == "player":
                        self.player.bulletCount -= 1
            except:
                continue

if __name__ == '__main__':
    game = TanksGame()
    game.runGame()
