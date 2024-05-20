import pygame as pg

class Sprite():
    def __init__(self, left_x, width,
                 left_y, height, 
                 path):
        self._path = path
        self._left_x = left_x
        self._right_x = self.left_x+width
        self._left_y = left_y
        self._right_y = self.left_y+height
        self._image = pg.image.load(self._path)

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, path):
        self._path = path

    @property
    def left_x(self):
        return self._left_x
    
    @left_x.setter
    def left_x(self,left_x):
        self._left_x = left_x

    @property
    def left_y(self):
        return self._left_y
    
    @left_y.setter
    def left_y(self, left_y):
        self._left_y = left_y
    
    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image
    
class Button(Sprite):
    def __init__(self, name, left_x, width,
                 left_y, height, 
                 path, clicked_path):
        super().__init__(left_x,width,left_y,height,path)
        self.__clicked_path = clicked_path
        self.__clicked=False
        self.__name = name

    @property
    def clicked(self):
        return self.__clicked
    
    @clicked.setter
    def clicked(self, clicked):
        self.__clicked = clicked

    @property
    def clicked_path(self):
        return self.__clicked_path
    
    @clicked_path.setter
    def clicked_path(self, clicked_path):
        self.__clicked_path = clicked_path

    @property
    def name(self):
        return self.__name

    def is_clicked(self, pointer_x, pointer_y):
        if (self._left_x <= pointer_x and pointer_x <= self._right_x
            and self._left_y <= pointer_y and pointer_y <= self._right_y):
            return True
        else:
            return False
