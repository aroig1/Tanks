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
            self.player.shoot()

            # Place bombs
            self.player.plantBomb(keys)

            for enemy in self.enemies:
                enemy.shoot(self.player.x + self.player.width, self.player.y + self.player.height)
                enemy.updateBullets()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameRunning = False

            # Update / Remove Bullets
            self.player.updateBullets()

            # Update / Explode Bombs
            self.player.updateBombs()

            self.displayScreen()
        
        pygame.quit()

    def displayScreen(self):
        # display background
        self.screen.blit(self.background, (0, 0))

        # display all player tank items
        self.player.display(self.screen)

        # display enemies
        for enemy in self.enemies:
            enemy.display(self.screen, self.player.x + self.player.width, self.player.y + self.player.height)

        # update display
        pygame.display.update()


if __name__ == '__main__':
    game = TanksGame()
    game.runGame()
