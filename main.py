import pygame
import math
import json
from settings import Settings
from blueTank import BlueTank
from brownTank import BrownTank
from greenTank import GreenTank
from bullet import Bullet
from brownBullet import BrownBullet
from blueBullet import BlueBullet
from fireBullet import FireBullet
from bomb import Bomb
from block import Block

class TanksGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.screenSize)
        pygame.display.set_caption("Tanks")
        pygame.mouse.set_visible(False)

        self.background = pygame.image.load('mapImages/concreteBackground.png')

        self.levels = ['level1.json', 'level2.json']

        self.blocks = []
        self.destroyBlocks = []

        self.player = 0

        self.enemies = []

        self.bullets = []

        self.bombs = []

        self.gameRunning = True
        self.levelRunning = True

    def runGame(self):
        level = 0

        while self.gameRunning:

            self.blocks = []
            self.player = 0
            self.enemies = []
            self.bullets = []

            level = level % 2 ## retained under max level limit

            self.levelRunning = True
            self.loadLevel(level)

            while self.levelRunning and len(self.enemies) > 0:
                pygame.time.delay(25)

                keys = pygame.key.get_pressed()

                # Move player tank
                self.movePlayer(keys)
            
                # Shoot bullets
                if self.player.shoot():
                    self.bullets.append(BlueBullet(self.player.x + self.player.width, self.player.y + self.player.height))

                # Place bombs
                if self.player.plantBomb(keys):
                    self.bombs.append(Bomb(self.player.x + self.player.width, self.player.y + self.player.height))

                # Update enemies
                for enemy in self.enemies:
                    if enemy.shoot(self.player.x + self.player.width, self.player.y + self.player.height):
                        match enemy.color:
                            case 'brown':
                                self.bullets.append(BrownBullet(enemy.x + enemy.width, enemy.y + enemy.height, self.player.x + self.player.width / 2, self.player.y + self.player.height / 2))
                            case 'green':
                                self.bullets.append(FireBullet(enemy.x + enemy.width, enemy.y + enemy.height, self.player.x + self.player.width / 2, self.player.y + self.player.height / 2))
                    if enemy.checkHit(self.bullets):
                        self.enemies.remove(enemy)


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameRunning = False
                        self.levelRunning = False
                        break
                if not self.levelRunning:
                    break

                # Update / Remove Bullets
                self.updateBullets()

                # Update / Explode Bombs
                self.updateBombs()

                # Check if player hit
                self.levelRunning = not self.player.checkHit(self.bullets)
    
                self.displayScreen()

            if not self.player.hit:
                level += 1
            else:
                level = 0
            
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

        # display bombs
        for bomb in self.bombs:
            self.screen.blit(bomb.image, (bomb.x, bomb.y))

        # display enemies
        for enemy in self.enemies:
            enemy.display(self.screen, self.player.x + self.player.width, self.player.y + self.player.height)

        # display all player tank items
        self.player.display(self.screen)

        # update display
        pygame.display.update()

    def loadLevel(self, i):
        with open(self.levels[i]) as levels_file:
            data = json.load(levels_file)
            for block in data['permanentBlocks']:
                self.blocks.append(Block(block['coordinates'][0], block['coordinates'][1], block['texture']))

            for block in data['destroyableBlocks']:
                self.blocks.append(Block(block['coordinates'][0], block['coordinates'][1], block['texture']))
                self.destroyBlocks.append(Block(block['coordinates'][0], block['coordinates'][1], block['texture']))

            for enemy in data['enemies']:
                match enemy['color']:
                    case 'brown':
                        self.enemies.append(BrownTank(enemy['coordinates'][0], enemy['coordinates'][1], self.blocks))
                    case 'green':
                        self.enemies.append(GreenTank(enemy['coordinates'][0], enemy['coordinates'][1], self.blocks))

            player = data['player']
            self.player = BlueTank(player['coordinates'][0], player['coordinates'][1], self.blocks)

    def movePlayer(self, keys):
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

    def updateBullets(self):
        for bullet in self.bullets:
            bullet.updatePos(self.blocks)
            if bullet.bounceCount > bullet.bounceMax:
                if bullet.type == "player":
                    self.player.bulletCount -= 1
                self.bullets.remove(bullet)

    def updateBombs(self):
        for bomb in self.bombs:
            bomb.update()
            if bomb.explodeCount >= bomb.explodeMax:
                self.bombs.remove(bomb)
                self.player.bombCount -= 1

if __name__ == '__main__':
    game = TanksGame()
    game.runGame()
