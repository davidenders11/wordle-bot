import pygame
from pygame.locals import *

restart_game_img = pygame.image.load('restart_button.jpeg').convert_alpha()

# Button class with scaling for size
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

# surface = screen variable in game loop
def draw(self, surface):

    #gets mouse position in game window
    pos = pygame.mouse.get_pos()

    #if button is clicked
    if self.rect.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            print('CLICKED RESTART')
            self.clicked = True

    if pygame.mouse.get_pressed()[0] == 0:
        self.clicked = False

    #draw button on screen
    surface.blit(self.image, (self.rect.x, self.rect.y))