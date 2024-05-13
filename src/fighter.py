import pygame as pg
from animation import *
FIGHTERS = ("doodles","bowie","ollie")
NUM_OF_FIGHTERS = 3

class Fighter():
    def __init__(self, path,movespeed=1,x=0,y=0, direction = "right", jump_height=0):
        self.name = path
        
        if self.name != "placeholder":
            self.direction = direction
            self.movespeed = movespeed
            self.x=x
            self.y=y
            self.path = path
            self.jump_height = jump_height
            self.jump_count = 0
            self.is_jump = False
            self.animation = Animation(100,self.path, self.direction)


class Doodles(Fighter):
    def __init__(self, direction):
        super().__init__("../assets/doodles",6, direction = direction,jump_height=5)

class Bowie(Fighter):
    def __init__(self, direction):
        super().__init__("../assets/bowie",4, direction = direction,jump_height = 5)

class Ollie(Fighter):
    def __init__(self, direction):
        super().__init__("../assets/ollie",9, direction = direction, jump_height = 5)