import pygame
from settings import Settings
from blueTank import BlueTank
from brownTank import BrownTank
from bullet import Bullet
from bomb import Bomb

class TanksGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.screenSize)
        pygame.display.set_caption("Tanks")
        self.background = pygame.image.load('mapImages/woodbackground.png')

        self.player = BlueTank()

        self.enemies = [BrownTank()]
        
        self.bullets = []
        self.bulletCount = 0

        self.bombs = []
        self.bombCount = 0

        self.gameRunning = True

    def runGame(self):
        while self.gameRunning:
            pygame.time.delay(10)

            keys = pygame.key.get_pressed()

            ## Movement
            if keys[pygame.K_w] and keys[pygame.K_d]:
                self.player.image = self.player.sprites[1]
                self.player.move(1.41, -1.41)
            elif keys[pygame.K_d] and keys[pygame.K_s]:
                self.player.image = self.player.sprites[3]
                self.player.move(1.41, 1.41)
            elif keys[pygame.K_s] and keys[pygame.K_a]:
                self.player.image = self.player.sprites[1]
                self.player.move(-1.41, 1.41)
            elif keys[pygame.K_a] and keys[pygame.K_w]:
                self.player.image = self.player.sprites[3]
                self.player.move(-1.41, -1.41)
            elif keys[pygame.K_w]:
                self.player.image = self.player.sprites[0]
                self.player.move(0, -2)
            elif keys[pygame.K_d]:
                self.player.image = self.player.sprites[2]
                self.player.move(2, 0)
            elif keys[pygame.K_s]:
                self.player.image = self.player.sprites[0]
                self.player.move(0, 2)
            elif keys[pygame.K_a]:
                self.player.image = self.player.sprites[2]
                self.player.move(-2, 0)

        
            # Shoot bullets
            if pygame.mouse.get_pressed()[0] and self.bulletCount <= self.settings.maxBullets:
                self.bullets.append(Bullet(self.player.x + (self.player.image.get_width() / 2), self.player.y + (self.player.image.get_height() / 2)))
                self.bulletCount += 1

            # Place bombs
            if keys[pygame.K_SPACE] and self.bombCount <= self.settings.maxBombs:
                self.bombs.append(Bomb(self.player.x + (self.player.image.get_width() / 2), self.player.y + (self.player.image.get_height() / 2)))
                self.bombCount += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameRunning = False

            # Update / Remove Bullets
            for i in range(len(self.bullets)):
                try:
                    self.bullets[i].updatePos()
                    if self.bullets[i].bounceCount > self.bullets[i].bounceMax:
                        self.bullets.pop(i)
                        self.bulletCount -= 1
                        i -= 1
                except:
                    continue

            # Update / Explode Bombs
            for i in range(len(self.bombs)):
                try:
                    self.bombs[i].update()
                    if self.bombs[i].explodeCount >= self.bombs[i].explodeMax:
                        self.bombs.pop(i)
                        self.bombCount -= 1
                        i -= 1
                except:
                    continue

            self.displayScreen()
        
        pygame.quit()

    def displayScreen(self):
        # display background
        self.screen.blit(self.background, (0, 0))

        # display bombs
        for bomb in self.bombs:
            self.screen.blit(bomb.image, (bomb.x, bomb.y))
        # display tank base
        self.screen.blit(self.player.image, (self.player.x, self.player.y))
        # display bullets
        for bullet in self.bullets:
            self.screen.blit(bullet.image, (bullet.x, bullet.y))
        # display tank turret
        turret_img, turret_rect = self.player.getTurret()
        self.screen.blit(turret_img, turret_rect.topleft)

        # display enemies
        for enemy in self.enemies:
            # display enemy tank base
            self.screen.blit(enemy.image, (enemy.x, enemy.y))
            # displat enemy tank turret
            turret_img, turret_rect = enemy.getTurret(self.player.x + self.player.width, self.player.y + self.player.height)
            self.screen.blit(turret_img, turret_rect.topleft)

        # update display
        pygame.display.update()


if __name__ == '__main__':
    game = TanksGame()
    game.runGame()
