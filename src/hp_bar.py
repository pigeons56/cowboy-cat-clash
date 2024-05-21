import pygame as pg
SCREEN_SIZE = (800,400)

class Hp_Bar():
    def __init__(self,player_num,hp):
        self.__player_num = player_num
        self.__bar_margin_x = 10
        self.__bar_margin_y = 30
        self.__height = 20

        self.update_bar(hp)
    
    @property
    def bar(self):
        return self.__bar
    
    def update_bar(self,hp):
        self.__hp = hp
        
        if self.__player_num == 1:
            self.__bar = pg.Rect(self.__bar_margin_x,self.__bar_margin_y,self.__hp,self.__height)
        else:
            self.__bar = pg.Rect(SCREEN_SIZE[0]-self.__bar_margin_x-self.__hp,self.__bar_margin_y,self.__hp,self.__height)