import pygame as pg
import os
from hurtbox import *

class Animation():
    def __init__(self, width, height, path, direction):
        """
        Initialize Animation object.

        Parameters:
            width (int): Width of image
            height (int): Height of image
            path (str): Path to all of fighter's images
            direction (str): Direction fighter is facing
        """
        self._width = width
        self._height = height
        self._path = path
        self._direction = direction
        
        self.load_all_images()
        self.check_direction(direction)
        self._image = self._idle_images[0]
        
        #Initialize hurtbox and hitbox objects
        self._hurtbox = Hurtbox(0,0,0,0)
        self._hitbox = Hitbox(0,0,0,0)
        
        self.reset_count()
    
    @property
    def hurtbox(self):
        return self._hurtbox

    @property
    def hitbox(self):
        return self._hitbox

    @property
    def image(self):
        return self._image

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @property
    def direction(self):
        return self._direction
    
    def load_images(self, path, array):
        """
        Load all images in a path.

        Parameters:
            path (str): File location of images for this animation.
            array (list(Pygame Image objects)): Stores loaded images
        
        Returns:
            array (list(Pygame Image objects)): List filled with loaded images.
        """
        for i in os.listdir(path):
            array.append(pg.image.load(f"{path}/{i}"))
        return array
    
    def load_jump_images(self):
        """
        Load images of jump animation.
        """
        self._jump_images = self.load_images(f"{self._path}/jump",[])
    
    def load_idle_images(self):
        """
        Load images of idle animation.
        """
        self._idle_images = self.load_images(f"{self._path}/idle",[])

    def load_light_attack_images(self):
        """
        Load images of light attack animation.
        """
        self._light_attack_images = self.load_images(f"{self._path}/light_attack",[])
    
    def load_heavy_attack_images(self):
        """
        Load images of heavy attack animation.
        """
        self._heavy_attack_images = self.load_images(f"{self._path}/heavy_attack",[])

    def load_move_forward_images(self):
        """
        Load images of move forward animation.
        """
        self._move_forward_images = self.load_images(f"{self._path}/move_forward",[])
    
    def load_move_backward_images(self):
        """
        Load images of move backward animation.
        """
        self._move_backward_images = self.load_images(f"{self._path}/move_backward",[])

    def load_defeat_images(self):
        """
        Load images of defeat animation.
        """
        self._defeat_images = self.load_images(f"{self._path}/defeat",[])

    def load_victory_images(self):
        """
        Load images of victory animation.
        """
        self._victory_images = self.load_images(f"{self._path}/victory",[])
    
    def load_all_images(self):
        """
        Loads all the needed images for all animations.
        """
        self.load_jump_images()
        self.load_idle_images()
        self.load_light_attack_images()
        self.load_heavy_attack_images()
        self.load_move_forward_images()
        self.load_move_backward_images()
        self.load_defeat_images()
        self.load_victory_images()

    def check_direction(self, direction):
        """
        Flip assets if needed to follow fighter's direction.

        Paramters:
            direction (str): Direction fighter is facing.
        """
        if self._direction != direction:
            self._jump_images = self.flip_images(self._jump_images)
            self._idle_images = self.flip_images(self._idle_images)
            self._light_attack_images = self.flip_images(self._light_attack_images)
            self._heavy_attack_images = self.flip_images(self._heavy_attack_images)
            self._move_forward_images = self.flip_images(self._move_forward_images)
            self._move_backward_images = self.flip_images(self._move_backward_images)
            self._victory_images = self.flip_images(self._victory_images)
            self._defeat_images = self.flip_images(self._defeat_images)

            self._direction = direction

    def flip_images(self,array):
        """
        Flip images along y-axis.

        Parameters:
            array (list(Pygame Image objects)): List of images to be flipped.
        
        Returns:
            array (list(Pygame Image objects)): List of flipped images.
        """
        for i in range(len(array)):
            array[i] = pg.transform.flip(array[i], True, False)
        return array
    
    def reset_count(self):
        """
        Reset the animation counter.
        """
        self._count = 0

    def play_jump(self):
        """
        Play jump animation.
        """
        self._image = self._jump_images[0]
    
    def play_idle(self):
        """
        Play idle animation.
        """
        pass

    def play_attack(self):
        """
        Play light or heavy attack animation.
        """

    def play_move_forward(self):
        """
        Play move forward animation.
        """
        pass

    def play_move_backward(self):
        """
        Play move backward animation.
        """
        pass

    def play_victory(self):
        """
        Play victory animation.
        """
        pass

    def play_defeat(self):
        """
        Play defeat animation.
        """
        pass

