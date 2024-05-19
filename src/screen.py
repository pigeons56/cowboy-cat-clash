import pygame as pg
import sys
from sprite import *
from fighter import *
from animation import *
from music import *
from random import choice

PLAYER1_CONTROLS = {"up": pg.K_w,
                     "down": pg.K_s,
                     "left": pg.K_a,
                     "right": pg.K_d,
                     "heavy_attack": pg.K_q,
                     "light_attack": pg.K_e}
PLAYER2_CONTROLS = {"up": pg.K_UP,
                     "down": pg.K_DOWN,
                     "left": pg.K_LEFT,
                     "right": pg.K_RIGHT,
                     "heavy_attack": pg.K_RSHIFT,
                     "light_attack": pg.K_RETURN}

GROUND_Y = 285

SCREEN_SIZE = (800,400)

class Screen():
    def __init__(self, background_path,
                 screen_size=SCREEN_SIZE):
        self._background = pg.image.load(background_path)
        self._screen = pg.display.set_mode(screen_size)
        self._running = False
        self._clock = pg.time.Clock()

    def check_quit(self, event):
        if event.type == pg.QUIT:
            sys.exit()

    def check_events(self, event):
        pass

    def loop_functions(self):
        pass

    def end_loop_functions(self):
        pass

    def check_button_hover(self,button):
        mouse_x,mouse_y = pg.mouse.get_pos()
        if button.is_clicked(mouse_x,mouse_y):
            button.clicked = True
            button.image = pg.image.load(button.clicked_path)
        else:
            button.clicked = False
            button.image = pg.image.load(button.path)


    def loop(self):
        self._running = True
        while self._running:
            self._screen.blit(self._background,(0,0))
            self.loop_functions()

            for event in pg.event.get():
                self.check_quit(event)
                self.check_events(event)

            pg.display.update()
            self._clock.tick(60)
        Music().stop()
        self.end_loop_functions()

