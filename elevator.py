import pygame

from animator import Animator

class Elevator:
    def __init__(self):
        self.elevator_background = pygame.image.load('elevator/elevator_background_3.png')
        self.elevator_interior = pygame.image.load('elevator/elevator_interior_2.png')
        self.x_background = (800 - 124) / 2
        self.y_background = 600 - 500

        self.x_door = (800 - 124) / 2 + (124 - 80) / 2

        self.elevator_opening_frames = Animator.load_frames('elevator/elevator.png', 80, 80, 80, 80, 5)
        self.elevator_closing_frames = list(reversed(self.elevator_opening_frames))

        self.elevator_closed = pygame.image.load('elevator/elevator_closed.png')
        self.elevator_opened = pygame.image.load('elevator/elevator_opened.png')

        self.animator_opening = [Animator(self.elevator_opening_frames, 10) for _ in range(3)]
        self.animator_closing = [Animator(self.elevator_closing_frames, 10) for _ in range(3)]

        self.elevator_door_position = {0: {'state' :'opening'},
                                       1: {'state':'closed'},
                                       2: {'state':'closed'}}

        self.door_size = 80 #same width height

        self.floor_cycle = [0, 1, 2, 1]
        self.cycle_index = 0

        self.current_floor = self.floor_cycle[self.cycle_index]
        self.state = 'opening'
        self.state_start_time = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()

        if self.state == 'opening':
            anim = self.animator_opening[self.current_floor]
            anim.update()
            if anim.current_frame_index == len(anim.frames) - 1:
                self.elevator_door_position[self.current_floor]['state'] = 'opened'
                self.state = 'opened_waiting'
                self.state_start_time = now

        elif self.state == 'opened_waiting':
            if now - self.state_start_time > 5000:
                self.elevator_door_position[self.current_floor]['state'] = 'closing'
                self.animator_closing[self.current_floor].current_frame_index = 0
                self.animator_closing[self.current_floor].frame_counter = 0
                self.state = 'closing'
                self.state_start_time = now

        elif self.state == 'closing':
            anim = self.animator_closing[self.current_floor]
            anim.update()
            if anim.current_frame_index == len(anim.frames) - 1:
                self.elevator_door_position[self.current_floor]['state'] = 'closed'
                self.state = 'closed_waiting'
                self.state_start_time = now

        elif self.state == 'closed_waiting':
            if now - self.state_start_time > 2000:
                self.cycle_index = (self.cycle_index + 1) % len(self.floor_cycle)
                self.current_floor = self.floor_cycle[self.cycle_index]

                self.elevator_door_position[self.current_floor]['state'] = 'opening'
                self.animator_opening[self.current_floor].current_frame_index = 0
                self.animator_opening[self.current_floor].frame_counter = 0
                self.state = 'opening'
                self.state_start_time = now

    def draw(self, surface):


        for i in range(3):

            y = 500 - 80 - i * 130
            x = self.x_door

            state = self.elevator_door_position[i]['state']

            if state == 'opening':
                self.animator_opening[i].draw(surface, x, y)
            elif state == 'closing':
                self.animator_closing[i].draw(surface, x, y)
            elif state == 'opened':
                surface.blit(self.elevator_opened, (x, y))
            else:
                surface.blit(self.elevator_closed, (x, y))


    def drawBackground(self, surface):

        surface.blit(self.elevator_background, (self.x_background, self.y_background))

        for i in range(3):
            y = 500 - 80 - i * 130
            x = self.x_door
            surface.blit(self.elevator_interior, (x, y))


    def getElevator_position(self):
        return self.elevator_door_position

    def get_x_door(self):
        return self.x_door

    def check_availability(self, floor):

        if floor < 3:
            if self.elevator_door_position[floor]['state'] == 'opened':
                return True
        else:
            return False

    def get_current_door_state(self, floor):
        if floor < 3:
           return self.elevator_door_position[floor]['state']
