from animator import Animator

class Player:

    def __init__(self):
        self.x = 380
        self.y = 430
        self.y_ = 430

        self.normal_height = 70
        self.hiding_height = 50
        self.height = 70
        self.width = 128
        #HITBOX

        self.side_margin = 50
        self.up_margin = 10
        self.height_hitbox = self.height - self.up_margin
        self.width_hitbox = self.width - 2*self.side_margin


        self.section = 7
        self.floor = 0

        self.entered_from = 'right'


        self.actions = {
            "jump": {'state': 'Stopped',
                     'start_y': self.y,
                     'speed': 1.0},

            "hide": {'state': "Standing"},

            "running": {'state': "Standing",
                        'direction' : "left"},

            "stairs_up": {'state' :'Stopped',
                          'start_x': 0,
                          'start_y': 0},

            "elevator": {'state': 'Stopped',
                         'floor': 0},#directfloor

            "hurted": {'state': 'Stopped'}

        }

        self.player_running_frames = Animator.load_frames('player/player_run1.png',
                                                          128, self.height, 128, self.height, 10)
        self.player_standing_frames = Animator.load_frames('player/player_standing1.png',
                                                           128, self.height, 128, self.height, 15)
        self.player_jumping_frames = Animator.load_frames('player/player_jumping1.png',
                                                          128, self.height, 128, self.height, 1)
        self.player_hiding_frames = Animator.load_frames('player/player_hiding1.png',
                                                         128, self.height, 128, self.height, 1)
        self.player_hurted_frames = Animator.load_frames('player/player_hurted1.png',
                                                         128, self.height, 128, self.height, 3)

        self.animator_standing = Animator(self.player_standing_frames, 60)
        self.animator_running = Animator(self.player_running_frames, 15)
        self.animator_jumping = Animator(self.player_jumping_frames)
        self.animator_hiding = Animator(self.player_hiding_frames)
        self.animator_hurted = Animator(self.player_hurted_frames, 25)

    def get_action_state(self, action):
        return self.actions[action]['state']

    def update(self):
        running_state = self.get_action_state('running')
        jumping_state = self.get_action_state('jump')
        hiding_state = self.get_action_state('hide')
        stairs_state = self.get_action_state('stairs_up')
        hurted_state = self.get_action_state('hurted')


        if hurted_state == 'Active':
            self.animator = self.animator_hurted
        elif stairs_state in ['In_progress_left', 'In_progress_right']:
            self.animator = self.animator_standing
        elif jumping_state != 'Stopped':
            self.animator = self.animator_jumping
        elif hiding_state == 'In progress':
            self.animator = self.animator_hiding
        elif running_state in ['Running_left', 'Running_right']:
            self.animator = self.animator_running
        else:
            self.animator = self.animator_standing

        self.animator.update()

    def draw(self, surface):
        stairs_state = self.get_action_state('stairs_up')
        direction = self.actions['running']['direction']

        if stairs_state in ['In_progress_left', 'Go_left']:
            direction = 'left'
        elif stairs_state in ['In_progress_right', 'Go_right']:
            direction = 'right'

        flip = direction == 'left'
        self.animator.draw(surface, self.x, self.y, flip=flip)

    def get_collision_rect(self):


        up_margin = self.up_margin
        if self.get_action_state('hide') == 'In progress':
            up_margin = self.up_margin + (self.normal_height - self.hiding_height)
        x_hitbox, y_hitbox = self.x + self.side_margin, self.y + up_margin

        return (x_hitbox, y_hitbox , self.width_hitbox , self.height_hitbox)



    def get_cords(self):
        return self.x, self.y

    def jump(self, distance=40):
        speed = self.actions['jump']['speed']

        if self.actions['jump']['state'] == "Start":
            self.actions['jump']['state'] = "In progress"
            self.actions['jump']['first_y'] = self.y #set y before jump

        elif self.actions['jump']['state'] == "In progress":
            if self.y > (self.actions['jump']['first_y'] - distance):
                self.y -= speed
                self.actions['jump']['speed'] = max(0.2, self.actions['jump']['speed'] - 0.01)
            else:
                self.actions['jump']['state'] = "Falling"

        elif self.actions['jump']['state'] == "Falling":
            if self.y < self.actions['jump']['first_y']:
                self.y += speed
                self.actions['jump']['speed'] = min(2.0, self.actions['jump']['speed'] + 0.01)
            else:
                if abs(self.y - self.actions['jump']['first_y']) < 2:
                    self.y = self.actions['jump']['first_y']
                self.actions['jump']['state'] = "Stopped"
                self.actions['jump']['speed'] = 1.0

    def validate_cords_player(self):
        screen_width = 800

        # Oblicz hitbox lewej i prawej krawędzi
        left_hitbox = self.x + self.side_margin
        right_hitbox = left_hitbox + self.width_hitbox

        if right_hitbox > screen_width:
            if self.section < 7:
                self.section += 1
                self.entered_from = 'left'
                self.x = -self.side_margin
            else:

                self.x = screen_width - self.side_margin - self.width_hitbox

        elif left_hitbox < 0:
            if self.section > 1:
                self.section -= 1
                self.entered_from = 'right'
                self.x = screen_width - self.side_margin - self.width_hitbox
            else:
                self.x = -self.side_margin + 1

    def validate_moving_background(self):
        if self.section == 1 and self.x <= 50:
            return False
        if self.section == 7 and self.x >= 750:
            return False
        return True

    def hiding(self):
        if self.actions['hide']['state'] == "In progress":
            self.height = self.hiding_height
            # self.y = self.y_ + (self.normal_height - hiding_height)
        elif self.actions['hide']['state'] == "Stopped":
            self.height = self.normal_height
            self.y = self.y_
            self.actions['hide']['state'] = "Standing"


    def check_actions(self):
        self.hiding()
        self.jump()

    def getSection(self):
        return self.section
