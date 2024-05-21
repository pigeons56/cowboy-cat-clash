import pygame as pg
from animation import *
from hurtbox import *

FIGHTERS = ("doodles","bowie","venturi")
NUM_OF_FIGHTERS = 3
SCREEN_SIZE = (800,400)


class Fighter():
    def __init__(self, path, controls=None, ground_y = 0, direction="right", movespeed=1,x=0,y=0, jump_height=0,width=100,height=100):
        self.name = path
        
        if self.name != "placeholder":
            self._movespeed = movespeed
            self._ground_y = ground_y
            self._ground = ground_y
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
            self._hurtbox = Hurtbox(x,width,y,height)
            self._hitbox = Hitbox(0,0,0,0)
            self._animation = Animation(width,height,self._path, direction)
            self._controls = controls

    @property
    def hurtbox(self):
        return self._hurtbox
    
    @hurtbox.setter
    def hurtbox(self, hurtbox):
        self._hurtbox = hurtbox

    @property
    def hitbox(self):
        return self._hitbox
    
    @hitbox.setter
    def hitbox(self, hitbox):
        self._hitbox = hitbox

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

    @property
    def ground_y(self):
        return self._ground_y

    def attack(self,keys):
        if self._can_attack:
            if keys[self._controls["light_attack"]]:
                self._attack_state="light_attack"
            elif keys[self._controls["heavy_attack"]]:
                self._attack_state="heavy_attack"
                
            if self._attack_state != None:   
                self._can_jump = True
                self._can_move_ground = False
                self._can_move_sky = True
                self._can_animate = False
                self._can_attack=False
                self._animation.reset_count()
        else:
            self._attack_state = self._animation.play_attack(self._attack_state)

            if self._attack_state == None:
                self._can_attack = True 
                self._can_jump = True
                self._can_move_ground = True
                self._can_move_sky = True
                self._can_animate = True

    def play_move_directional(self, move_direction):
        img_direction = self._animation.direction

        if img_direction == move_direction:
            self._animation.play_move_forward()
        else:
            self._animation.play_move_backward()

    def jump(self,keys):
        if keys[self._controls["up"]] and not self._is_jump and self._y == self._ground and self._can_jump:
            self._is_jump = True
        if self._is_jump:
            if self._can_animate: 
                self._animation.play_jump()
            if self._jump_count < 45:
                self._y -= self._jump_height
                self._jump_count+=1
            else:    
                self._jump_count = 0
                self._is_jump = False

    def fall(self):
        if not self._is_jump and self._y < self._ground:
            self._y += self._jump_height

    def is_input(self, keys):
        for i in list(self._controls.values()):
            if keys[i]:
                return True
        
        return False

    def check_ground(self, other_fighter):
        if self._y < other_fighter.y and (self._x + self._animation.width >= other_fighter.x and other_fighter.x + other_fighter.animation.width >= self._x):
            self._ground = other_fighter.y - other_fighter.animation.height
        else:
            self._ground = self._ground_y

    def move(self,keys, other_fighter):
            tried_move = False 
            if not self.is_input(keys) and self._can_animate:
                self._animation.play_idle()
            elif self._can_move_ground or (self._can_move_sky and self._y != self._ground):
                if keys[self._controls["right"]]:
                    move_direction = "right"
                    tried_move = True
                    if self.check_can_move(other_fighter,move_direction):
                        self._x+=self._movespeed
                
                elif keys[self._controls["left"]]:
                    move_direction = "left"
                    tried_move = True
                    if self.check_can_move(other_fighter,move_direction):
                        self._x-=self._movespeed
                
                if tried_move and self._can_animate:
                    self.play_move_directional(move_direction)
    
    def check_can_move(self, other_fighter, move_direction):
        return self.check_screen_bounds(move_direction) and self.check_fighter_collision(other_fighter, move_direction)
    
    def check_screen_bounds(self, move_direction):

        if move_direction == "right" and self._x + self._movespeed + self._animation.width > SCREEN_SIZE[0]:
            return False
        elif move_direction == "left" and self._x - self._movespeed < 0:
            return False
        
        return True
    
    def check_fighter_collision(self, other_fighter, move_direction):
        img_direction = self._animation.direction

        if move_direction != img_direction:
            return True
        
        if move_direction == "right" and self._x + self._movespeed + self._animation.width < other_fighter.x:
            return True
        elif move_direction == "left" and self._x - self._movespeed > other_fighter.x + other_fighter.animation.width:
            return True
        
        if self._y + self._animation.height <= other_fighter.y or self._y >= other_fighter.y + other_fighter.animation.height:
            return True           
        
        return False


class Doodles(Fighter):
    def __init__(self, direction, controls, width=70,height=60):
        super().__init__(path="../assets/doodles",controls=controls,movespeed=2, direction = direction,jump_height=2,
                         width=width,height=height,ground_y=270)
        self._animation = Doodles_Animation(width,height,self._path, direction)


class Bowie(Fighter):
    def __init__(self, direction, controls, width=60,height=50):
        super().__init__(path="../assets/bowie",controls=controls,movespeed=4, direction = direction,jump_height = 3,
                         width=width,height=height, ground_y=285)
        self._animation = Bowie_Animation(width,height,self._path, direction)

class Venturi(Fighter):
    def __init__(self, direction,controls,width=75,height=60):
        super().__init__(path="../assets/venturi",controls=controls,movespeed=6, direction = direction, jump_height = 4,
                         width=width,height=height, ground_y=270)
        self._animation = Venturi_Animation(width,height,self._path, direction)
