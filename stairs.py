from animator import Animator

class Stairs:

    def __init__(self):

        self.width = 300
        self.height = 150

        self.stair_frames = Animator.load_frames("stairs/moving_stairs1.png",
                                                 self.width, self.height, self.width, self.height, 6)

        self.frame_duration = 10

        self.stairs = {0 : {'section': 1,
                            'x': 250,
                            'y': 370,
                            'floor': 0,
                            'direction': 'left',
                            'animator': Animator(self.stair_frames, self.frame_duration)},
                       1: {'section': 7,
                           'x': 250,
                           'y': 240,
                           'floor': 1,
                           'direction': 'right',
                           'animator': Animator(self.stair_frames, self.frame_duration)},
                       2: {'section': 1,
                           'x': 250,
                           'y': 110,
                           'floor': 2,
                           'direction': 'left',
                           'animator': Animator(self.stair_frames, self.frame_duration)}}


    def draw(self, surface, section):
        for stair in self.stairs.values():
            stair_section = stair['section']
            x = stair['x']
            y = stair['y']
            direction = stair['direction']
            animator = stair['animator']

            if section == stair_section:
                flip = direction == 'right'
                animator.draw(surface, x, y, flip=flip)

        for stair in self.stairs.values():
            stair['animator'].update()


    def get_items(self):
        return self.stairs







