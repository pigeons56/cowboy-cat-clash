class Hurtbox():
    def __init__(self, left_x, right_x, left_y, right_y):
        self._left_x = left_x
        self._right_x = right_x
        self._left_y = left_y
        self._right_y = right_y
    
    def set_size(self, left_x,left_y,right_x,right_y):
        if self._left_x != left_x:
            self._left_x = left_x +30
        
        if self._left_y != left_y:
            self._left_y = left_y +30

        if self._right_x != right_x:
            self._right_x = right_x -25
        
        if self._right_y != right_y:
            self._right_y = right_y -25
    
    def get_size(self):
        return (self._left_x,self._left_y,self._right_x,self._right_y)

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
            change_left_x = -change_left_x - direction_offset

        return (change_left_x,change_right_x,change_left_y,change_right_y)

    def activate(self, hurtbox, change_left_x,change_right_x,change_left_y,change_right_y):
        if not self.__active:
            self._left_x = hurtbox._left_x + change_left_x
            self._left_y = hurtbox._left_y + change_left_y
            self._right_x = hurtbox._right_x + change_right_x
            self._right_y = hurtbox._right_y + change_right_y

            self.__active = True
    
    def deactivate(self, hurtbox):
        if self.__active:
            self._left_x = hurtbox._left_x
            self._left_y = hurtbox._left_y 
            self._right_x = hurtbox._right_x
            self._right_y = hurtbox._right_y         

            self.__active = False