import pygame
from pygame import mixer
import math
import json
from settings import Settings
from blueTank import BlueTank
from brownTank import BrownTank
from greenTank import GreenTank
from redTank import RedTank
from purpleTank import PurpleTank
from yellowTank import YellowTank
from bullet import Bullet
from brownBullet import BrownBullet
from blueBullet import BlueBullet
from fireBullet import FireBullet
from bomb import Bomb
from block import Block

class TanksGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.screenSize)
        pygame.display.set_caption("Tanks")
        # pygame.mouse.set_visible(False)

        self.background = pygame.image.load('mapImages/woodBackground.png')
        self.missionTitleBackground = pygame.image.load('mapImages/missionTitleScreen.png')
        self.missionCompleteImage = pygame.image.load('mapImages/missionComplete.PNG')
        self.startImage = pygame.image.load('mapImages/start.png')
        self.scoreImage = pygame.image.load('mapImages/scoreCounter.png')
        self.resultsImage = pygame.image.load('mapImages/results.png')

        self.musicChannel = mixer.Channel(1)
        self.moveChannel = mixer.Channel(2)
        self.effectsChannel = mixer.Channel(3)

        self.startLevelSound = mixer.Sound('sounds/roundStart.wav')
        self.backgroundMusic = mixer.Sound('sounds/backgroundMusic.wav')
        self.missionCompleteSound = mixer.Sound('sounds/roundEnd.wav')
        self.missionFailedSound = mixer.Sound('sounds/roundFailure.wav')
        self.resultsSound = mixer.Sound('sounds/results.wav')
        self.shootSound = mixer.Sound('sounds/shootBullet.wav')
        self.bulletBounceSound = mixer.Sound('sounds/bounce.wav')
        self.bombSound = mixer.Sound('sounds/plantBomb.wav')
        self.moveSound = mixer.Sound('sounds/tankMoving.wav')
        self.moveSound.set_volume(0.05)

        self.levels = ['levels/level1.json', 'levels/level2.json', 'levels/level3.json',
                        'levels/level4.json', 'levels/level5.json', 'levels/level6.json',
                        'levels/level7.json', 'levels/level8.json', 'levels/level9.json']

        self.blocks = []
        self.destroyBlocks = []
        self.matrix = []

        self.player = 0
        self.score = 0
        self.tankKills = {'brown' : 0, 'green' : 0, 'red' : 0, 'purple' : 0, 'yellow' : 0}

        self.enemies = []

        self.bullets = []

        self.bombs = []

        self.gameRunning = True
        self.levelRunning = True

    def runGame(self):
        level = 0
        maxLevel = 9

        while self.gameRunning:

            self.blocks = []
            self.player = 0
            self.enemies = []
            self.bullets = []
            self.bombs = []

            level = level % maxLevel

            self.missionTitleScreen(level)

            self.levelRunning = True
            if self.gameRunning:
                self.loadLevel(level)

            while self.gameRunning and self.levelRunning and len(self.enemies) > 0:
                pygame.time.delay(5)

                keys = pygame.key.get_pressed()

                # Move player tank
                self.movePlayer(keys)
            
                # Shoot bullets
                if self.player.shoot():
                    self.bullets.append(BlueBullet(self.player.x + self.player.width, self.player.y + self.player.height))
                    self.effectsChannel.play(self.shootSound)

                # Place bombs
                if self.player.plantBomb(keys):
                    self.bombs.append(Bomb(self.player.x + self.player.width / 2, self.player.y + self.player.height / 2))
                    self.effectsChannel.play(self.bombSound)

                # Update enemies
                for enemy in self.enemies:
                    enemy.move(self.player.x + self.player.width, self.player.y + self.player.height, self.matrix)
                    if enemy.shoot(self.player.x + self.player.width, self.player.y + self.player.height):
                        match enemy.color:
                            case 'brown':
                                self.bullets.append(BrownBullet(enemy.x + enemy.width, enemy.y + enemy.height, self.player.x + self.player.width / 2, self.player.y + self.player.height / 2))
                            case 'green':
                                self.bullets.append(FireBullet(enemy.x + enemy.width, enemy.y + enemy.height, self.player.x + self.player.width / 2, self.player.y + self.player.height / 2))
                            case 'red':
                                self.bullets.append(BrownBullet(enemy.x + enemy.width, enemy.y + enemy.height, self.player.x + self.player.width / 2, self.player.y + self.player.height / 2))
                            case 'purple':
                                self.bullets.append(FireBullet(enemy.x + enemy.width, enemy.y + enemy.height, self.player.x + self.player.width / 2, self.player.y + self.player.height / 2))
                            case 'yellow':
                                self.bullets.append(BrownBullet(enemy.x + enemy.width, enemy.y + enemy.height, self.player.x + self.player.width / 2, self.player.y + self.player.height / 2))
                        self.effectsChannel.play(self.shootSound)
                    if enemy.plantBomb():
                        self.bombs.append(Bomb(enemy.x + enemy.width / 2, enemy.y + enemy.height / 2))
                        self.effectsChannel.play(self.bombSound)
                    if enemy.checkHit(self.bullets, self.bombs):
                        self.score += 1
                        self.tankKills[enemy.color] += 1
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
                self.levelRunning = not self.player.checkHit(self.bullets, self.bombs)
    
                self.displayScreen()

            self.musicChannel.stop()
            if (not self.player.hit) and self.gameRunning:
                level += 1
                self.missionCompleteScreen()
            elif self.gameRunning:
                level = 0
                self.missionFailedScreen()
            if (self.player.hit or level >= maxLevel) and self.gameRunning:
                self.resultsScreen()
            
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
                self.blocks.append(Block(block['coordinates'][0], block['coordinates'][1], block['texture'], 'destroyable'))
            
            try:
                for hole in data['holes']:
                    self.blocks.append(Block(hole['coordinates'][0], hole['coordinates'][1] + 8, hole['texture'], 'hole'))
            except:
                pass

            self.matrix = data['matrix']

            for enemy in data['enemies']:
                match enemy['color']:
                    case 'brown':
                        self.enemies.append(BrownTank(enemy['coordinates'][0], enemy['coordinates'][1], self.blocks))
                    case 'green':
                        self.enemies.append(GreenTank(enemy['coordinates'][0], enemy['coordinates'][1], self.blocks))
                    case 'red':
                        self.enemies.append(RedTank(enemy['coordinates'][0], enemy['coordinates'][1], self.blocks))
                    case 'purple':
                        self.enemies.append(PurpleTank(enemy['coordinates'][0], enemy['coordinates'][1], self.blocks))
                    case 'yellow':
                        self.enemies.append(YellowTank(enemy['coordinates'][0], enemy['coordinates'][1], self.blocks))

            player = data['player']
            self.player = BlueTank(player['coordinates'][0], player['coordinates'][1], self.blocks)

        self.musicChannel.play(self.backgroundMusic, -1)
        running  = True
        i = 0

        while i < 75 and running:
            pygame.time.delay(5)
            self.displayScreen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.gameRunning = False
                    self.levelRunning = False
                    break

            i += 1

        i = 0
        while i < 25 and running:
            pygame.time.delay(5)
            self.displayScreen()
            # display start
            self.screen.blit(self.startImage, (525, 375))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.gameRunning = False
                    self.levelRunning = False
                    break

            i += 1

    def movePlayer(self, keys):
        # movement Sound
        if keys[pygame.K_w] or keys[pygame.K_d] or keys[pygame.K_s] or keys[pygame.K_a]:
            self.moveChannel.play(self.moveSound)
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
            tempBounceCount = bullet.bounceCount
            bullet.updatePos(self.blocks)
            if bullet.bounceCount > tempBounceCount and bullet.bounceCount <= bullet.bounceMax:
                self.effectsChannel.play(self.bulletBounceSound)
            if bullet.bounceCount > bullet.bounceMax:
                if bullet.type == "player":
                    self.player.bulletCount -= 1
                self.bullets.remove(bullet)

    def updateBombs(self):
        for bomb in self.bombs:
            bomb.update()
            if bomb.countdown == 0:
                bomb.checkBlockCollision(self.blocks)
            if bomb.explodeCount >= bomb.explodeMax:
                if bomb.type == 'player':
                    self.player.bombCount -= 1
                self.bombs.remove(bomb)

    def missionTitleScreen(self, level):
        with open(self.levels[level]) as levels_file:
            data = json.load(levels_file)

            self.musicChannel.play(self.startLevelSound)
            self.player = BlueTank(650, 700, self.blocks)
            running = True
            i = 0

            while i < 100 and running:
                # display background
                self.screen.blit(self.missionTitleBackground, (0, 0))

                # display text
                font = pygame.font.SysFont('impact', 125)
                text = font.render(f'Mission  {data["level"]}', True, (242, 234, 153))
                self.screen.blit(text, (450, 250))
                font = pygame.font.SysFont('impact', 75)
                text = font.render(f'Enemy tanks:  {len(data["enemies"])}', True, (242, 234, 153))
                self.screen.blit(text, (470, 450))

                # display player tank
                self.player.display(self.screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        self.gameRunning = False
                        self.levelRunning = False
                        break

                i += 1

                pygame.display.update()

    def missionCompleteScreen(self):
        self.musicChannel.play(self.missionCompleteSound)
        self.screen.blit(self.missionCompleteImage, (280, 300))
        self.screen.blit(self.scoreImage, (500, 500))
        font = pygame.font.SysFont('impact', 80)
        text = font.render(str(self.score), True, (43, 176, 231))
        self.screen.blit(text, (690, 560))
        pygame.display.update()

        pygame.time.delay(2000)

    def missionFailedScreen(self):
        self.musicChannel.play(self.missionFailedSound)
        font = pygame.font.SysFont('impact', 80)
        text = font.render('Mission Failed', True, (242, 234, 153))
        self.screen.blit(text, (450, 400))
        pygame.display.update()

        pygame.time.delay(2000)

    def resultsScreen(self):
        self.displayScreen()
        self.musicChannel.play(self.resultsSound)
        self.screen.blit(self.resultsImage, (450, 0))
        font = pygame.font.SysFont('impact', 70)

        running = True
        i = 0
        while i < 150 and running:
            pygame.time.delay(5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.gameRunning = False
                    self.levelRunning = False
                    break

            if i > 20:
                brown = BrownTank(500, 210, [])
                brown.display(self.screen, 650, 210)
                text = font.render(str(self.tankKills['brown']), True, (56, 32, 0))
                self.screen.blit(text, (710, 200))

            if i > 50:
                red = RedTank(500, 310, [])
                red.display(self.screen, 650, 310)
                text = font.render(str(self.tankKills['red']), True, (56, 32, 0))
                self.screen.blit(text, (710, 300))

            if i > 70:
                green = GreenTank(500, 410, [])
                green.display(self.screen, 650, 410)
                text = font.render(str(self.tankKills['green']), True, (56, 32, 0))
                self.screen.blit(text, (710, 400))

            if i > 85:
                purple = PurpleTank(500, 510, [])
                purple.display(self.screen, 650, 510)
                text = font.render(str(self.tankKills['purple']), True, (56, 32, 0))
                self.screen.blit(text, (710, 500))

            if i > 95:
                yellow = YellowTank(500, 610, [])
                yellow.display(self.screen, 650, 610)
                text = font.render(str(self.tankKills['yellow']), True, (56, 32, 0))
                self.screen.blit(text, (710, 600))

            if i == 110:
                self.screen.blit(self.scoreImage, (500, 700))
                font2 = pygame.font.SysFont('impact', 80)
                text = font2.render(str(self.score), True, (43, 176, 231))
                self.screen.blit(text, (690, 760))

            pygame.display.update()
            i += 1



if __name__ == '__main__':
    game = TanksGame()
    game.runGame()
