import pygame as pg
import sys
from sprite import *
from fighter import *
from animation import *
from music import *
from hp_bar import *
from random import choice

PLAYER1_CONTROLS = {"up": pg.K_w,
                     "left": pg.K_a,
                     "right": pg.K_d,
                     "heavy_attack": pg.K_q,
                     "light_attack": pg.K_e}

PLAYER2_CONTROLS = {"up": pg.K_UP,
                     "left": pg.K_LEFT,
                     "right": pg.K_RIGHT,
                     "heavy_attack": pg.K_PERIOD,
                     "light_attack": pg.K_SLASH}


class Screen():
    def __init__(self, background_path,
                 screen_size=SCREEN_SIZE):
        """
        Initializes a Screen object.
 
        Parameters:
            background_path (str): Relative path to background image.
            screen_size (tuple(int,int)): Width and height of game screen.
        """
        self._background = pg.image.load(background_path)
        self._screen = pg.display.set_mode(screen_size)
        self._running = True
        self._clock = pg.time.Clock()

    def check_quit(self, event):
        """
        Exit program when user presses the 'X' in the window.
 
        Parameters:
            event (pygame event): User interaction with the window.
        """
        if event.type == pg.QUIT:
            sys.exit()

    def check_events(self, event):
        """
        Check for and react to user interactions with the window.
 
        Parameters:
            event (pygame event): User interaction with the window.
        """
        pass

    def loop_functions(self):
        """
        Code that will be executed within Screen's main game loop.
        """
        pass

    def end_loop_functions(self):
        """
        Code that will be executed after Screen's main game loop exits.
        """
        pass

    def check_button_hover(self,button):
        """
        Check if mouse pointer is currently on a button.
 
        Parameters:
            button (Button object): Clickable Button object.
        """
        mouse_x,mouse_y = pg.mouse.get_pos()
        if button.is_clicked(mouse_x,mouse_y):
            button.clicked = True
            button.image = pg.image.load(button.clicked_path)
        else:
            button.clicked = False
            button.image = pg.image.load(button.path)


    def loop(self):
        """
        Create Screen's main game loop. Anything that happens in this Screen is handled in the loop.
        """
        while self._running:
            self._screen.blit(self._background,(0,0))
            self.loop_functions()

            for event in pg.event.get():
                self.check_quit(event)
                self.check_events(event)

            pg.display.update() #Update visuals displayed on the screen
            self._clock.tick(60) #Limit to 60 FPS
        
        #End of loop calls
        Music().stop()
        self.end_loop_functions()


class Victory_Screen(Screen):
    def __init__(self, victor,loser,victor_num,player1_hp_bar,player2_hp_bar):
        """
        Initialize a Victory_Screen object.
 
        Parameters:
            victor (Fighter object): Fighter who won the match.
            loser (Fighter object): Fighter who lost the match.
            victor_num (int): Player number (1 or 2) of victor.
            player1_hp_bar (Hp_Bar object): HP bar of Player 1 at the end of the match.
            player2_hp_bar (Hp_Bar object): HP bar of Player 2 at the end of the match.
        """
        super().__init__("./assets/backgrounds/battle_background.png")
        self.__victor = victor
        self.__loser = loser
        self.__victor_num = victor_num
        
        self.__player1_hp_bar = player1_hp_bar
        self.__player2_hp_bar = player2_hp_bar
        self.__victor_num = victor_num

        Music().load_and_play_infinite("rolling_hills.mp3")

        self.load_win_title()

    def load_win_title(self):
        """
        Load image file for Win Title (Player __ Wins!) depending on which player won.
        """
        if self.__victor_num == 1:
            self.__win_title = pg.image.load("./assets/text/player1_win_title.png")
        else:
            self.__win_title = pg.image.load("./assets/text/player2_win_title.png")

    def blit_hp_bars(self):
        """
        Display HP bars onto screen.
        """
        pg.draw.rect(self._screen,(219,7,0),self.__player1_hp_bar.bar)
        pg.draw.rect(self._screen,(219,7,0),self.__player2_hp_bar.bar)

    def blit_fighters(self):
        """
        Display fighters onto screen.
        """
        self._screen.blit(self.__victor.animation.image,(self.__victor.x,self.__victor.y))
        self._screen.blit(self.__loser.animation.image,(self.__loser.x,self.__loser.y))

    def check_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.__next_screen = "start"
                self._running = False
            if event.key == pg.K_SPACE:
                self.__next_screen = "battle"
                self._running = False

    def loop_functions(self):
        self.blit_fighters()
        self.blit_hp_bars()

        self.__victor.animation.play_victory()
        self.__loser.animation.play_defeat()
        self._screen.blit(self.__win_title,(0,0))

    def reset_fighter(self,fighter,direction,player_controls):
        """
        Reset fighter for a new match by creating new Fighter object.
 
        Parameters:
            fighter (Fighter object): Fighter to be reset.
            direction (str): Direction fighter is facing.
            player_controls (dict): Control scheme for player 1 or 2.
        
        Returns:
            player (Fighter object): Reset fighter.
        """
        if fighter.name == "bowie":
            player = Bowie(direction,player_controls)
        elif fighter.name == "doodles":
            player = Doodles(direction,player_controls)
        elif fighter.name == "venturi":
            player = Venturi(direction,player_controls)

        return player

    def end_loop_functions(self):
        if self.__next_screen == "start":
            Start_Screen().loop()

        elif self.__next_screen == "battle":
            if self.__victor_num == 1:
                player1 = self.reset_fighter(self.__victor,"right",PLAYER1_CONTROLS)
                player2 = self.reset_fighter(self.__loser,"left",PLAYER2_CONTROLS)
            else:
                player1 = self.reset_fighter(self.__loser,"right",PLAYER1_CONTROLS)
                player2 = self.reset_fighter(self.__victor,"left",PLAYER2_CONTROLS)
            
            Battle_Screen(player1,player2).loop()

    
