import pygame as pg
from animation import *
FIGHTERS = ("doodles","bowie","ollie")
NUM_OF_FIGHTERS = 3

class Fighter():
    def __init__(self, path, ground=0, movespeed=1,x=0,y=0, direction = "right", jump_height=0):
        self.name = path
        
        if self.name != "placeholder":
            self.direction = direction
            self.movespeed = movespeed
            self.ground = ground
            self.x=x
            self.y=y
            self.path = path
            self.jump_height = jump_height
            self.jump_count = 0
            self.is_jump = False
            self.animation = Animation(100,self.path, self.direction)


class Doodles(Fighter):
    def __init__(self, direction, ground):
        super().__init__(path="../assets/doodles",movespeed=6, direction = direction,jump_height=5,ground=ground)

class Bowie(Fighter):
    def __init__(self, direction, ground):
        super().__init__(path="../assets/bowie",movespeed=4, direction = direction,jump_height = 5,ground=ground)

class Ollie(Fighter):
    def __init__(self, direction, ground):
        super().__init__(path="../assets/ollie",movespeed=9, direction = direction, jump_height = 5, ground=ground)