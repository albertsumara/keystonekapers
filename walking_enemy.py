from enemy_base import EnemyBase
from animator import Animator

class WalkingEnemy(EnemyBase):
    def __init__(self, section, floor, shift, animal_type):
        super().__init__(section, floor)

        self.animal_type = animal_type
        if self.animal_type == 'rat':
            self.animal_frames = Animator.load_frames('enemy/rat.png',
                                                      32, 32, 32, 32, 4)
            self.animal_hurted_frames = Animator.load_frames('enemy/rat_hurt.png',
                                                      32, 32, 32, 32, 2)
            self.height = 32
            self.width = 32
            self.speed = 1

        if self.animal_type == 'dog':
            self.animal_frames = Animator.load_frames('enemy/dog.png',
                                                      48, 48, 48, 48, 6)
            self.animal_hurted_frames = Animator.load_frames('enemy/dog_hurt.png',
                                                             48, 48, 48, 48, 2)
            self.height = 48
            self.width = 48
            self.speed = 0.8

        self.shift = shift
        self.x += shift
        self.y = self.set_y()
        self.y_first = self.y

        self.up_margin = 25
        self.side_margin = 15
        self.height_hitbox = self.height - self.up_margin
        self.width_hitbox = self.width - 2 * self.side_margin


        self.animator_attack = Animator(self.animal_frames, 15)
        self.animator_hurted = Animator(self.animal_hurted_frames, 25)

        self.section_width = 800

    def draw(self, surface):

        if self.collision_status == 'Active':
            self.animator = self.animator_hurted
            if self.entry_direction == 'left':
                self.animator.draw(surface, self.x, self.y, True)
            else:
                self.animator.draw(surface, self.x, self.y)
        else:
            self.animator = self.animator_attack
            if self.status == "Active":
                if self.entry_direction == 'left':
                    self.animator.draw(surface, self.x, self.y, True)
                else:
                    self.animator.draw(surface, self.x, self.y)
        self.animator.update()


    def move(self):
        if self.collision_status == 'Inactive':
            if self.status == 'Activated':
                self.reset()
                self.status = 'Active'

            if self.status == "Active":

                if self.entry_direction == 'right':
                    self.x += self.speed
                    if self.x > self.section_width:
                        self.x = -10

                else:
                    self.x -= self.speed
                    if self.x < self.width / 2:
                        self.x = self.section_width


    def set_y(self, first_floor=500):

        y = first_floor - self.height - ((self.before_floor_height+self.floor_height)*self.floor)
        return y

    def reset(self):
        if self.entry_direction == "right":
            self.x = self.shift
        else:
            self.x = self.section_width - self.shift

        self.y = self.set_y()