class Battle_Screen(Screen):
    def __init__(self,player1,player2):
        """
        Initialize a Battle_Screen object.
 
        Parameters:
            player1 (Fighter object): Chosen fighter for player 1.
            player2 (Fighter object): Chosen fighter for player 2.
        """
        super().__init__("./assets/backgrounds/battle_background.png")
        
        self.__player1_fighter = player1
        self.__player1_fighter.x = 0 #Set player 1 to left side of screen
        self.__player1_fighter.y = self.__player1_fighter.ground_y #Make sure player 1 is standing on the stage
        self.__player1_fighter.update_hurtbox() #Update hurtbox to current position
        
        self.__player2_fighter = player2
        self.__player2_fighter.x = 700 #Set player 2 to right side of screen
        self.__player2_fighter.y = self.__player2_fighter.ground_y #Make sure player 1 is standing on the stage
        self.__player2_fighter.update_hurtbox() #Update hurtbox to current position

        self.__music_list = ("ash_and_dust.mp3","riding_solo.mp3","the_outlaw_arrives.mp3",
                           "western_adventures.mp3","western_cowboy_ride.mp3",
                           "western.mp3")
        
        self.load_hp_bars()
    
    def load_hp_bars(self):
        """
        Create HP_Bar objects for both players.
        """
        self.__player1_hp_bar = Hp_Bar(1,self.__player1_fighter.hp)
        self.__player2_hp_bar = Hp_Bar(2,self.__player2_fighter.hp)
    
    def blit_hp_bars(self):
        """
        Update HP_Bar object to current fighters' HPs and display HP_Bar to screen.
        """
        self.__player1_hp_bar.update_bar(self.__player1_fighter.hp)
        pg.draw.rect(self._screen,(219,7,0),self.__player1_hp_bar.bar)
        self.__player2_hp_bar.update_bar(self.__player2_fighter.hp)
        pg.draw.rect(self._screen,(219,7,0),self.__player2_hp_bar.bar)

    def blit_fighters(self):
        """
        Display fighters to screen.
        """
        self._screen.blit(self.__player1_fighter.animation.image,(self.__player1_fighter.x,self.__player1_fighter.y))
        self._screen.blit(self.__player2_fighter.animation.image,(self.__player2_fighter.x,self.__player2_fighter.y))

    def check_keys(self):
        """
        Check inputs for both players.
        """
        keys = pg.key.get_pressed()
        self.check_fighter_inputs(keys,self.__player1_fighter,self.__player2_fighter)
        self.check_fighter_inputs(keys,self.__player2_fighter,self.__player1_fighter)

    def check_fighter_inputs(self,keys,this_fighter,other_fighter):
        """
        Check and react to player inputs.

        Parameters:
            keys (lists(bools)): State of all keys (True is pressed).
            this_fighter (Fighter object): Current fighter whose inputs are being checked.
            other_fighter (Fighter object): Other fighter not being checked.
        """
        this_fighter.move(keys,other_fighter)
        this_fighter.jump(keys)
        this_fighter.check_ground(other_fighter)
        this_fighter.fall()
        this_fighter.attack(keys)
        
    def check_fighter_x(self):
        """
        Compare player 1 and player 2 x-values and flip assets to always face each other.
        """
        player1_can_flip = self.__player1_fighter.check_can_flip()
        player2_can_flip = self.__player2_fighter.check_can_flip()

        if self.__player1_fighter.x > self.__player2_fighter.x:
            if player1_can_flip: self.__player1_fighter.animation.check_direction("left")
            if player2_can_flip: self.__player2_fighter.animation.check_direction("right")
        else:
            if player1_can_flip: self.__player1_fighter.animation.check_direction("right")
            if player2_can_flip: self.__player2_fighter.animation.check_direction("left")
    
    def check_fighter_hit(self):
        """
        Check if fighters were hit.
        """
        self.__player1_fighter.take_dmg(self.__player2_fighter)
        self.__player2_fighter.take_dmg(self.__player1_fighter)
    
    def check_fighter_bounds(self):
        """
        Check if fighters are within screen bounds.
        """
        self.__player1_fighter.check_bounds()
        self.__player2_fighter.check_bounds()

    def check_defeat(self):
        """
        Check if any fighter's HP has reached 0. If so, record victor and loser and end main game loop.
        """
        if self.__player1_fighter.hp <= 0:
            self.__victor = self.__player2_fighter
            self.__loser = self.__player1_fighter
            self.__victor_num = 2
            self._running = False
        elif self.__player2_fighter.hp <= 0:
            self.__victor = self.__player1_fighter
            self.__loser = self.__player2_fighter
            self.__victor_num = 1
            self._running = False

    def loop_functions(self):
        self.check_defeat()
        self.blit_fighters()    
        self.blit_hp_bars() 
        self.check_fighter_x()
        self.check_keys()
        self.check_fighter_hit()
        self.check_fighter_bounds()
        Music().load_and_continue_play(choice(self.__music_list))
    
    def end_loop_functions(self):
        Victory_Screen(self.__victor,self.__loser,self.__victor_num,self.__player1_hp_bar,self.__player2_hp_bar).loop()


