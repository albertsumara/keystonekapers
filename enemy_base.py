from abc import ABC, abstractmethod

class EnemyBase(ABC):
    def __init__(self, section, floor):
        self.section = section
        self.x = -10
        self.y = -10

        self.floor = floor

        self.width = 10
        self.height = 10

        self.before_floor_height = 110
        self.floor_height = 20


        self.status = "Inactive"
        self.entry_direction = 'left'
        self.section_width = 800

        self.collision_status = "Inactive"
        self.hit_time = 0

        self.side_margin = 10
        self.up_margin = 10
        self.width_hitbox = self.width - 2 * self.side_margin
        self.height_hitbox = self.height - 2 * self.up_margin

    @abstractmethod
    def draw(self, surface):
        pass


    @abstractmethod
    def move(self):
        pass

    def reset_position_if_needed(self):
        return
    @abstractmethod
    def set_y(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    def set_entry_direction(self, direction):
        self.entry_direction = direction

    def get_collision_rect(self):
        x_hitbox, y_hitbox = self.x + self.side_margin, self.y + self.up_margin
        return (x_hitbox, y_hitbox , self.width_hitbox , self.height_hitbox)