class Bowie_Animation(Animation):
    def __init__(self, width, height, path, direction):
        """
        Initialize Bowie_Animation object.

        Parameters:
            width (int): Width of image
            height (int): Height of image
            path (str): Path to all of fighter's images
            direction (str): Direction fighter is facing
        """
        super().__init__(width,height,path,direction)

    def play_idle(self):
        #Count keeps track of animation progression
        #Each frame of the animation is displayed for a certain amount of counts
        if self._count < 20: 
            self._image = self._idle_images[0]
            self._count+=1
        elif self._count >= 20:
            self._image = self._idle_images[1]
            self._count+=1
        if self._count >= 40:
            self.reset_count() #Loops the animation

    def play_move_forward(self):
        if self._count < 20:
            self._image = self._move_forward_images[0]
            self._count+=1
        elif self._count >= 20:
            self._image = self._move_forward_images[1]
            self._count+=1
        if self._count >= 40:
            self.reset_count()

    def play_move_backward(self):
        if self._count < 20:
            self._image = self._move_backward_images[0]
            self._count+=1
        elif self._count >= 20:
            self._image = self._move_backward_images[1]
            self._count+=1
        if self._count >= 40:
            self.reset_count()

    def play_attack(self, attack_state):
        if attack_state == "light_attack":

            change_left_x,change_right_x,change_left_y,change_right_y = self._hitbox.set_change_variables(
                50,20,20,-10,self._direction,20)
            
            if self._count < 15:
                self._image = self._light_attack_images[0]
                self._count+=1

                #Hitbox is only active on this frame
                self._hitbox.activate(self._hurtbox,change_left_x,change_right_x,change_left_y,change_right_y)
                
            if self._count >= 15:
                self.reset_count()

                #Hitbox is no longer active
                self._hitbox.deactivate(self._hurtbox)
                
                return None

        elif attack_state == "heavy_attack":
            change_left_x,change_right_x,change_left_y,change_right_y = self._hitbox.set_change_variables(
                40,20,0,10,self._direction,20)
            
            if self._count < 10:
                self._image = self._heavy_attack_images[0]
                self._count+=1
            elif self._count >= 10 and self._count < 20:
                self._image = self._heavy_attack_images[1]
                self._count+=1
            elif self._count >= 20 and self._count < 30:
                self._image = self._heavy_attack_images[2]
                self._count+=1
                self._hitbox.activate(self._hurtbox,change_left_x,change_right_x,change_left_y,change_right_y)
            elif self._count >= 30:
                self._image = self._heavy_attack_images[3]
                self._hitbox.deactivate(self._hurtbox)
                self._count+=1
            if self._count >= 40:
                self.reset_count() 
                return None
                        
        return attack_state   

    def play_victory(self):
        if self._count < 20:
            self._image = self._victory_images[0]
            self._count+=1
        elif self._count >= 20:
            self._image = self._victory_images[1]
            self._count+=1
        if self._count >= 40:
            self.reset_count()

    def play_defeat(self):
        if self._count < 20:
            self._image = self._defeat_images[0]
            self._count+=1
        else:
            self._image = self._defeat_images[1] 
            #No need to loop this animation

