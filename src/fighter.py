import pygame as pg
from animation import *
FIGHTERS = ("doodles","bowie","ollie")
NUM_OF_FIGHTERS = 3

class Fighter():
    def __init__(self, path, ground=0, movespeed=1,x=0,y=0, direction = "right", jump_height=0,width=100,height=100):
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
            self.is_attack = False
            self.attack_duration = 10
            self.attack_count = 0
            self.animation = Animation(width,height,self.path, self.direction)


class Doodles(Fighter):
    def __init__(self, direction):
        super().__init__(path="../assets/doodles",movespeed=6, direction = direction,jump_height=5)

class Bowie(Fighter):
    def __init__(self, direction):
        super().__init__(path="../assets/bowie",movespeed=4, direction = direction,jump_height = 5,
                         width=60,height=50)

class Ollie(Fighter):
    def __init__(self, direction):
        super().__init__(path="../assets/ollie",movespeed=9, direction = direction, jump_height = 5)