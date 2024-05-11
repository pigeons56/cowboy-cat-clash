import pygame as pg
FIGHTERS = ("doodles","bowie","ollie")
NUM_OF_FIGHTERS = 3

class Fighter():
    def __init__(self, path):
        self.name = path
        
        if self.name != "placeholder":
            self.direction = "right"
            self.path = path
            self.idle_frames_count = 2
            self.idle_animation_count = 0
            self.load_idle_images()
            self.image = self.idle_frames[0]

    def load_idle_images(self):
        self.idle_frames = [None] * self.idle_frames_count
        for i in range(self.idle_frames_count):
            self.idle_frames[i] = pg.image.load(f"../assets/{self.path}/{self.path}_idle{i}.png")

    def flip_assets(self, direction):
        if direction != self.direction:
            for i in range(self.idle_frames_count):
                self.idle_frames[i] = pg.transform.flip(self.idle_frames[i], True, False)
            self.direction=direction
        
    def play_idle_animation(self):
        if self.idle_animation_count < 20:
            self.image = self.idle_frames[0]
        elif self.idle_animation_count >= 20:
            self.image = self.idle_frames[1]
        if self.idle_animation_count == 40:
            self.idle_animation_count=0
        self.idle_animation_count+=1


class Doodles(Fighter):
    def __init__(self):
        super().__init__("doodles")

class Bowie(Fighter):
    def __init__(self):
        super().__init__("bowie")

class Ollie(Fighter):
    def __init__(self):
        super().__init__("ollie")