class Doodles_Animation(Animation):
    def __init__(self, width, height, path, direction):
        """
        Initialize Doodles_Animation object.

        Parameters:
            width (int): Width of image
            height (int): Height of image
            path (str): Path to all of fighter's images
            direction (str): Direction fighter is facing
        """
        super().__init__(width,height,path,direction)

    def play_idle(self):
        if self._count < 20:
            self._image = self._idle_images[0]
            self._count+=1
        elif self._count >= 20:
            self._image = self._idle_images[1]
            self._count+=1
        if self._count >= 40:
            self.reset_count()

    def play_move_forward(self):
        if self._count < 20:
            self._image = self._move_forward_images[0]
            self._count+=1
        elif self._count >= 20:
            self._image = self._move_forward_images[1]
            self._count+=1
        if self._count >= 40:
            self.reset_count()

    def play_move_backward(self):
        if self._count < 20:
            self._image = self._move_backward_images[0]
            self._count+=1
        elif self._count >= 20:
            self._image = self._move_backward_images[1]
            self._count+=1
        if self._count >= 40:
            self.reset_count()

    def play_attack(self, attack_state):
        if attack_state == "light_attack":

            change_left_x,change_right_x,change_left_y,change_right_y = self._hitbox.set_change_variables(
                60,0,30,0,self._direction,30)
            
            if self._count < 15:
                self._image = self._light_attack_images[0]
                self._count+=1
                self._hitbox.activate(self._hurtbox,change_left_x,change_right_x,change_left_y,change_right_y)

            if self._count >= 15:
                self.reset_count()
                self._hitbox.deactivate(self._hurtbox)

                return None

        elif attack_state == "heavy_attack":
            change_left_x,change_right_x,change_left_y,change_right_y = self._hitbox.set_change_variables(
                -30,80,10,30,self._direction,-60)

            if self._count < 10:
                self._image = self._heavy_attack_images[0]
                self._count+=1
            elif self._count >= 10 and self._count < 20:
                self._image = self._heavy_attack_images[1]
                self._count+=1
            elif self._count >= 20 and self._count < 40:
                self._image = self._heavy_attack_images[2]
                self._count+=1
            elif self._count >= 40 and self._count < 50:
                self._image = self._heavy_attack_images[3]
                self._count+=1
                self._hitbox.activate(self._hurtbox,change_left_x,change_right_x,change_left_y,change_right_y)

            elif self._count >= 50:
                self._image = self._heavy_attack_images[4]
                self._count+=1
                self._hitbox.deactivate(self._hurtbox)

            if self._count >= 70:
                self.reset_count() 
                return None
                        
        return attack_state   

    def play_victory(self):
        if self._count < 20:
            self._image = self._victory_images[0]
            self._count+=1
        elif self._count >= 20:
            self._image = self._victory_images[1]
            self._count+=1
        if self._count >= 40:
            self.reset_count()

    def play_defeat(self):
        if self._count < 20:
            self._image = self._defeat_images[0]
            self._count+=1
        else:
            self._image = self._defeat_images[1]


    

class Venturi_Animation(Animation):
    def __init__(self, width, height, path, direction):
        """
        Initialize Venturi_Animation object.

        Parameters:
            width (int): Width of image
            height (int): Height of image
            path (str): Path to all of fighter's images
            direction (str): Direction fighter is facing
        """
        super().__init__(width,height,path,direction)

    def play_idle(self):
        if self._count < 20:
            self._image = self._idle_images[0]
            self._count+=1
        elif self._count >= 20:
            self._image = self._idle_images[1]
            self._count+=1
        if self._count >= 40:
            self.reset_count()

    def play_move_forward(self):
        if self._count < 20:
            self._image = self._move_forward_images[0]
            self._count+=1
        if self._count >= 20:
            self.reset_count()

    def play_move_backward(self):
        if self._count < 20:
            self._image = self._move_backward_images[0]
            self._count+=1
        if self._count >= 20:
            self.reset_count()

    def play_attack(self, attack_state):
        if attack_state == "light_attack":
            change_left_x,change_right_x,change_left_y,change_right_y = self._hitbox.set_change_variables(
                40,0,40,-20,self._direction,20)
            
            if self._count < 15:
                self._image = self._light_attack_images[0]
                self._count+=1
                self._hitbox.activate(self._hurtbox,change_left_x,change_right_x,change_left_y,change_right_y)

            if self._count >= 15:
                self.reset_count()
                self._hitbox.deactivate(self._hurtbox)

                return None

        elif attack_state == "heavy_attack":
            change_left_x,change_right_x,change_left_y,change_right_y = self._hitbox.set_change_variables(
                40,0,-40,80,self._direction,20)
            
            if self._count < 10:
                self._image = self._heavy_attack_images[0]
                self._count+=1
            elif self._count >= 10 and self._count < 20:
                self._image = self._heavy_attack_images[1]
                self._count+=1
            elif self._count >= 20 and self._count < 30:
                self._image = self._heavy_attack_images[2]
                self._count+=1
                self._hitbox.activate(self._hurtbox,change_left_x,change_right_x,change_left_y,change_right_y)

            if self._count >= 30:
                self.reset_count() 
                self._hitbox.deactivate(self._hurtbox)
                return None
                        
        return attack_state   
    
    def play_victory(self):
        if self._count < 20:
            self._image = self._victory_images[0]
            self._count+=1
        elif self._count >= 20:
            self._image = self._victory_images[1]
            self._count+=1
        if self._count >= 40:
            self.reset_count()

    def play_defeat(self):
        self._image = self._defeat_images[0]

