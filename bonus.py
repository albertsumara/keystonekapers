import random

import pygame.time

from animator import Animator
    
    
class Chest:

    def __init__(self, section, floor):

        self.screen_width = 800
        self.first_floor = 500
        self.next_floor = 130
        self.collision_time = None

        self.points_collected = False
        self.visible = False
        self.collision_status = 'Inactive'

        self.bonus_size = 32
        self.section = section
        self.floor = floor

        self.x = self.screen_width / 2 - self.bonus_size / 2
        self.y = self.first_floor - self.bonus_size - (self.floor * self.next_floor)

        self.current_frame = 0

        self.chest_to_open = Animator.load_frames('bonus/chest_to_pick.png', 32, 32,
                                                  32, 32, 1)
        self.chest_opening = Animator.load_frames('bonus/chest_opening.png', 32, 32,
                                                  32, 32, 4)
        self.chest_opened = Animator.load_frames('bonus/chest_opened.png', 32, 32,
                                                  32, 32, 1)

        self.animator_to_pick = Animator(self.chest_to_open, 100)
        self.animator_opening = Animator(self.chest_opening, 40)
        self.animator_opened = Animator(self.chest_opened, 100)

    def draw(self, surface):

        now = pygame.time.get_ticks()

        if self.collision_time and now - self.collision_time > 2000:
            return

        if self.collision_status == 'Inactive':
            self.animator = self.animator_to_pick


        elif self.collision_status == 'Activated':
            self.animator = self.animator_opening

            if self.animator.current_frame_index >= len(self.chest_opening) - 1:
                self.collision_status = 'Active'
                self.animator = self.animator_opened

        elif self.collision_status == 'Active':
            self.animator = self.animator_opened


        self.animator.draw(surface, self.x, self.y)
        self.animator.update()

    def get_collision_rect(self):
        return (self.x, self.y, self.bonus_size, self.bonus_size)


class Money:

    def __init__(self, section, floor):

        self.screen_width = 800
        self.first_floor = 500
        self.next_floor = 130

        self.collision_status = 'Inactive'
        self.visible = False
        self.points_collected = False

        self.bonus_size = 24
        self.section = section
        self.floor = floor

        self.x = self.screen_width / 2 - self.bonus_size / 2
        self.y = self.first_floor - self.bonus_size - (self.floor * self.next_floor)

        self.money_to_pick = Animator.load_frames('bonus/money_to_pick.png', 24, 24,
                                                  24, 24, 6)

        self.animator_to_pick = Animator(self.money_to_pick, 30)
        self.animator_picking = Animator(self.money_to_pick, 60)



    def draw(self, surface):


        if self.collision_status == 'Inactive':
            self.animator = self.animator_to_pick
            self.animator.draw(surface, self.x, self.y)
        if self.collision_status == 'Opening':
            self.animator = self.animator_to_pick

        self.animator.update()

    def get_collision_rect(self):

        return (self.x, self.y, self.bonus_size, self.bonus_size)


class Bonuses:

    def __init__(self, level):
        self.min_of_bonuses = 2
        self.level = level

        self.blocked = ((7, 1), (7, 0), (1, 0), (1, 2), (4, 0), (4, 1), (4, 2))
        self.number_of_sections = 7
        self.number_of_floor = 3

        self.options = self.make_options()
        self.bonuses = self.create_bonuses()

    def make_options(self):

        options = []
        for section in range(1, self.number_of_sections + 1):
            for floor in range(0, self.number_of_floor + 1):
                if (section, floor) in self.blocked:
                    continue
                options.append({'section': section,
                                'floor': floor,
                                'bonus_type': random.choice(['chest', 'money'])})
        return options

    def create_bonuses(self):

        bonuses = []

        bonuses_to_create = self.min_of_bonuses + self.level // 5


        for bonus in range(bonuses_to_create):
            option = self.options.pop(random.randint(0, len(self.options) - 1))
            section = option['section']
            floor = option['floor']
            bonus_type = option['bonus_type']
            if bonus_type == 'chest':
                bonuses.append(Chest(section,floor))
            else:
                bonuses.append(Money(section,floor))

        return bonuses

    def draw_bonuses(self, surface):

        for bonus in self.bonuses:
            if bonus.visible:
                bonus.draw(surface)


                
    
