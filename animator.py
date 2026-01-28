import pygame

class Animator:

    def __init__(self, frames, frame_duration=15):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame_index = 0
        self.frame_counter = 0

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_duration:
            self.frame_counter = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)

    def draw(self, surface, x, y, flip=False):
        frame = self.frames[self.current_frame_index]
        if flip:
            frame = pygame.transform.flip(frame, True, False)
        surface.blit(frame, (x, y))

    @staticmethod
    def load_frames(sprite_sheet_path, frame_width, frame_height, scale_width, scale_height, num_frames):
        sprite_sheet = pygame.image.load(sprite_sheet_path)
        frames = []
        for i in range(num_frames):
            rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = sprite_sheet.subsurface(rect)
            scaled_frame = pygame.transform.scale(frame, (scale_width, scale_height))
            frames.append(scaled_frame)
        return frames
