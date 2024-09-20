import pygame as pg

class Hurtbox():
    def __init__(self):
        """
        Initialize Hurtbox object.
        """
        self._left_x = 0
        self._right_x = 0
        self._left_y = 0
        self._right_y = 0

        #Pygame rect object used to represent box b/c of built-in collision methods and easy to display
        self._box = pg.Rect(self._left_x,self._left_y,self._right_x,self._right_y)
    
    @property
    def box(self):
        return self._box
    
    def set_size(self, left_x,left_y,right_x,right_y):
        """
        Change size of hurtbox. 

        Parameters:
            left_x (int): Left x-value
            right_x (int): Right x-value (width)
            left_y (int): Left y-value
            right_y (int): Right y-value (height)
        """
        self._left_x = left_x
        self._right_x = right_x
        self._left_y = left_y
        self._right_y = right_y
        self._box.update(left_x+25,left_y+30,right_x-15,right_y-20)
    

class Hitbox(Hurtbox):
    def __init__(self):
        """
        Initialize Hitbox object.
        """
        super().__init__()
        self.__active = False #Whether or not hitbox is on

    @property
    def active(self):
        return self.__active
    
    @active.setter
    def active(self,active):
        self.__active = active
    
    def set_change_variables(self, change_left_x,change_right_x,change_left_y,change_right_y,
                             direction,direction_offset):
        """
        Set how much the size of hitbox will be adjusted relative to hurtbox.

        Parameters:
            change_left_x (int): Change in left x-value.
            change_right_x (int): Change in right x-value (width).
            change_left_y (int): Change in left y-value.
            change_right_y (int): Change in right y-value (height).
            direction (str): Direction of fighter.
            direction_offset (int): Change in left_x when direction is "right."
        """
        if direction == "L":
            change_left_x = -change_left_x + direction_offset

        return (change_left_x,change_right_x,change_left_y,change_right_y)

    def activate(self, hurtbox, change_left_x,change_right_x,change_left_y,change_right_y):
        """
        Set hitbox size and turn active.
        
        Parameters:
            hurtbox (Hurtbox object): Hurtbox of the fighter.
            change_left_x (int): Change in left x-value.
            change_right_x (int): Change in right x-value (width).
            change_left_y (int): Change in left y-value.
            change_right_y (int): Change in right y-value (height).
        """
        self._box.update(hurtbox._left_x + change_left_x, hurtbox._left_y + change_left_y,
                         hurtbox._right_x + change_right_x, hurtbox._right_y + change_right_y)
        
        if not self.__active:
            self.__active = True
    
    def deactivate(self, hurtbox):
        """
        Reset hitbox size to hurtbox's size and turn active false.

        Parameters:
            hurtbox (Hurtbox object): Hurtbox of the fighter.
        """
        if self.__active:
            self._box = hurtbox.box.copy()      
            self.__active = False

    def is_hit(self, hurtbox):
        """
        Check if hitbox collided with other fighter's hurtbox.

        Returns:
            bool: True if hit, false it not hit.
        """
        return self._box.colliderect(hurtbox.box)
