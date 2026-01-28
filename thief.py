from animator import Animator

class Thief:


    def __init__(self):



        self.width = 128
        self.height = 70

        #HITBOX
        self.side_margin = 50
        self.up_margin = 0
        self.width_hitbox = self.width - 2*self.side_margin
        self.height_hitbox = self.height - self.up_margin

        self.thief_frames_running = Animator.load_frames('thief/thief_run1.png', self.width , self.height,
                                                         self.width , self.height, 10)
        self.animator_run = Animator(self.thief_frames_running, 15)

        self.thief_frames_jumping = Animator.load_frames('thief/thief_jump.png', self.width, self.height,
                                                         self.width, self.height, 1)

        self.animator_jump = Animator(self.thief_frames_jumping, 50)

        self.screen_width = 800
        self.screen_height = 800
        self.last_floor_y = 500
        self.space_between_floors = 130
        self.stair_width = 300


        self.section = 4
        self.floor = 1


        self.x = self.screen_width/2 - self.width/2
        self.y = None
        self.update_y()

        self.actions = {'jump': {'state': 'Stopped',
                            'first_y': self.y,
                            'direct_y': None}}

        self.floors = {0: 'left',
                       1: 'right',
                       2: 'left',
                       3: 'right'}

        self.flip = False

        self.is_caught = False

    def update_y(self):

        self.y = self.last_floor_y - self.height - (self.space_between_floors * self.floor)


    def draw(self, surface):

        if self.get_action_state('jump') == 'Active':
            self.animator = self.animator_jump
        else:
            self.animator = self.animator_run

        self.animator.draw(surface, self.x, self.y, self.flip)
        self.animator.update()

    def run_away(self):
        direction_run = self.floors[self.floor]

        jumping = self.get_action_state('jump')

        if self.is_caught:
            return

        if jumping == 'Active':
            if self.y > self.actions['jump']['direct_y']:
                self.y -= 1
            if self.y <= self.actions['jump']['direct_y']:
                self.actions['jump']['state'] = 'Stopped'
            return

        speed = 0.6

        # Ruch w zależności od kierunku przypisanego do danego piętra
        if direction_run == 'right':
            self.x += speed
            self.flip = False
        elif direction_run == 'left':
            self.x -= speed
            self.flip = True

        left_hitbox = self.x + self.side_margin
        right_hitbox = left_hitbox + self.width_hitbox

        if right_hitbox > self.screen_width:
            if self.section < 7:
                self.section += 1
                self.x = -self.side_margin
            else:
                self.x = self.screen_width - self.side_margin - self.width_hitbox

        elif left_hitbox < 0:
            if self.section > 1:
                self.section -= 1
                self.x = self.screen_width - self.side_margin - self.width_hitbox
            else:
                self.x = -self.side_margin + 1

        x = self.x + self.side_margin

        if self.section == 7 and self.floor == 1 and x > self.screen_width/2 - self.stair_width/2:
            self.floor += 1
            self.actions['jump']['state'] = 'Active'
            self.actions['jump']['first_y'] = self.y
            self.actions['jump']['direct_y'] = self.y - self.space_between_floors

        if self.section == 1 and self.floor == 2 and x < self.screen_width /2 + self.screen_width/2:
            self.floor += 1
            self.actions['jump']['state'] = 'Active'
            self.actions['jump']['first_y'] = self.y
            self.actions['jump']['direct_y'] = self.y - self.space_between_floors

    def get_collision_rect(self):

        x_hitbox, y_hitbox = self.x + self.side_margin, self.y + self.up_margin
        return (x_hitbox, y_hitbox, self.width_hitbox, self.height_hitbox)

    def get_action_state(self, action):

        return self.actions[action]['state']