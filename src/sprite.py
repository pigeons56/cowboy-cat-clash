import pygame as pg

class Sprite():
    def __init__(self, left_x, width,
                 left_y, height, 
                 path):
        self.path = path
        self.left_x = left_x
        self.right_x = self.left_x+width
        self.left_y = left_y
        self.right_y = self.left_y+height
        self.image = pg.image.load(self.path)

class Button(Sprite):
    def __init__(self, name, left_x, width,
                 left_y, height, 
                 path, clicked_path):
        super().__init__(left_x,width,left_y,height,path)
        self.clicked_path = clicked_path
        self.clicked=False
        self.name = name

    def is_clicked(self, pointer_x, pointer_y):
        if (self.left_x <= pointer_x and pointer_x <= self.right_x
            and self.left_y <= pointer_y and pointer_y <= self.right_y):
            return True
        else:
            return False 
