import pygame as pg
from animation import *
from hurtbox import *
from fighter_exceptions import *

FIGHTERS = ("doodles","bowie","venturi")
NUM_OF_FIGHTERS = len(FIGHTERS)
SCREEN_SIZE = (800,400)

class Fighter():
    def __init__(self, name, 
                 path, 
                 controls=None, 
                 stage_y = 0, 
                 direction="R", 
                 movespeed=1,
                 x=0,
                 y=0, 
                 jump_height=0,
                 width=100,
                 height=100,
                 light_dmg=10,
                 heavy_dmg=10):
        """
        Initialize a Fighter object.

        Parameters:
            name (str): Name of fighter.
            path (str): Path to all of this fighter's image files
            controls (dict): Player 1 or 2 control scheme for this fighter
            stage_y (int): y-value of stage for the fighter to stand on
            direction (str): Direction of fighter
            movespeed (int): How far in the x-direction fighter can move each frame
            x (int): Fighter's x position
            y (int): Fighter's y position
            jump_height (int): How far in the y-direction fighter can move each frame
            width (int): Width of fighter's image.
            height (int): Height of fighter's image.
            light_dmg (int): Damage of light attack.
            heavy_dmg (int): Damage of heavy attack.
        """
        self.path = path
        self.name = name
        
        if self.name != "placeholder":
            self._movespeed = movespeed
            self._stage_y = stage_y
            self._min_y = stage_y #The lowest y-value the fighter can reach
            self._x=x
            self._y=y
            self._width = width
            self._height = height
            self._path = path
           
            #Counting jumping
            self._jump_height = jump_height
            self._jump_count = 0
            self._is_jump = False
            
            #Checks to prevent movement when certain actions are executed
            self._can_move_ground = True
            self._can_move_sky = True
            self._can_jump = True
            self._can_animate = True
            self._can_attack = True
            self._can_take_dmg = True
            self._attack_state = None

            self._controls = controls
            self._hp = 250
            self._heavy_dmg = heavy_dmg
            self._light_dmg = light_dmg

            self._animation = Animation(self._width,self._height,self._path, direction)
    
    @property
    def hp(self):
        return self._hp

    @property
    def light_dmg(self):
        return self._light_dmg
    
    @property
    def heavy_dmg(self):
        return self._heavy_dmg

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
    def min_y(self):
        return self._min_y
    
    @min_y.setter
    def min_y(self, min_y):
        self._min_y = min_y

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
    def stage_y(self):
        return self._stage_y
    
    def update_hurtbox(self):
        """
        Update fighter's hurtbox to current x,y position.
        """
        self._animation.hurtbox.set_size(self._x,self._y,self._width,self._height)

    def take_dmg(self,other_fighter):
        """
        Fighter loses HP if their hurtbox collides with other fighter's hitbox.

        Parameters:
            other_fighter (Fighter object): Fighter that is not this one.
        """
        if other_fighter.animation.hitbox.is_hit(self._animation.hurtbox) and other_fighter.animation.hitbox.active:
            if other_fighter.attack_state == "light_attack":
                if self._can_take_dmg: self._hp -= other_fighter.light_dmg
                self.knockback(self._animation.direction,2)
            elif other_fighter.attack_state == "heavy_attack":
                if self._can_take_dmg: self._hp -= other_fighter.heavy_dmg
                self.knockback(self._animation.direction,4)
            
            #Preventing action when hit
            self._attack_state = None
            self._can_jump = False
            self._can_move_ground = False
            self._can_move_sky = False
            self._can_animate = False
            self._can_take_dmg = False
            self.animation.reset_count()

        elif not self._can_take_dmg:
            #Allowing action after hit
            self._can_jump = True
            self._can_move_ground = True
            self._can_move_sky = True
            self._can_animate = True
            self._can_take_dmg = True

    def knockback(self,direction,strength):
        """
        Push fighter backwards from the other fighter after getting hit.

        Parameters:
            direction (str): Direction the fighter is facing.
            strength (int): Change in x-value during knockback
        """
        if direction == "R":
            self._x -= strength
        else:
            self._x += strength 
        self.update_hurtbox()

    def attack(self,keys):
        """
        Fighter performs attack when correct keys are pressed.

        Parameters:
            keys (lists(bools)): State of all keys (True is pressed).
        """
        if self._can_attack:
            if keys[self._controls["light_attack"]]:
                self._attack_state="light_attack"
            
            elif keys[self._controls["heavy_attack"]]:
                self._attack_state="heavy_attack"
            
            #If attack keys are pressed, limit movement during attack animation
            if self._attack_state != None:   
                self._can_jump = True
                self._can_move_ground = False
                self._can_move_sky = True
                self._can_animate = False
                self._can_attack=False
                self._animation.reset_count()
        else:
            #Play attack animation
            self._attack_state = self._animation.play_attack(self._attack_state)

            #When attack animation is done, allow movement again
            if self._attack_state == None:
                self._can_attack = True 
                self._can_jump = True
                self._can_move_ground = True
                self._can_move_sky = True
                self._can_animate = True

    def play_move_directional(self, move_direction):
        """
        Play move forward or backward animation depending on fighter's movement direction.

        Parameters:
            move_direction (str): Direction the fighter is moving in.
        """
        img_direction = self._animation.direction
        self.update_hurtbox()

        if img_direction == move_direction:
            self._animation.play_move_forward()
        else:
            self._animation.play_move_backward()

    def jump(self,keys):
        """
        Fighter jumps when correct keys are pressed.

        Parameters:
            keys (lists(bools)): State of all keys (True is pressed).
        """
        #Check if keys are pressed, jump movement is allowed, and player is not already jumping
        if keys[self._controls["up"]] and not self._is_jump and self._y == self._min_y and self._can_jump:
            self._is_jump = True
        if self._is_jump:
            if self._can_animate: 
                self._animation.play_jump()
            if self._jump_count < 45: #Go upward
                self.update_hurtbox()
                self._y -= self._jump_height
                self._jump_count+=1
            else: #Stop going upward (allows falling)
                self._jump_count = 0
                self._is_jump = False

    def fall(self):
        """
        Bring the fighter back down to the ground after jumping.
        """
        if not self._is_jump and self._y < self._min_y:
            self.update_hurtbox()
            self._y += self._jump_height

    def is_input(self, keys):
        """
        Check if this player had any inputs.

        Returns:
            bool: True if player had an input, false if not.
        """
        for i in list(self._controls.values()):
            if keys[i]:
                return True
        
        return False

    def check_min_y(self, other_fighter):
        """
        Check which y-value this fighter should land on as ground.
        """
        #Land on the other fighter's head
        if self._y < other_fighter.y and (self._x + self._animation.width >= other_fighter.x and other_fighter.x + other_fighter.animation.width >= self._x):
            self._min_y = other_fighter.y - other_fighter.animation.height
        else: #Otherwise land on the stage
            self._min_y = self._stage_y

    def move(self,keys, other_fighter):
        """
        Move the fighter when correct keys are pressed.

        Parameters:
            keys (lists(bools)): State of all keys (True is pressed).
            other_fighter (Fighter object): Fighter other than this one.
        """
        tried_move = False
        
        #Play idle when no keys are pressed and animation is allowed (not in a jump or attack)
        if not self.is_input(keys) and self._can_animate and self._can_take_dmg:
            self._animation.play_idle()
        
        #Try moving only if allowed
        elif self.can_move_ground or (self.can_move_sky and self._y != self._min_y):
            if keys[self._controls["R"]]:
                move_direction = "R"
                tried_move = True
                if self.check_fighter_collision(other_fighter,move_direction,self._movespeed):
                    self._x+=self._movespeed
            
            elif keys[self._controls["L"]]:
                move_direction = "L"
                tried_move = True
                if self.check_fighter_collision(other_fighter,move_direction,self._movespeed):
                    self._x-=self._movespeed
            
            if tried_move and self._can_animate: 
                #Move animation still plays if keys are pressed, even if x-value did not change
                self.play_move_directional(move_direction)
     
    def check_fighter_collision(self, other_fighter, move_direction,dist_change):
        """
        Checks if fighters are colliding with each other.

        Parameters:
            other_fighter (Fighter object): Fighter other than this one.
            move_direction (str): Direction this fighter is trying to move in.
            dist_change (int): Attempted future movement (that may lead to collision)
        
        Returns:
            bool: True if not collided
        """
        img_direction = self._animation.direction

        #Fighters will never collide if moving away from each other
        if move_direction != img_direction:
            return True
        
        #Checking that x-values don't overlap
        if move_direction == "R" and self._x + dist_change + self._animation.width <= other_fighter.x:
            return True
        elif move_direction == "L" and self._x - dist_change >= other_fighter.x + other_fighter.animation.width:
            return True
        
        #Checking that y-values don't overlap; allows jumping over each other
        if self._y + self._animation.height -10 <= other_fighter.y or self._y >= other_fighter.y + other_fighter.animation.height:
            return True           
        
        return False
    
    def check_bounds(self):
        """
        Makes sure that the fighter stays within screen bounds.
        """
        try:
            if self.can_move():
                if self._x < 0:
                    raise Out_Of_Left_Bound
                elif self._x + self._width > SCREEN_SIZE[0]:
                    raise Out_Of_Right_Bound
        
        except Out_Of_Right_Bound:
            self._x = 0
            self.update_hurtbox()
        
        except Out_Of_Left_Bound:
            self._x = SCREEN_SIZE[0] - self._width
            self.update_hurtbox()

    def check_can_flip(self):
        """
        Fighter's images can only flip when allowed (not when attacking).

        Returns:
            bool: True if flipping is allowed.
        """
        if self.can_move():
            return True
        else:
            return False
        
    def can_move(self):
        """
        Checks if fighter movement is allowed while on the ground or in the air.

        Returns:
            bool: True if movement is allowed.
        """
        return (self._can_move_ground and self._y == self._min_y) or (self._can_move_sky and self._y != self._min_y)


