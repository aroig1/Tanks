import pygame 

class Button:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image ## pygame images

    def isClicked(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (self.x <= mouse_x <= self.x + self.image.get_width()) and (self.y <= mouse_y <= self.y + self.image.get_height()):
            return True
        else:
            return False