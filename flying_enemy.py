from animator import Animator
from enemy_base import EnemyBase

class FlyingEnemy(EnemyBase):
    def __init__(self, section, floor, shift):
        super().__init__(section, floor)
        self.height = 32
        self.width = 32

        self.distance_from_top = -30

        self.shift = shift
        self.x += shift
        self.y = self.set_y()
        self.up_margin = 10
        self.side_margin = 10
        self.height_hitbox = self.height - 2*self.up_margin
        self.width_hitbox = self.width - 2*self.side_margin

        self.bird_frames = Animator.load_frames('enemy/bird.png', 32, 32,
                                                32, 32 ,6)

        self.bird_hurt_frames =  Animator.load_frames('enemy/bird_hurt.png', 32, 32,
                                                32, 32 ,2)

        self.animator_attack = Animator(self.bird_frames, 15)
        self.animator_hurted = Animator(self.bird_hurt_frames, 25)




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

        speed = 1
        if self.collision_status == 'Inactive':
            if self.status == 'Activated':
                self.reset()
                self.status = 'Active'

            if self.status == "Active":

                if self.entry_direction == 'right':
                    self.x += speed
                    if self.x > self.section_width - (self.width/2):
                        self.x = -10

                else:
                    self.x -= speed
                    if self.x < self.width/2:
                        self.x = self.section_width - (self.width/2)

    def set_y(self, first_floor=500):

        y = ((first_floor - self.before_floor_height -
             (self.floor * (self.before_floor_height + self.floor_height)))
             - self.distance_from_top)
        return y

    def reset(self):
        if self.entry_direction == "right":
            self.x = self.shift
        else:
            self.x = self.section_width - self.shift

        self.y = self.set_y()
