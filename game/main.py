import pygame as pg
import sys

SCREEN_SIZE = (800,400)

class Screen():
    def __init__(self, background_path,
                 screen_size=SCREEN_SIZE):
        self.background = pg.image.load(background_path)
        self.selected = None
        self.screen = pg.display.set_mode(screen_size)
        self.running = False
        self.clock = pg.time.Clock()

    def check_quit(self, event):
        if event.type == pg.QUIT:
            sys.exit()

    def check_events(self, event):
        pass

    def loop_functions(self):
        pass

    def load(self):
        pass

    def loop(self):
        self.running = True
        while self.running:
            self.screen.blit(self.background,(0,0))
            self.loop_functions()

            for event in pg.event.get():
                self.check_quit(event)
                self.check_events(event)

            pg.display.update()
            self.clock.tick(60)

class Controls_Screen(Screen):
    def __init__(self):
        super().__init__("../assets/backgrounds/controls_screen_background.png")
    
    def check_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.running = False
                start_screen.loop()

class Credits_Screen(Screen):
    def __init__(self):
        super().__init__("../assets/backgrounds/credits_screen_background.png")
    
    def check_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.running = False
                start_screen.loop()

class Select_Screen(Screen):
    def __init__(self):
        super().__init__("../assets/backgrounds/select_screen_background.png")
    
    def check_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.running = False
                start_screen.loop()

class Start_Screen(Screen):
    def __init__(self):
        self.start_button = Button(100, 200, 50, 100, 
                              "../assets/buttons/start_button_unclicked.png",
                              "../assets/buttons/start_button_clicked.png")
        self.controls_button = Button(100, 200, 100, 150, 
                              "../assets/buttons/controls_button_unclicked.png",
                              "../assets/buttons/controls_button_clicked.png")
        self.credits_button = Button(100, 200, 150, 200, 
                              "../assets/buttons/credits_button_unclicked.png",
                              "../assets/buttons/credits_button_clicked.png")
        
        self.title = Sprite(100, 300, 200, 100, "../assets/text/title.png") 

        super().__init__("../assets/backgrounds/start_screen_background.png")
    
    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.start_button.is_clicked(event.pos[0],event.pos[1]):
                self.running = False
                select_screen.loop()
            elif self.controls_button.is_clicked(event.pos[0],event.pos[1]):
                self.running = False
                controls_screen.loop()        
            elif self.credits_button.is_clicked(event.pos[0],event.pos[1]):
                self.running = False
                credits_screen.loop()        

    def load(self):
        pass

    def loop_functions(self):
        self.screen.blit(self.title.image,(self.title.left_x,self.title.left_y))
        self.screen.blit(self.start_button.image,(self.start_button.left_x, self.start_button.left_y))
        self.screen.blit(self.controls_button.image,(self.controls_button.left_x, self.controls_button.left_y))
        self.screen.blit(self.credits_button.image,(self.credits_button.left_x, self.credits_button.left_y))

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

    start_screen = Start_Screen()
    controls_screen = Controls_Screen()
    credits_screen = Credits_Screen()
    select_screen = Select_Screen()

    start_screen.loop()