class Controls_Screen(Screen):
    def __init__(self):
        """
        Initialize Controls_Screen object.
        """
        self.__controls_title = Sprite(180, 440, 5, 100, "./assets/text/controls_title.png") 
        super().__init__("./assets/backgrounds/controls_background.png")
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
        """
        Initialize Credits_Screen object.
        """
        super().__init__("./assets/backgrounds/credits_background.png")
        self.__credits_title = Sprite(210, 380, 5, 100, "./assets/text/credits_title.png") 
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
        """
        Initialize Select_Screen object.
        """
        super().__init__("./assets/backgrounds/main_background.png")
        self.__select_title = Sprite(0, 800, 0, 132, "./assets/text/select_title.png") 
        self.__ready_button = Button("ready_button",310, 170, 300, 60,"./assets/buttons/start_button_unclicked.png",
                              "./assets/buttons/start_button_clicked.png")
        
        #Placeholder will be replaced by the fighters picked by the players
        self.__player1_fighter=Fighter("placeholder","placeholder")
        self.__player2_fighter=Fighter("placeholder","placeholder")
        
        #Indicator on the fighter portrait of which player picked a fighter
        self.__player1_picked = Sprite(0,75,0,75,"./assets/extra/player1_picked.png")
        self.__player2_picked = Sprite(0,75,0,75,"./assets/extra/player2_picked.png")

        self.load_portraits()

        Music().load_and_play_infinite("rough_n_ready.mp3")

    def load_portraits(self):
        """
        Create a Button object for each fighter portrait.
        """
        self.__portraits=[None] * NUM_OF_FIGHTERS
        x,y=275,100
        portrait_size=75
        for i in range(NUM_OF_FIGHTERS):
            self.__portraits[i] = Button(FIGHTERS[i],x,portrait_size,y,portrait_size,
                                         f"./assets/{FIGHTERS[i]}/portrait/{FIGHTERS[i]}_portrait_unclicked.png",
                                         f"./assets/{FIGHTERS[i]}/portrait/{FIGHTERS[i]}_portrait_clicked.png")
            x+=portrait_size

    def blit_idles(self):
        """
        Display the fighters when chosen by the players.
        """
        if self.__player1_fighter.name != "placeholder":
            self.__player1_fighter.animation.play_idle()
            self._screen.blit(self.__player1_fighter.animation.image,(50,180))
            self._screen.blit(self.__player1_picked.image,(self.__player1_picked.left_x,self.__player1_picked.left_y))

        if self.__player2_fighter.name != "placeholder":
            self.__player2_fighter.animation.play_idle()
            self._screen.blit(self.__player2_fighter.animation.image,(650,180))
            self._screen.blit(self.__player2_picked.image,(self.__player2_picked.left_x,self.__player2_picked.left_y))

    def set_this_fighter(self,fighter,this_fighter_var, direction,player_controls):
        """
        Set the player's fighter according to what portrait was clicked.

        Parameters:
            fighter (str): Name of fighter whose portrait was clicked.
            this_fighter_var (Fighter object): Variable to store new Fighter object.
            direction (str): Direction the fighter is facing.
            player_controls (dict): Player 1 or 2 controls to use for this fighter.
        Returns:
            this_fighter_var (Fighter object): The fighter the player picked.
        """
        if this_fighter_var.name != fighter:
            if fighter == "doodles":
                this_fighter_var = Doodles(direction=direction,controls=player_controls)
            elif fighter == "bowie":
                this_fighter_var = Bowie(direction=direction,controls=player_controls)
            elif fighter == "venturi":
                this_fighter_var = Venturi(direction=direction,controls=player_controls)
            
        return this_fighter_var

    def blit_portraits(self):
        """
        Display portraits to screen.
        """
        for i in self.__portraits:
            self._screen.blit(i.image,(i.left_x,i.left_y))

    def blit_ready_button(self):
        """
        Display the ready button if both fighters are selected.
        """
        if self.__player1_fighter.name != "placeholder" and self.__player2_fighter.name != "placeholder":
            self._screen.blit(self.__ready_button.image,(self.__ready_button.left_x,self.__ready_button.left_y))

    def check_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            for i in self.__portraits:
                if i.clicked:
                    if event.button == 1: #Left click on portrait sets player 1
                        self.__player1_fighter = self.set_this_fighter(i.name,self.__player1_fighter, "right",PLAYER1_CONTROLS)
                        
                        #Setting the player indicator on the portrait
                        self.__player1_picked.left_x = i.left_x-10
                        self.__player1_picked.left_y = i.left_y - 10
                    elif event.button == 3: #Right click on portrait sets player 2
                        self.__player2_fighter = self.set_this_fighter(i.name,self.__player2_fighter, "left",PLAYER2_CONTROLS)
                        
                        #Setting the player indicator on the portrait
                        self.__player2_picked.left_x = i.left_x+10
                        self.__player2_picked.left_y = i.left_y + 20
            
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
        self._screen.blit(self.__select_title.image,(self.__select_title.left_x,self.__select_title.left_y))


