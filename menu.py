import pygame
import sys
from game import Game


class Menu:

    def __init__(self):
        pygame.init()

        pygame.mixer.music.load("audio/menu.mp3")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(loops=-1)

        self.width = 800
        self.height = 600
        self.fps = 200
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Menu")

        self.backgrounds = [
            [pygame.image.load('menu/img/1.png'), [0, 0], 0],
            [pygame.image.load('menu/img/2.png'), [0, 0], 1],
            [pygame.image.load('menu/img/3.png'), [0, 0], 2],
            [pygame.image.load('menu/img/4.png'), [0, 0], 3],
            [pygame.image.load('menu/img/5.png'), [0, 0], 4],
            [pygame.image.load('menu/img/2.png'), [800, 0], 1],
            [pygame.image.load('menu/img/3.png'), [800, 0], 2],
            [pygame.image.load('menu/img/5.png'), [800, 0], 4],
        ]

        for i in range(len(self.backgrounds)):
            original_image = self.backgrounds[i][0]
            scaled_image = pygame.transform.scale(original_image, (800, 600))
            self.backgrounds[i][0] = scaled_image

        self.font_main = pygame.font.Font('menu/press_start.ttf', 40)
        self.font = pygame.font.Font('menu/press_start.ttf', 32)
        self.text = self.font_main.render('Menu główne', True, ('black'))

        self.side_space = 50
        self.space_between_top = 20
        self.margin = 50

        self.main_text_width, self.main_text_height = self.text.get_size()
        self.main_text_background_width, self.main_text_background_height = self.main_text_width + self.side_space, self.space_between_top * 2 + self.main_text_height
        self.main_text_background_surface = pygame.Surface((self.main_text_background_width, self.main_text_background_height),
                                                      pygame.SRCALPHA)


        self.text_background_width, self.text_background_height = self.main_text_width + self.side_space, self.height
        self.text_background_surface = pygame.Surface((self.text_background_width, self.text_background_height),
                                                      pygame.SRCALPHA)
        self.gray_main_text= (50,70,90,160)
        self.main_text_background_surface.fill(self.gray_main_text)
        self.gray_text= (90,100,120,128)
        self.text_background_surface.fill(self.gray_text)

        self.menu_options_text = [
                                    "Nowa gra",
                                    "Wyjdź z gry"]

        self.option_surfaces = []


        self.x_options, self.y_options = self.prepare_menu_surface()

        self.current_option = 0
        self.current_option_width, self.current_option_height = (self.main_text_background_width, self.main_text_background_height
                                                                 + self.margin/2)
        self.current_option_surface = pygame.Surface(
            (self.current_option_width, self.current_option_height),
            pygame.SRCALPHA)
        self.current_option_surface.fill(self.gray_main_text)

        self.last_score = None

    def draw(self):
        self.draw_background()
        self.draw_current_option_background()
        self.draw_text_menu()

    def draw_background(self):
        for image, position, _ in self.backgrounds:
            self.screen.blit(image, position)

    def draw_text_menu(self):

        self.screen.blit(self.main_text_background_surface, (self.width / 2 - self.text_background_width / 2, 0))
        self.screen.blit(self.text_background_surface, (self.width / 2 - self.text_background_width / 2, 0))
        self.screen.blit(self.text, (self.width / 2 - self.main_text_width / 2, self.space_between_top))


        if self.last_score is not None:
            text = self.font.render(f"Wynik: {self.last_score}", True, 'black')
            x, y = text.get_size()
            self.screen.blit(text, (self.width / 2 - x / 2, self.space_between_top +
                                         self.main_text_background_height))

        i = 0
        for option_text in self.option_surfaces:
            x,y = option_text.get_size()
            width = self.width/2 - x/2
            height = (self.height - len(self.option_surfaces) * y - (len(self.option_surfaces) - 1)
                      * self.margin) / 2 + i * (y + self.margin)
            self.screen.blit(option_text, (width, height))
            i += 1

    def draw_current_option_background(self):
        x, y = self.option_surfaces[self.current_option].get_size()

        highlight_height = y + self.margin
        highlight_width = self.text_background_width

        highlight_surface = pygame.Surface((highlight_width, highlight_height), pygame.SRCALPHA)
        highlight_surface.fill(self.gray_main_text)

        width = self.width / 2 - highlight_width / 2
        height = (self.height - len(self.option_surfaces) * y - (len(self.option_surfaces) - 1)
                  * self.margin) / 2 + self.current_option * (y + self.margin) - self.margin / 2

        self.screen.blit(highlight_surface, (width, height))

    def prepare_menu_surface(self):

        for option_text in self.menu_options_text:
            self.option_surfaces.append(self.font.render(option_text, True, ('black')))

        x_max = 0
        y_sum = 0

        for option_text in self.option_surfaces:
            x, y = option_text.get_size()
            y_sum += y
            if y > y_sum:
                x_max = x

        return x_max, y_sum

    def move_background(self):
        for _, position, layer_id in self.backgrounds:
            if layer_id == 1:
                position[0] -= 0.2
            elif layer_id == 2:
                position[0] -= 0.3
            elif layer_id == 4:
                position[0] -= 0.4

            if position[0] <= -800:
                position[0] += 1600

        self.train()

    def train(self):
        self.backgrounds[3][1][0] -= 0.6
        if self.backgrounds[3][1][0] < -800:
            self.backgrounds[3][1][0] = -20

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    self.current_option += 1
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.current_option -= 1
                elif event.key == pygame.K_RETURN:
                    self.choose_option(self.current_option)

            self.validate_current_option()

    def validate_current_option(self):
        if self.current_option == -1:
            self.current_option = len(self.option_surfaces) - 1
        elif self.current_option > len(self.option_surfaces) - 1:
            self.current_option = 0

    def run(self):
        while True:
            self.handle_events()
            self.screen.fill((0, 0, 0))
            self.draw()
            self.move_background()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def choose_option(self, option):

        if option == 0:
            self.play_game()
        elif option == 1:
            pygame.quit()
            sys.exit()


    def play_game(self):

        total_points = 0
        level = 1

        while True:

            game = Game(level, total_points)
            status, points = game.run()
            total_points = points
            level += 1

            if not status:
                self.last_score = total_points
                return






if __name__ == "__main__":
    menu = Menu()
    menu.run()

    game = Game()
    game.run()
