import pygame

class Floor:


    def __init__(self):
        self.floor = pygame.image.load('section/floor.png')
        self.first_floor_y = 500

    def draw(self, surface):

        y = self.first_floor_y

        for i in range(4):
            surface.blit(self.floor, [0, y])
            y -= 130




