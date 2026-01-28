import pygame

class GameMap:

    def __init__(self):

        self.mini_map = pygame.image.load('minimap/mini_map.png')
        self.face_player = pygame.image.load('minimap/face_mini.png')
        self.face_thief = pygame.image.load('minimap/thief_face.png')

        self.mini_map_height = 100
        self.mini_map_width = 400

        self.face_player_width = 10
        self.face_player_height = 10

        self.x = 200
        self.y = 520

        self.quantity_of_sections = 7
        self.first_floor_on_minimap_y = 63

    def draw(self, surface, player, thief):

        surface.blit(self.mini_map, (self.x, self.y))

        self.draw_object(surface, player, self.face_player)
        self.draw_object(surface, thief, self.face_thief)


    def draw_object(self, surface, object, img):

        #Player drawing on mini map
        x = (self.x + (self.mini_map_width/self.quantity_of_sections) * (object.section-1) +
             (object.x * (self.mini_map_width/self.quantity_of_sections)/800)
             - self.face_player_width/2)
        y = self.y+self.first_floor_on_minimap_y - self.face_player_height - (object.floor*16)

        surface.blit(img, (x, y))


