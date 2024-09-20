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
    
    def set_size(self, direction, left_x,left_y,right_x,right_y):
        """
        Change size of hurtbox. 

        Parameters:
            direction (str): Direction the fighter is facing
            left_x (int): Left x-value
            right_x (int): Right x-value (width)
            left_y (int): Left y-value
            right_y (int): Right y-value (height)
        """
        self._left_x = left_x
        self._right_x = right_x
        self._left_y = left_y
        self._right_y = right_y

        if direction == "L":
            self._box.update(2 * left_x - left_x, 2 * left_y - left_y, left_x, left_y)
        elif direction == "R":
            self._box.update(left_x, left_y,right_x, right_y)
    

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

    def activate(self):
        """
        Turn on hitbox.
        """
        if not self.__active:
            self.__active = True
    
    def deactivate(self):
        """
        Turn off hitbox.
        """
        if self.__active:     
            self.__active = False

    def is_hit(self, hurtbox):
        """
        Check if hitbox collided with a hurtbox.

        Parmeters:
            hurtbox (Hurtbox object): Hurtbox to check for collision. Usually the other fighter's hurtbox.
        Returns:
            bool: True if hit, false it not hit.
        """
        return self._box.colliderect(hurtbox.box)
