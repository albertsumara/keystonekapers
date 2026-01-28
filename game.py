import pygame
import sys

from bonus import Bonuses
from player import Player
from enemies import Enemies
from input_handler import InputHandler
from renderer import Renderer
from background import Background
from floors import Floor
from stairs import Stairs
from elevator import Elevator
from map import GameMap
from thief import Thief


class Game:

    pygame.init()
    def __init__(self,level=1 ,start_points=0,):

        pygame.display.set_caption("The Game")

        self.points = {'value' : start_points,
                       'x': 10,
                       'y': 530}

        self.time_to_lose = {'value': 50,
                             'x': 790,
                             'y': 530}

        self.time_measure = 0
        self.last_update_time = 0
        self.bonus_per_second = 100


        self.background = Background()
        self.floors = Floor()
        self.stairs = Stairs()
        self.elevator = Elevator()
        self.gameMap = GameMap()

        self.level = level
        self.width = 800
        self.height = 600
        self.fps = 200
        self.screen = pygame.display.set_mode((self.width, self.height))


        self.player = Player()

        self.thief = Thief()

        self.enemies = Enemies(self.level)
        self.enemies_base = self.enemies.get_enemy_base()

        self.bonuses = Bonuses(self.level)

        self.input_handler = InputHandler(self.player, self.background)
        self.renderer = Renderer(self.screen)
        self.collision_detected = False

    def collision_detection(self, player, other):
        player_rect = pygame.Rect(player.get_collision_rect())
        other_rect = pygame.Rect(other.get_collision_rect())

        stairs_up_state = player.get_action_state('stairs_up')
        elevator_state = player.get_action_state('elevator')

        if elevator_state in ['Ready', 'Stopped'] \
                and stairs_up_state not in ['In_progress_left', 'In_progress_right']:
            return player_rect.colliderect(other_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def handle_input(self):
        self.input_handler.handle()

    def check_collision_player(self):
        now = pygame.time.get_ticks()
        i = -1
        enemy_base_ = self.enemies_base.copy()
        for enemy in self.enemies_base:
            i += 1
            if enemy.section != self.player.section:
                enemy.status = "Inactive"
                continue
            if enemy.status != 'Active':
                enemy.status = 'Activated'
                enemy.entry_direction = self.player.entered_from
            if self.collision_detection(self.player, enemy):
                if enemy.collision_status != 'Active':
                    self.time_to_lose['value'] -= 5
                    enemy.collision_status = 'Active'
                    self.collision_detected = True
                    enemy.hit_time = now
                    self.player.actions['hurted']['state'] = 'Active'
            if enemy.collision_status == 'Active' and (now - enemy.hit_time) >= 1000:
                del enemy_base_[i]
                self.player.actions['hurted']['state'] = 'Stopped'
                self.enemies_base = enemy_base_
                self.collision_detected = False
                break

        self.enemies_base = enemy_base_






    def update(self):

        self.background.train()
        self.player.update()
        self.player.check_actions()


        self.check_stairs_with_player()
        self.moving_up_stairs()

        self.player.validate_cords_player()

        self.check_elevator_with_player()
        self.moving_by_elevator()
        self.elevator.update()

        self.update_time()

        if not self.collision_detected:
            self.enemies.move_enemies()
        self.check_collision_player()
        self.check_player_with_bonuses()
        self.thief.run_away()

        self.check_thief_collision()





    def draw(self):
        self.renderer.draw(self.player, self.enemies_base, self.background,
                           self.floors, self.stairs, self.elevator,
                           self.gameMap, self.bonuses, self.thief, self.points, self.time_to_lose)

    def play_music(self):
        pygame.mixer.music.load("audio/game.mp3")
        pygame.mixer.music.set_volume(0.10)
        pygame.mixer.music.play(loops=-1)

    def run(self):

        self.play_music()
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.fps)
            self.handle_events()
            self.handle_input()
            self.update()
            self.draw()

            if self.thief.is_caught:
                return True, self.points['value']

            if self.time_to_lose['value'] < 1 :
                return False, self.points['value']

    def check_stairs_with_player(self):
        if self.player.actions['stairs_up']['state'] not in ['Stopped', 'Ready_right', 'Ready_left']:
            return

        x,y,size_x,size_y = self.player.get_collision_rect()
        check_space = 20

        for stair in self.stairs.get_items().values():
            if (stair['section'] == self.player.section) and self.player.floor == stair['floor']:
                if stair['direction'] == 'right' and (stair['x']
                                                      < x < stair['x'] + check_space):
                    self.player.actions['stairs_up']['state'] = 'Ready_right'
                    self.player.actions['stairs_up']['start_x'] = stair['x'] - self.player.side_margin
                elif stair['direction'] == 'left' and (stair['x'] + self.stairs.width - check_space
                                                       < x < stair['x'] + self.stairs.width):
                    self.player.actions['stairs_up']['state'] = 'Ready_left'
                    self.player.actions['stairs_up']['start_x'] = (stair['x'] + self.stairs.width
                                                                   - size_x - self.player.side_margin)
                else:
                    self.player.actions['stairs_up']['state'] = 'Stopped'



    def moving_up_stairs(self):
        if self.player.actions['stairs_up']['state'] == "Go_right":
            self.player.x = self.player.actions['stairs_up']['start_x']
            self.player.actions['stairs_up']['start_x'] = self.player.x
            self.player.actions['stairs_up']['start_y'] = self.player.y
            self.player.actions['stairs_up']['state'] = "In_progress_right"

        elif self.player.actions['stairs_up']['state'] == "Go_left":
            self.player.x = self.player.actions['stairs_up']['start_x']
            self.player.actions['stairs_up']['start_x'] = self.player.x
            self.player.actions['stairs_up']['start_y'] = self.player.y
            self.player.actions['stairs_up']['state'] = "In_progress_left"

        if self.player.actions['stairs_up']['state'] == "In_progress_right":
            start_x = self.player.actions['stairs_up']['start_x']
            start_y = self.player.actions['stairs_up']['start_y']

            if self.player.x < start_x + 300:
                self.player.x += 0.5

            if self.player.y > start_y - 130:
                self.player.y -= 0.25

            if self.player.y <= start_y - 130:
                self.player.y = start_y - 130
                self.player.y_ = self.player.y
                self.player.floor += 1
                self.player.actions['stairs_up']['state'] = "Stopped"

        if self.player.actions['stairs_up']['state'] == "In_progress_left":
            start_x = self.player.actions['stairs_up']['start_x']
            start_y = self.player.actions['stairs_up']['start_y']

            if self.player.x > start_x - 300:
                self.player.x -= 0.5
            if self.player.y > start_y - 130:
                self.player.y -= 0.25

            if self.player.y <= start_y - 130:
                self.player.y = start_y - 130
                self.player.y_ = self.player.y
                self.player.floor += 1
                self.player.actions['stairs_up']['state'] = "Stopped"

    def check_elevator_with_player(self):


        x = self.player.get_collision_rect()[0]

        elevator_state = self.elevator.get_current_door_state(self.player.floor)

        if self.player.actions['elevator']['state'] not in ['Moving', 'Readiness', 'Inside']:
            if elevator_state in ['closing', 'closed']:
                self.player.actions['elevator']['state'] = 'Stopped'

        if self.elevator.check_availability(self.player.floor) and self.player.section == 4:

            if self.player.actions['elevator']['state'] == 'Escape':
                self.player.actions['elevator']['state'] = 'Ready'

            if self.elevator.get_x_door() < x <  self.elevator.get_x_door() + self.elevator.door_size:
                if self.player.actions['elevator']['state'] == 'Stopped':
                    self.player.actions['elevator']['state'] = 'Ready'

            else:
                if self.player.actions['elevator']['state'] not in ['Inside', 'Escape']:
                    self.player.actions['elevator']['state'] = 'Stopped'
        else:
            if self.player.actions['elevator']['state'] == 'Escape':
                self.player.actions['elevator']['state'] = 'Inside'




        if self.player.actions['elevator']['state'] == 'Inside':
            for elevator_pos in self.elevator.getElevator_position().values():
                if elevator_pos['state'] == "closing":
                    self.player.actions['elevator']['state'] = 'Moving'

        if self.player.actions['elevator']['state'] == 'Moving':
            for floor, elevator_pos in self.elevator.getElevator_position().items():
                if elevator_pos['state'] == "opening":
                    self.player.actions['elevator']['state'] = 'Readiness'
                    self.player.actions['elevator']['floor'] = floor

    def moving_by_elevator(self):
        if self.player.actions['elevator']['state'] == 'Inside':
            self.player.x = self.width/2 - self.player.width/2

        if self.player.actions['elevator']['state'] == 'Readiness':
            self.player.y = self.player.y - ((self.player.actions['elevator']['floor'] - self.player.floor) * 130)
            self.player.y_ = self.player.y
            self.player.floor = self.player.actions['elevator']['floor']
            self.player.actions['elevator']['state'] = 'Inside'


    def check_player_with_bonuses(self):

        for bonus in self.bonuses.bonuses:
            if bonus.section != self.player.section:
                bonus.visible = False
                continue
            else:
                bonus.visible = True

            if self.collision_detection(self.player, bonus) and bonus.collision_status != 'Active':
                bonus.collision_status = 'Activated'
                bonus_type = bonus.__class__.__name__


                if not bonus.points_collected:
                    bonus.points_collected = True
                    if bonus_type == 'Chest':
                        self.points['value'] += 100
                    else:
                        self.points['value'] += 50

                bonus.collision_time = pygame.time.get_ticks()

    def update_time(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.last_update_time
        self.time_measure += elapsed

        if self.time_measure > 2000:
            self.time_to_lose['value'] -= 1
            self.time_measure = 0

        self.last_update_time = current_time

    def check_thief_collision(self):

        if self.player.section != self.thief.section:
            return

        if self.collision_detection(self.player, self.thief):

            if not self.thief.is_caught:
                self.points['value'] += self.time_to_lose['value'] * self.bonus_per_second
                self.thief.is_caught = True
                self.level += 1








