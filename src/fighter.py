import pygame as pg
from animation import *
FIGHTERS = ("doodles","bowie","ollie")
NUM_OF_FIGHTERS = 3

class Fighter():
    def __init__(self, path,movespeed=1,x=0,y=0, direction = "right"):
        self.name = path
        
        if self.name != "placeholder":
            self.direction = direction
            self.movespeed = movespeed
            self.x=x
            self.y=y
            self.path = path
            self.animation = Animation(100,self.path, self.direction)


class Doodles(Fighter):
    def __init__(self, direction):
        super().__init__("../assets/doodles",6, direction = direction)

class Bowie(Fighter):
    def __init__(self, direction):
        super().__init__("../assets/bowie",4, direction = direction)

class Ollie(Fighter):
    def __init__(self, direction):
        super().__init__("../assets/ollie",9, direction = direction)