class Hurtbox():
    def __init__(self, left_x, right_x, left_y, right_y):
        self._left_x = left_x
        self._right_x = right_x
        self._left_y = left_y
        self._right_y = right_y
    
    @property
    def left_x(self):
        return self._left_x
    
    @left_x.setter
    def left_x(self, left_x):
        self._left_x = left_x

    @property
    def right_x(self):
        return self._right_x
    
    @right_x.setter
    def right_x(self, right_x):
        self._right_x = right_x

    @property
    def left_y(self):
        return self._left_y
    
    @left_y.setter
    def left_y(self, left_y):
        self._left_y = left_y

    @property
    def right_y(self):
        return self._right_y
    
    @right_y.setter
    def right_y(self, right_y):
        self._right_y = right_y
    
    def update_size(self, left_x,right_x,left_y,right_y):
        self.left_x(left_x)
        self.left_y(left_y)
        self.right_x(right_x)
        self.right_y(right_y)

class Hitbox(Hurtbox):
    def __init__(self, left_x, right_x, left_y, right_y):
        super().__init__(left_x, right_x, left_y, right_y)
        self.active = False