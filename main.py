import pygame
from settings import Settings
from blueTank import BlueTank
from bullet import Bullet

class TanksGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.screenSize)
        pygame.display.set_caption("Tanks")
        self.background = pygame.image.load('mapImages/woodbackground.png')

        self.player = BlueTank()
        
        self.bullets = []
        self.bulletCount = 0

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

            if pygame.mouse.get_pressed()[0]:
                self.bullets.append(Bullet(self.player.x + (self.player.image.get_width() / 2), self.player.y + (self.player.image.get_height() / 2)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameRunning = False

            for i in range(len(self.bullets)):
                self.bullets[i].updatePos()

            self.displayScreen()
        
        pygame.quit()

    def displayScreen(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image, (self.player.x, self.player.y))

        for bullet in self.bullets:
            self.screen.blit(bullet.image, (bullet.x, bullet.y))

        turret_img, turret_rect = self.player.getTurret()
        self.screen.blit(turret_img, turret_rect.topleft)
        pygame.display.update()


if __name__ == '__main__':
    game = TanksGame()
    game.runGame()