class Battle_Screen(Screen):
    def __init__(self,player1,player2):
        super().__init__("../assets/backgrounds/battle_background.png")
        
        self.__player1_fighter = player1
        self.__player1_fighter.x = 0
        self.__player1_fighter.y = GROUND_Y
        self.__player1_fighter.ground = GROUND_Y
        
        self.__player2_fighter = player2
        self.__player2_fighter.x = 700
        self.__player2_fighter.y = GROUND_Y
        self.__player1_fighter.ground = GROUND_Y

        self.__music_list = ("ash_and_dust.mp3","riding_solo.mp3","the_outlaw_arrives.mp3",
                           "western_adventures.mp3","western_cowboy_ride.mp3",
                           "western.mp3")

    def blit_fighters(self):
        self._screen.blit(self.__player1_fighter.animation.image,(self.__player1_fighter.x,self.__player1_fighter.y))
        self._screen.blit(self.__player2_fighter.animation.image,(self.__player2_fighter.x,self.__player2_fighter.y))

    def check_events(self, event):
        pass

    def check_keys(self):
        keys = pg.key.get_pressed()
        self.check_all_fighter_inputs(keys,self.__player1_fighter,self.__player2_fighter,1,PLAYER1_CONTROLS)
        self.check_all_fighter_inputs(keys,self.__player2_fighter,self.__player1_fighter,2,PLAYER2_CONTROLS)

    def check_all_fighter_inputs(self,keys,this_fighter,other_fighter,fighter_num,player_controls):
        self.move_fighters(keys,this_fighter,other_fighter,fighter_num,player_controls)
        self.jump_fighters(keys, this_fighter, player_controls)
        self.set_fighter_ground(this_fighter, other_fighter)
        self.fall_fighters(this_fighter)
        self.attack_fighters(keys,this_fighter,player_controls)

    def attack_fighters(self,keys,this_fighter,player_controls):
        if this_fighter.attack_state == None and this_fighter.can_attack:
            if keys[player_controls["light_attack"]]:
                this_fighter.attack_state="light_attack"
            elif keys[player_controls["heavy_attack"]]:
                this_fighter.attack_state="heavy_attack"
            else:
                this_fighter.can_jump = True
                this_fighter.can_move_ground = True
                this_fighter.can_move_sky = True
                this_fighter.can_animate = True
                
            if this_fighter.attack_state != None:           
                this_fighter.can_jump = True
                this_fighter.can_move_ground = False
                this_fighter.can_move_sky = True
                this_fighter.can_animate = False
                this_fighter.animation.reset_count()
        else:
            this_fighter.attack_state = this_fighter.animation.play_attack(this_fighter.attack_state) 



    def is_input(self, player_num, keys):
        if player_num == 1: controls = list(PLAYER1_CONTROLS.values())
        else: controls = list(PLAYER2_CONTROLS.values())

        for i in list(controls):
            if keys[i]:
                return True
        
        return False
    
    def play_fighter_move(self, this_fighter, move_direction):
        img_direction = this_fighter.animation.direction

        if img_direction == move_direction:
            this_fighter.animation.play_move_forward()
        else:
            this_fighter.animation.play_move_backward()
    
    def jump_fighters(self,keys, this_fighter, player_controls):
        if keys[player_controls["up"]] and not this_fighter.is_jump and this_fighter.y == this_fighter.ground and this_fighter.can_jump:
            this_fighter.is_jump = True
        if this_fighter.is_jump:
            if this_fighter.can_animate: 
                this_fighter.animation.play_jump()
            if this_fighter.jump_count < 45:
                this_fighter.y -= this_fighter.jump_height
                this_fighter.jump_count+=1
            else:    
                this_fighter.jump_count = 0
                this_fighter.is_jump = False

    def fall_fighters(self, this_fighter):
        if not this_fighter.is_jump and this_fighter.y < this_fighter.ground:
            this_fighter.y += this_fighter.jump_height
    
    def set_fighter_ground(self, this_fighter, other_fighter):
        if this_fighter.y < other_fighter.y and (this_fighter.x + this_fighter.animation.width >= other_fighter.x and other_fighter.x + other_fighter.animation.width >= this_fighter.x):
            this_fighter.ground = other_fighter.y - other_fighter.animation.height
        else:
            this_fighter.ground = GROUND_Y

    def move_fighters(self,keys, this_fighter, other_fighter, fighter_num, player_controls):
        tried_move = False 
        if not self.is_input(fighter_num,keys) and this_fighter.can_animate:
            this_fighter.animation.play_idle()
        elif this_fighter.can_move_ground or (this_fighter.can_move_sky and this_fighter.y != this_fighter.ground):
            if keys[player_controls["right"]]:
                move_direction = "right"
                tried_move = True
                if self.can_fighter_move(this_fighter,other_fighter,move_direction):
                    this_fighter.x+=this_fighter.movespeed
            
            elif keys[player_controls["left"]]:
                move_direction = "left"
                tried_move = True
                if self.can_fighter_move(this_fighter,other_fighter,move_direction):
                    this_fighter.x-=this_fighter.movespeed
            
            if tried_move and this_fighter.can_animate:
                self.play_fighter_move(this_fighter, move_direction)
    
    def can_fighter_move(self, this_fighter, other_fighter, move_direction):
        return self.check_screen_bounds(this_fighter,move_direction) and self.check_fighter_collision(this_fighter, other_fighter, move_direction)
    
    def check_screen_bounds(self, this_fighter,move_direction):

        if move_direction == "right" and this_fighter.x + this_fighter.movespeed + this_fighter.animation.width > SCREEN_SIZE[0]:
            return False
        elif move_direction == "left" and this_fighter.x - this_fighter.movespeed < 0:
            return False
        
        return True
    
    def check_fighter_collision(self, this_fighter, other_fighter, move_direction):
        img_direction = this_fighter.animation.direction

        if move_direction != img_direction:
            return True
        
        if move_direction == "right" and this_fighter.x + this_fighter.movespeed + this_fighter.animation.width < other_fighter.x:
            return True
        elif move_direction == "left" and this_fighter.x - this_fighter.movespeed > other_fighter.x + other_fighter.animation.width:
            return True
        
        if this_fighter.y + this_fighter.animation.height <= other_fighter.y or this_fighter.y >= other_fighter.y + other_fighter.animation.height:
            return True           
        
        return False

    def check_fighter_x(self):
        if self.__player1_fighter.x > self.__player2_fighter.x:
            self.__player1_fighter.animation.check_direction("left")
            self.__player2_fighter.animation.check_direction("right")
        else:
            self.__player1_fighter.animation.check_direction("right")
            self.__player2_fighter.animation.check_direction("left")

    def loop_functions(self):
        self.blit_fighters()     
        self.check_fighter_x()
        self.check_keys()
        Music().load_and_continue_play(choice(self.__music_list))
    


class Controls_Screen(Screen):
    def __init__(self):
        self.__controls_title = Sprite(180, 440, 5, 100, "../assets/text/controls_title.png") 
        super().__init__("../assets/backgrounds/main_background.png")
        Music().load_and_play_infinite("wild_west_background.mp3")

    def loop_functions(self):
        self._screen.blit(self.__controls_title.image,(self.__controls_title.left_x,self.__controls_title.left_y))

    def end_loop_functions(self):
        Start_Screen().loop()

    def check_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self._running = False

class Credits_Screen(Screen):
    def __init__(self):
        super().__init__("../assets/backgrounds/main_background.png")
        self.__credits_title = Sprite(210, 380, 5, 100, "../assets/text/credits_title.png") 
        Music().load_and_play_infinite("wild_west_background.mp3")

    def loop_functions(self):
        self._screen.blit(self.__credits_title.image,(self.__credits_title.left_x,self.__credits_title.left_y))

    def end_loop_functions(self):
        Start_Screen().loop()

    def check_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self._running = False

