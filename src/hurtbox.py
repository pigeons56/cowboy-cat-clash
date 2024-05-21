class Hurtbox():
    def __init__(self, left_x, right_x, left_y, right_y):
        self._left_x = left_x
        self._right_x = right_x
        self._left_y = left_y
        self._right_y = right_y
    
    def update_size(self, left_x,left_y,right_x,right_y):
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
        self.active = False