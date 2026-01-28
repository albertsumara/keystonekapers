import pygame


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('menu/press_start.ttf', 28)

    def draw_text(self, text, move=False ,color='black'):

        value = text['value']

        if 0 < value <= 10:
            color = 'red'

        text_to_print  = self.font.render(str(text['value']), True, color)

        x = text['x']
        y = text['y']
        if move:
            x -= text_to_print.get_size()[0]

        self.screen.blit(text_to_print, (x, y))

    def draw(self, player, enemies, background, floors, stairs, elevator, gameMap, bonuses, thief, points, time):
        self.screen.fill((0, 0, 0))

        background.draw(self.screen)
        bonuses.draw_bonuses(self.screen)


        #HITBOX CHECKING
        # for enemy in enemies:
        #     pygame.draw.rect(self.screen, 'red', enemy.get_collision_rect())
        # pygame.draw.rect(self.screen, 'blue', player.get_collision_rect())
        # pygame.draw.rect(self.screen, 'green', thief.get_collision_rect())


        if player.section == 4:

            if player.actions['elevator']['state'] in ['Inside', 'Moving', 'Readiness']:
                elevator.drawBackground(self.screen)
                floors.draw(self.screen)
                player.draw(self.screen)
                elevator.draw(self.screen)

            else:
                elevator.drawBackground(self.screen)
                elevator.draw(self.screen)
                floors.draw(self.screen)
                player.draw(self.screen)

        else:
            floors.draw(self.screen)
            player.draw(self.screen)

        if player.section == thief.section:
            thief.draw(self.screen)

        for enemy in enemies:
            if enemy.status == "Active":
                enemy.draw(self.screen)

        gameMap.draw(self.screen, player, thief)
        stairs.draw(self.screen, player.getSection())

        self.draw_text(points)
        self.draw_text(time, True)

        pygame.display.flip()

