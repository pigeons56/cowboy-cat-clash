import pygame as pg
import sys

SCREEN_SIZE = (800,400)

class Screen():
    def __init__(self, background_path,
                 screen_size=SCREEN_SIZE):
        self.background = pg.image.load(background_path)
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

    def end_loop_functions(self):
        pass

    def check_button_hover(self,array):
        mouse_x,mouse_y = pg.mouse.get_pos()
        for i in array:
            if i.is_clicked(mouse_x,mouse_y):
                i.clicked = True
                i.image = pg.image.load(i.clicked_path)
            else:
                i.clicked = False
                i.image = pg.image.load(i.path)

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
        self.end_loop_functions()

class Battle_Screen(Screen):
    def __init__(self):
        super().__init__("../assets/backgrounds/battle_screen_background.png")
        self.player1_x = 0
        self.player1_y = 50

        self.player2_x = 350
        self.player2_x = 50
    


class Controls_Screen(Screen):
    def __init__(self):
        super().__init__("../assets/backgrounds/controls_screen_background.png")
    
    def end_loop_functions(self):
        start_screen.loop()

    def check_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.running = False

class Credits_Screen(Screen):
    def __init__(self):
        super().__init__("../assets/backgrounds/credits_screen_background.png")
    
    def end_loop_functions(self):
        start_screen.loop()

    def check_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.running = False

class Select_Screen(Screen):
    def __init__(self):
        super().__init__("../assets/backgrounds/select_screen_background.png")
        self.ready_button = Button("ready_button",200,400,300,400,"../assets/buttons/ready_button_unclicked.png",
                              "../assets/buttons/ready_button_clicked.png")
        self.player1_fighter=Fighter("placeholder")
        self.player2_fighter=Fighter("placeholder")
        self.load_portraits()

    def load_portraits(self):
        self.portraits=[None] * NUM_OF_FIGHTERS
        x,y=100,100
        for i in range(NUM_OF_FIGHTERS):
            self.portraits[i] = Button(FIGHTERS[i],x,x+50,y,y+50,f"../assets/{FIGHTERS[i]}/{FIGHTERS[i]}_portrait_unclicked.png",
                                       f"../assets/{FIGHTERS[i]}/{FIGHTERS[i]}_portrait_clicked.png")
            x+=50

    def blit_idles(self):
        if self.player1_fighter.name != "placeholder":
            self.player1_fighter.flip_assets("right")
            self.player1_fighter.play_idle_animation()
            self.screen.blit(self.player1_fighter.image,(0,200))
        if self.player2_fighter.name != "placeholder":
            self.player2_fighter.flip_assets("left")
            self.player2_fighter.play_idle_animation()
            self.screen.blit(self.player2_fighter.image,(600,200))

    def set_player_fighter(self,fighter,player_fighter_var):
        if player_fighter_var.name != fighter:
            if fighter == "doodles":
                player_fighter_var = Doodles()
            elif fighter == "bowie":
                player_fighter_var = Bowie()
            elif fighter == "ollie":
                player_fighter_var = Ollie()
            
        return player_fighter_var

    def blit_portraits(self):
        for i in self.portraits:
            self.screen.blit(i.image,(i.left_x,i.left_y))

    def blit_ready_button(self):
        if self.player1_fighter.name != "placeholder" and self.player2_fighter.name != "placeholder":
            self.screen.blit(self.ready_button.image,(self.ready_button.left_x,self.ready_button.left_y))

    def check_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            for i in self.portraits:
                if i.clicked:
                    if event.button == 1:
                        self.player1_fighter = self.set_player_fighter(i.name,self.player1_fighter)
                    elif event.button == 3:
                        self.player2_fighter = self.set_player_fighter(i.name,self.player2_fighter)
            if self.ready_button.is_clicked(event.pos[0],event.pos[1]) and self.player1_fighter.name != "placeholder" and self.player2_fighter.name != "placeholder":
                self.running = False
    
    def end_loop_functions(self):
        battle_screen.loop()


    def loop_functions(self):
        self.blit_portraits()
        self.check_button_hover(self.portraits)
        self.check_button_hover([self.ready_button])
        self.blit_idles()
        self.blit_ready_button()

class Start_Screen(Screen):
    def __init__(self):
        self.start_button = Button("start_button",100, 200, 50, 100, 
                              "../assets/buttons/start_button_unclicked.png",
                              "../assets/buttons/start_button_clicked.png")
        self.controls_button = Button("controls_button",100, 200, 100, 150, 
                              "../assets/buttons/controls_button_unclicked.png",
                              "../assets/buttons/controls_button_clicked.png")
        self.credits_button = Button("credits_button",100, 200, 150, 200, 
                              "../assets/buttons/credits_button_unclicked.png",
                              "../assets/buttons/credits_button_clicked.png")
        
        self.buttons = (self.start_button,self.controls_button,self.credits_button)
        
        self.title = Sprite(100, 300, 200, 100, "../assets/text/title.png") 

        super().__init__("../assets/backgrounds/start_screen_background.png")
    
    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            for i in self.buttons:
                if i.clicked:
                    self.running = False
    
    def end_loop_functions(self):
        if self.start_button.clicked:
            select_screen.loop()
        elif self.credits_button.clicked:
            credits_screen.loop()
        elif self.controls_button.clicked:
            controls_screen.loop()

    def loop_functions(self):
        self.screen.blit(self.title.image,(self.title.left_x,self.title.left_y))
        self.screen.blit(self.start_button.image,(self.start_button.left_x, self.start_button.left_y))
        self.screen.blit(self.controls_button.image,(self.controls_button.left_x, self.controls_button.left_y))
        self.screen.blit(self.credits_button.image,(self.credits_button.left_x, self.credits_button.left_y))
        self.check_button_hover(self.buttons)

class Fighter():
    def __init__(self, path):
        self.name = path
        
        if self.name != "placeholder":
            self.direction = "right"
            self.path = path
            self.idle_frames_count = 2
            self.idle_animation_count = 0
            self.load_idle_images()
            self.image = self.idle_frames[0]

    def load_idle_images(self):
        self.idle_frames = [None] * self.idle_frames_count
        for i in range(self.idle_frames_count):
            self.idle_frames[i] = pg.image.load(f"../assets/{self.path}/{self.path}_idle{i}.png")

    def flip_assets(self, direction):
        if direction != self.direction:
            for i in range(self.idle_frames_count):
                self.idle_frames[i] = pg.transform.flip(self.idle_frames[i], True, False)
            self.direction=direction
        
    def play_idle_animation(self):
        if self.idle_animation_count < 20:
            self.image = self.idle_frames[0]
        elif self.idle_animation_count >= 20:
            self.image = self.idle_frames[1]
        if self.idle_animation_count == 40:
            self.idle_animation_count=0
        self.idle_animation_count+=1


class Doodles(Fighter):
    def __init__(self):
        super().__init__("doodles")

class Bowie(Fighter):
    def __init__(self):
        super().__init__("bowie")

class Ollie(Fighter):
    def __init__(self):
        super().__init__("ollie")

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
    def __init__(self, name, left_x, right_x,
                 left_y, right_y, 
                 path, clicked_path):
        super().__init__(left_x,right_x,left_y,right_y,path)
        self.clicked_path = clicked_path
        self.clicked=False
        self.name = name

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

    FIGHTERS = ("doodles","bowie","ollie")
    NUM_OF_FIGHTERS = 3

    start_screen = Start_Screen()
    controls_screen = Controls_Screen()
    credits_screen = Credits_Screen()
    select_screen = Select_Screen()
    battle_screen = Battle_Screen()

    start_screen.loop()