class Select_Screen(Screen):
    def __init__(self):
        super().__init__("../assets/backgrounds/main_background.png")
        self.__ready_button = Button("ready_button",200,200,300,100,"../assets/buttons/ready_button_unclicked.png",
                              "../assets/buttons/ready_button_clicked.png")
        self.__player1_fighter=Fighter("placeholder")
        self.__player2_fighter=Fighter("placeholder")
        self.load_portraits()

        Music().load_and_play_infinite("rough_n_ready.mp3")

    def load_portraits(self):
        self.__portraits=[None] * NUM_OF_FIGHTERS
        x,y=100,100
        for i in range(NUM_OF_FIGHTERS):
            self.__portraits[i] = Button(FIGHTERS[i],x,50,y,50,f"../assets/{FIGHTERS[i]}/portrait/{FIGHTERS[i]}_portrait_unclicked.png",
                                       f"../assets/{FIGHTERS[i]}/portrait/{FIGHTERS[i]}_portrait_clicked.png")
            x+=50

    def blit_idles(self):
        if self.__player1_fighter.name != "placeholder":
            self.__player1_fighter.animation.play_idle()
            self._screen.blit(self.__player1_fighter.animation.image,(0,200))
        if self.__player2_fighter.name != "placeholder":
            self.__player2_fighter.animation.play_idle()
            self._screen.blit(self.__player2_fighter.animation.image,(600,200))

    def set_this_fighter(self,fighter,this_fighter_var, direction):
        if this_fighter_var.name != fighter:
            if fighter == "doodles":
                this_fighter_var = Doodles(direction=direction)
            elif fighter == "bowie":
                this_fighter_var = Bowie(direction=direction)
            elif fighter == "ollie":
                this_fighter_var = Ollie(direction=direction)
            
        return this_fighter_var

    def blit_portraits(self):
        for i in self.__portraits:
            self._screen.blit(i.image,(i.left_x,i.left_y))

    def blit_ready_button(self):
        if self.__player1_fighter.name != "placeholder" and self.__player2_fighter.name != "placeholder":
            self._screen.blit(self.__ready_button.image,(self.__ready_button.left_x,self.__ready_button.left_y))

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            for i in self.__portraits:
                if i.clicked:
                    if event.button == 1:
                        self.__player1_fighter = self.set_this_fighter(i.name,self.__player1_fighter, "right")
                    elif event.button == 3:
                        self.__player2_fighter = self.set_this_fighter(i.name,self.__player2_fighter, "left")
            if self.__ready_button.is_clicked(event.pos[0],event.pos[1]) and self.__player1_fighter.name != "placeholder" and self.__player2_fighter.name != "placeholder":
                self._running = False
    
    def end_loop_functions(self):
        Battle_Screen(self.__player1_fighter,self.__player2_fighter).loop()


    def loop_functions(self):
        self.blit_portraits()
        for portrait in self.__portraits:
            self.check_button_hover(portrait)
        self.check_button_hover(self.__ready_button)
        self.blit_idles()
        self.blit_ready_button()

class Start_Screen(Screen):
    def __init__(self):
        self.__start_button = Button("start_button",310, 170, 200, 60, 
                              "../assets/buttons/start_button_unclicked.png",
                              "../assets/buttons/start_button_clicked.png")
        self.__controls_button = Button("controls_button",265, 270, 265, 60, 
                              "../assets/buttons/controls_button_unclicked.png",
                              "../assets/buttons/controls_button_clicked.png")
        self.__credits_button = Button("credits_button",290, 225, 330, 60, 
                              "../assets/buttons/credits_button_unclicked.png",
                              "../assets/buttons/credits_button_clicked.png")
        
        self.__buttons = (self.__start_button,self.__controls_button,self.__credits_button)
        
        self.__start_title = Sprite(200, 400, 5, 180, "../assets/text/start_title.png")
        self.__start_button_extra = Sprite(482,35,213,35,"../assets/extra/start_button_extra.png")
        self.__controls_button_extra = Sprite(222,70,234,80,"../assets/extra/controls_button_extra.png")
        self.__credits_button_extra = Sprite(510,40,350,35,"../assets/extra/credits_button_extra.png")
        
        Music().load_and_play_infinite("mexican_cowboys.mp3")

        super().__init__("../assets/backgrounds/main_background.png")
    
    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            for i in self.__buttons:
                if i.clicked:
                    self._running = False
    
    def end_loop_functions(self):
        if self.__start_button.clicked:
            Select_Screen().loop()
        elif self.__credits_button.clicked:
            Credits_Screen().loop()
        elif self.__controls_button.clicked:
            Controls_Screen().loop()

    def loop_functions(self):
        self._screen.blit(self.__start_title.image,(self.__start_title.left_x,self.__start_title.left_y))
        
        self._screen.blit(self.__start_button.image,(self.__start_button.left_x, self.__start_button.left_y))
        self._screen.blit(self.__start_button_extra.image,(self.__start_button_extra.left_x, self.__start_button_extra.left_y))
        
        self._screen.blit(self.__controls_button.image,(self.__controls_button.left_x, self.__controls_button.left_y))
        self._screen.blit(self.__controls_button_extra.image,(self.__controls_button_extra.left_x, self.__controls_button_extra.left_y))
        
        self._screen.blit(self.__credits_button.image,(self.__credits_button.left_x, self.__credits_button.left_y))
        self._screen.blit(self.__credits_button_extra.image,(self.__credits_button_extra.left_x, self.__credits_button_extra.left_y))        
        
        for button in self.__buttons:
            self.check_button_hover(button)