class Start_Screen(Screen):
    def __init__(self):
        """
        Initialize Start_Screen object.
        """
        self.__start_button = Button("start_button",310, 170, 200, 60, 
                              "./assets/buttons/start_button_unclicked.png",
                              "./assets/buttons/start_button_clicked.png")
        self.__controls_button = Button("controls_button",265, 270, 265, 60, 
                              "./assets/buttons/controls_button_unclicked.png",
                              "./assets/buttons/controls_button_clicked.png")
        self.__credits_button = Button("credits_button",290, 225, 330, 60, 
                              "./assets/buttons/credits_button_unclicked.png",
                              "./assets/buttons/credits_button_clicked.png")
        
        self.__buttons = (self.__start_button,self.__controls_button,self.__credits_button)
        
        self.__start_title = Sprite(200, 400, 5, 180, "./assets/text/start_title.png")
        
        #The picture decorations next to the buttons
        self.__start_button_extra = Sprite(482,35,213,35,"./assets/extra/start_button_extra.png")
        self.__controls_button_extra = Sprite(222,70,234,80,"./assets/extra/controls_button_extra.png")
        self.__credits_button_extra = Sprite(510,40,350,35,"./assets/extra/credits_button_extra.png")
        
        Music().load_and_play_infinite("mexican_cowboys.mp3")

        super().__init__("./assets/backgrounds/main_background.png")
    
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