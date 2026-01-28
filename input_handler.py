import pygame


class InputHandler:
    def __init__(self, player, background):
        self.player = player
        self.background = background

    def handle(self):
        keys = pygame.key.get_pressed()


        if self.player.actions['hurted']['state'] != 'Active':
            if keys[pygame.K_a] and self.player.actions['hide']['state'] == "Standing" \
                    and self.player.actions['stairs_up']['state'] in ["Stopped", "Ready_right", "Ready_left"] \
                    and self.player.actions['elevator']['state'] in ['Stopped', 'Ready']:
                self.player.x -= 1
                self.player.actions['running']['state'] = 'Running_left'
                self.player.actions['running']['direction'] = 'left'

                if self.player.validate_moving_background():
                    self.background.moveRight()

            elif keys[pygame.K_d] and self.player.actions['hide']['state'] == "Standing" \
                    and self.player.actions['stairs_up']['state'] in ["Stopped", "Ready_right", "Ready_left"]\
                    and self.player.actions['elevator']['state'] in ['Stopped', 'Ready']:
                self.player.x += 1
                self.player.actions['running']['state'] = 'Running_right'
                self.player.actions['running']['direction'] = 'right'

                if self.player.validate_moving_background():
                    self.background.moveLeft()

            else:
                self.player.actions['running']['state'] = 'Standing'

            if self.player.actions['stairs_up']['state'] == "Ready_right":
                self.player.actions['stairs_up']['state'] = "Go_right"
            if self.player.actions['stairs_up']['state'] == "Ready_left":
                self.player.actions['stairs_up']['state'] = "Go_left"


            if keys[pygame.K_w]:

                if self.player.actions['elevator']['state'] == 'Ready':
                    self.player.actions['elevator']['state'] = 'Inside'


                elif self.player.actions['stairs_up']['state'] == "Stopped" and \
                        self.player.actions['elevator']['state'] == 'Stopped':

                    if self.player.actions['jump']['state'] == "Stopped" and self.player.actions['hide']['state'] == "Standing":
                        self.player.actions['jump']['state'] = "Start"

            if keys[pygame.K_s] \
                    and self.player.actions['stairs_up']['state'] in ["Stopped", "Ready_right", "Ready_left"]:

                if self.player.actions['elevator']['state'] == 'Inside':
                    self.player.actions['elevator']['state'] = 'Escape'

                elif self.player.actions['jump']['state'] == "Stopped" and \
                      self.player.actions['elevator']['state'] in ["Stopped"]  :
                    self.player.actions['hide']['state'] = "In progress"
            else:
                if self.player.actions['hide']['state'] == "In progress":
                    self.player.actions['hide']['state'] = "Stopped"
                else:
                    self.player.actions['hide']['state'] = "Standing"
