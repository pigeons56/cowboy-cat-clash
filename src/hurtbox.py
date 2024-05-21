import pygame as pg

class Hurtbox():
    def __init__(self, left_x, right_x, left_y, right_y):
        self._left_x = left_x
        self._right_x = right_x
        self._left_y = left_y
        self._right_y = right_y
        self._box = pg.Rect(self._left_x,self._left_y,self._right_x,self._right_y)
    
    @property
    def box(self):
        return self._box
    
    def set_size(self, left_x,left_y,right_x,right_y):
        self._left_x = left_x
        self._right_x = right_x
        self._left_y = left_y
        self._right_y = right_y
        self._box.update(left_x+25,left_y+30,right_x-15,right_y-20)
    

class Hitbox(Hurtbox):
    def __init__(self, left_x, right_x, left_y, right_y):
        super().__init__(left_x, right_x, left_y, right_y)
        self.__active = False

    @property
    def active(self):
        return self.__active
    
    @active.setter
    def active(self,active):
        self.__active = active
    
    def set_change_variables(self, change_left_x,change_right_x,change_left_y,change_right_y,
                             direction,direction_offset):
        if direction == "left":
            change_left_x = -change_left_x + direction_offset

        return (change_left_x,change_right_x,change_left_y,change_right_y)

    def activate(self, hurtbox, change_left_x,change_right_x,change_left_y,change_right_y):
        self._box.update(hurtbox._left_x + change_left_x, hurtbox._left_y + change_left_y,
                         hurtbox._right_x + change_right_x, hurtbox._right_y + change_right_y)
        if not self.__active:
            self.__active = True
    
    def deactivate(self, hurtbox):
        if self.__active:
            self._box = hurtbox.box.copy()      
            self.__active = False

    def is_hit(self, hurtbox):
        return self._box.colliderect(hurtbox.box)
