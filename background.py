import pygame

class Background:

    def __init__(self):
        self.backgrounds = [
            [pygame.image.load('background/1.png'), [0, 0], 0],
            [pygame.image.load('background/2.png'), [0, 0], 1],
            [pygame.image.load('background/3.png'), [0, 0], 2],
            [pygame.image.load('background/4.png'), [0, 0], 3],
            [pygame.image.load('background/5.png'), [0, 0], 4],
            [pygame.image.load('background/2.png'), [800, 0], 1],
            [pygame.image.load('background/3.png'), [800, 0], 2],
            [pygame.image.load('background/5.png'), [800, 0], 4],
        ]

        for i in range(len(self.backgrounds)):
            original_image = self.backgrounds[i][0]
            scaled_image = pygame.transform.scale(original_image, (800, 600))
            self.backgrounds[i][0] = scaled_image

    def draw(self, surface):
        for image, position, _ in self.backgrounds:
            surface.blit(image, position)

    def moveLeft(self):
        for i, (image, position, layer_id) in enumerate(self.backgrounds):
            if layer_id == 1:
                position[0] -= 0.05
            elif layer_id == 2:
                position[0] -= 0.1
            elif layer_id == 4:
                position[0] -= 0.2

            if position[0] <= -800:
                position[0] += 1600

    def moveRight(self):
        for i, (image, position, layer_id) in enumerate(self.backgrounds):
            if layer_id == 1:
                position[0] += 0.05
            elif layer_id == 2:
                position[0] += 0.1
            elif layer_id == 4:
                position[0] += 0.2

            if position[0] >= 800:
                position[0] -= 1600

    def train(self):

        self.backgrounds[3][1][0] -= 0.2

        if  self.backgrounds[3][1][0] < -800:
            self.backgrounds[3][1][0] = -20




