from animator import Animator
from enemy_base import EnemyBase

class BouncingEnemy(EnemyBase):
    def __init__(self, section, floor, shift):
        super().__init__(section, floor)
        self.height = 24
        self.width = 24

        self.shift = shift
        self.x += shift
        self.y = self.set_y()
        self.y_first = self.y

        self.up_margin = 6
        self.side_margin = 6
        self.height_hitbox = self.height - 2 * self.up_margin
        self.width_hitbox = self.width - 2 * self.side_margin

        self.rad = 10
        self.state = "flying_up"
        self.moving_speed = 0.00
        self.acceleration = "Increment"


        self.card_frames = Animator.load_frames('enemy/card.png', 24, 24, 24, 24 ,8)
        self.animator = Animator(self.card_frames, 30)



        self.section_width = 800


    def draw(self, surface):

        if self.status == "Active":
            self.animator.draw(surface, self.x, self.y)
            self.animator.update()


    def move(self):

        if self.status == 'Activated':
            self.reset()
            self.status = 'Active'

        if self.status == "Active":

            if self.collision_status == 'Inactive':
                if self.entry_direction == 'right':
                    self.x += 0.25 + self.moving_speed
                    if self.x > self.section_width - (self.width/2):
                        self.x = -10

                else:
                    self.x -= 0.25 + self.moving_speed
                    if self.x < self.width/2:
                        self.x = self.section_width - (self.width/2)

                range = self.before_floor_height/2 - self.width/2
                up_max = self.y_first - range
                down_max = self.y_first + range


                if self.state == "flying_up":
                    if self.y > (up_max):
                        self.y -= 0.25
                    if self.y <= (up_max):
                        self.state = "flying_down"

                elif self.state == "flying_down":
                    if self.y < (down_max):
                        self.y += 0.25
                    if self.y >= (down_max):
                        self.state = "flying_up"

                if self.acceleration == "Increment":
                    if self.moving_speed < 0.40:
                        self.moving_speed += 0.01
                    else:
                        self.acceleration = "Decrement"
                elif self.acceleration == "Decrement":
                    if self.moving_speed > 0:
                        self.moving_speed -= 0.01
                    else:
                        self.acceleration = "Increment"

    def set_y(self, first_floor=500):

        y = (first_floor - (self.before_floor_height/2) - (self.height/2) -
             ((self.floor) * (self.before_floor_height+self.floor_height)))
        return y

    def reset(self):
        if self.entry_direction == "right":
            self.x = self.shift
        else:
            self.x = self.section_width - self.shift

        self.y = self.set_y()
