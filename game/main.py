import pygame as pg
import sys

SCREEN_SIZE = (800,400)

class Sprite():
    def __init__(self, left_x, right_x,
                 left_y, right_y, 
                 path):
        self.path = path
        self.image = pg.image.load(self.path)
        self.left_x = left_x
        self.right_x = right_x
        self.left_y = left_y
        self.right_y = right_y

class Button(Sprite):
    def __init__(self, left_x, right_x,
                 left_y, right_y, 
                 path, clicked_path):
        super().__init__(left_x,right_x,left_y,right_y,path)
        self.clicked_path = clicked_path

    def is_clicked(self, pointer_x, pointer_y):
        if (self.left_x <= pointer_x and pointer_x <= self.right_x
            and self.left_y <= pointer_y and pointer_y <= self.right_y):
            return True
        else:
            return False 


if __name__ == "__main__":
    #Initialize pygame
    pg.init()
    pg.font.init()