import pygame as pg
SCREEN_SIZE = (800,400)

class Hp_Bar():
    def __init__(self,player_num,hp):
        """
        Initialize a Hp_Bar object.

        Parameters:
            player_num (int): Player 1 or 2.
            hp (int): Hp of fighter associated with that player.
        """
        self.__player_num = player_num
        self.__bar_margin_x = 10
        self.__bar_margin_y = 30
        self.__height = 20

        self.update_bar(hp)
    
    @property
    def bar(self):
        return self.__bar
    
    def update_bar(self,hp):
        """
        Update Hp bar size according to Hp of fighter.
        """
        if hp <= 0:
            self.__hp = 0
        else:
            self.__hp = hp

        #Player number changes if the bar is on the left or right
        #Pygame Rect object makes it easy to display the Hp bars when needed
        if self.__player_num == 1:
            self.__bar = pg.Rect(self.__bar_margin_x,self.__bar_margin_y,self.__hp,self.__height)
        else:
            self.__bar = pg.Rect(SCREEN_SIZE[0]-self.__bar_margin_x-self.__hp,self.__bar_margin_y,self.__hp,self.__height)