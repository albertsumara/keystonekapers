import random

from flying_enemy import FlyingEnemy
from bouncing_enemy import BouncingEnemy
from walking_enemy import WalkingEnemy

class Enemies:

    def __init__(self, level):

        self.level = level
        self.quantity_of_enemies = 4

        self.number_of_sections = 7
        self.number_of_floor = 3
        self.options = self.make_options()
        self.enemies_base = self.create_enemies()


    def create_enemies(self):

        enemies = []

        # last_enemy_type = "WalkingEnemy"
        for animal in range(self.level*self.quantity_of_enemies):
            if len(self.options) == 0:
                break

            section, floor, offset, enemy_type = self.find_position()

            if enemy_type == 'card':
                enemies.append(BouncingEnemy(section,floor,offset))

            elif enemy_type == 'bird':
                enemies.append(FlyingEnemy(section, floor, offset))

            elif enemy_type == 'dog':
                enemies.append(WalkingEnemy(section, floor, offset, enemy_type))

            elif enemy_type == 'rat':
                enemies.append(WalkingEnemy(section, floor, offset, enemy_type))

        return enemies



        #     if last_enemy_type == "WalkingEnemy":
        #         enemy_name = 'bird'
        #         section, floor, shift = self.find_position(enemy_name)
        #         enemies.append(FlyingEnemy(section, floor, shift))
        #         last_enemy_type = 'FlyingEnemy'
        #
        #     elif last_enemy_type == 'FlyingEnemy':
        #         enemy_name = 'card'
        #         section, floor, shift = self.find_position(enemy_name)
        #         enemies.append(BouncingEnemy(section, floor, shift))
        #         last_enemy_type = 'BouncingEnemy'
        #
        #     elif last_enemy_type == 'BouncingEnemy':
        #         enemy_name = random.choice(['dog', 'rat'])
        #         section, floor, shift = self.find_position(enemy_name)
        #         enemies.append(WalkingEnemy(section, floor, shift, enemy_name))
        #         last_enemy_type = 'WalkingEnemy'

    def make_options(self):

        options = []

        for section in range(1,self.number_of_sections+1):
            for floor in range(0, self.number_of_floor+1):
                options.append({'section' : section,
                                     'floor': floor,
                                     'offset': [0,-200,-400,-600],
                                     'enemy_type': random.choice(['dog', 'rat', 'bird', 'card'])})

        return options

    def find_position(self):

        index = random.randint(0, (len(self.options) - 1))
        choice = self.options[index]

        section = choice['section']
        floor = choice['floor']
        offset = choice['offset'].pop(0)
        enemy_type = choice['enemy_type']

        if len(choice['offset']) == 0:
            del self.options[index]

        return section, floor, offset, enemy_type



    # def exists_check(self, enemy_name):
    #
    #     no_founded = True
    #     while no_founded:
    #         exists = False
    #         other_enemy = False
    #
    #         section = random.randint(1,7)
    #         floor = random. randint(0,3)
    #
    #         for enemy, positions in self.map_of_enemies.items():
    #
    #             if enemy == enemy_name:
    #                 continue
    #             for position in positions:
    #                 if position['section'] == section and position['floor'] == floor:
    #                     other_enemy = True
    #                     break
    #             if other_enemy:
    #                 break
    #         if other_enemy:
    #             continue
    #
    #         for enemy in self.map_of_enemies[enemy_name]:
    #             i = 0
    #             if enemy['section'] == section and enemy['floor'] == floor:
    #                 exists = True
    #                 if enemy['shift'] != -600:
    #                     shift = enemy['shift'] - 200
    #                     self.map_of_enemies[enemy_name].insert(i, {
    #                         'section': section,
    #                         'floor' : floor,
    #                         'shift' : shift
    #                     })
    #                     return section, floor, shift
    #                 else:
    #                     break
    #             i += 1
    #         if not exists:
    #             shift = 0
    #             self.map_of_enemies[enemy_name].append({
    #                 'section': section,
    #                 'floor': floor,
    #                 'shift': shift
    #             })
    #             return section, floor, shift


    def get_enemy_base(self):
        return self.enemies_base

    def move_enemies(self):

        for enemy in self.enemies_base:
            enemy.move()

    # def enemies_print(self):
    #     for enemy, positions in self.map_of_enemies.items():
    #         print(f"{enemy}:")
    #         for position in positions:
    #             print(f"Sekcja: {position['section']}, piętro: {position['floor']}, przesunięcie: {position['shift']}")








