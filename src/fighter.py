import pygame as pg
from animation import *
FIGHTERS = ("doodles","bowie","venturi")
NUM_OF_FIGHTERS = 3

class Fighter():
    def __init__(self, path, ground=0, direction="right", movespeed=1,x=0,y=0, jump_height=0,width=100,height=100):
        self.name = path
        
        if self.name != "placeholder":
            self._movespeed = movespeed
            self._ground = ground
            self._x=x
            self._y=y
            self._path = path
            self._jump_height = jump_height
            self._jump_count = 0
            self._is_jump = False
            self._can_move_ground = True
            self._can_move_sky = True
            self._can_jump = True
            self._can_animate = True
            self._can_attack = True
            self._attack_state = None
            self._animation = Animation(width,height,self._path, direction)

    @property
    def movespeed(self):
        return self._movespeed
    
    @movespeed.setter
    def movespeed(self, movespeed):
        self._movespeed = movespeed

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, x):
        self._x = x
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, y):
        self._y = y
    
    @property
    def ground(self):
        return self._ground
    
    @ground.setter
    def ground(self, ground):
        self._ground = ground

    @property
    def animation(self):
        return self._animation
    
    @property
    def attack_state(self):
        return self._attack_state

    @attack_state.setter
    def attack_state(self, attack_state):
        self._attack_state = attack_state

    @property
    def can_attack(self):
        return self._can_attack
    
    @can_attack.setter
    def can_attack(self,can_attack):
        self._can_attack = can_attack

    @property
    def can_jump(self):
        return self._can_jump
    
    @can_jump.setter
    def can_jump(self,can_jump):
        self._can_jump = can_jump

    @property
    def can_move_ground(self):
        return self._can_move_ground
    
    @can_move_ground.setter
    def can_move_ground(self,can_move_ground):
        self._can_move_ground = can_move_ground

    @property
    def can_move_sky(self):
        return self._can_move_sky
    
    @can_move_sky.setter
    def can_move_sky(self,can_move_sky):
        self._can_move_sky = can_move_sky

    @property
    def can_animate(self):
        return self._can_animate
    
    @can_move_sky.setter
    def can_animate(self,can_animate):
        self._can_animate = can_animate

    @property
    def is_jump(self):
        return self._is_jump
    
    @is_jump.setter
    def is_jump(self,is_jump):
        self._is_jump = is_jump

    @property
    def jump_count(self):
        return self._jump_count
    
    @jump_count.setter
    def jump_count(self,jump_count):
        self._jump_count = jump_count

    @property
    def jump_height(self):
        return self._jump_height
    
    @jump_height.setter
    def jump_height(self,jump_height):
        self._jump_height = jump_height

class Doodles(Fighter):
    def __init__(self, direction,width=100,height=100):
        super().__init__(path="../assets/doodles",movespeed=6, direction = direction,jump_height=5,width=width,height=height)

class Bowie(Fighter):
    def __init__(self, direction,width=60,height=50):
        super().__init__(path="../assets/bowie",movespeed=4, direction = direction,jump_height = 5,
                         width=width,height=height)
        self._animation = Bowie_Animation(width,height,self._path, direction)

class Venturi(Fighter):
    def __init__(self, direction,width=100,height=100):
        super().__init__(path="../assets/venturi",movespeed=9, direction = direction, jump_height = 5,
                         width=width,height=height)