class Doodles(Fighter):
    def __init__(self, direction, controls, width=70,height=60):
        """
        Initialize Doodles object.

        Parameters:
            direction (str): Direction fighter is facing.
            controls (dict): Player 1 or 2 controls to use.
            width (int): Width of fighter image.
            height (int): Height of fighter image.
        """
        super().__init__(name="doodles",path="./assets/doodles",controls=controls,movespeed=2, 
                         direction = direction,jump_height=2, width=width,height=height,
                         stage_y=270,light_dmg=8,heavy_dmg=25)
        
        self._animation = Doodles_Animation(width,height,self._path, direction)

class Bowie(Fighter):
    def __init__(self, direction, controls, width=60,height=57):
        """
        Initialize Bowie object.

        Parameters:
            direction (str): Direction fighter is facing.
            controls (dict): Player 1 or 2 controls to use.
            width (int): Width of fighter image.
            height (int): Height of fighter image.
        """
        super().__init__(name="bowie",path="./assets/bowie",controls=controls,movespeed=4, 
                         direction = direction,jump_height = 3, width=width,height=height, 
                         stage_y=285,light_dmg=5,heavy_dmg=20)
        
        self._animation = Bowie_Animation(width,height,self._path, direction)

class Venturi(Fighter):
    def __init__(self, direction,controls,width=75,height=60):
        """
        Initialize Venturi object.

        Parameters:
            direction (str): Direction fighter is facing.
            controls (dict): Player 1 or 2 controls to use.
            width (int): Width of fighter image.
            height (int): Height of fighter image.
        """
        super().__init__(name="venturi",path="./assets/venturi",controls=controls,movespeed=6, 
                         direction = direction, jump_height = 4, width=width,height=height, 
                         stage_y=270,light_dmg=3,heavy_dmg=16)
        
        self._animation = Venturi_Animation(width,height,self._path, direction)