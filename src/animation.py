import pygame as pg
import os

class Animation():
    def __init__(self, path, direction,hurtbox,hitbox):
        """
        Initialize Animation object.

        Parameters:
            path (str): Path to all of fighter's images
            direction (str): Direction fighter is facing
        """
        self._path = path

        #Default to right because images face right by default.
        self._direction = "R"
        
        #Load images (currently facing right)
        self.load_all_images()
        
        #Check if direction should be left, flip if needed
        self.check_direction(direction)

        self._image = self._idle_images[0]
        
        #Initialize hurtbox and hitbox objects
        self._hurtbox = hurtbox
        self._hitbox = hitbox
        
        self.reset_count()
    
    @property
    def image(self):
        return self._image
    
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
            array (list(Pygame Image objects)): Tuple filled with loaded images.
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

    #The following functions are for playing animation. There is a default animation
    #sequence that each fighter can override for a unique sequence.

    def play_jump(self):
        """
        Play jump animation.
        """
        self._image = self._jump_images[0]
    
    def play_idle(self):
        """
        Play idle animation.
        """
        self.animation_player(self._idle_images, (0,20,40))

    #play_attack() has no default b/c each fighter is expected to
    #have unique attacks

    def play_attack(self):
        """
        Play light or heavy attack animation.
        """
        pass

    def play_move_forward(self):
        """
        Play move forward animation.
        """
        self.animation_player(self._move_forward_images, (0,20,40))

    def play_move_backward(self):
        """
        Play move backward animation.
        """
        self.animation_player(self._move_backward_images, (0,20,40))

    def play_victory(self):
        """
        Play victory animation.
        """
        self.animation_player(self._victory_images, (0,20,40))

    def play_defeat(self):
        """
        Play defeat animation.
        """
        self.animation_player(self._defeat_images, (0,20,40), is_loop = False)

    def animation_player(self, images, counts, is_loop = True):
        """
        Change images for animation according to how many counts have passed.

        Parameters:
            images (list(Pygame Image objects)): Loaded images of the specific 
                                                  animation
            counts (tuple(Int)): How long to wait between each animation. Final integer 
                            indicates end of animation. Length is length of images - 1.
            is_loop (boolean): Whether to loop the animation. Default is True.
        """
        for i in range(len(counts)):
            if self._count >= counts[-1]:
                if is_loop: self.reset_count() #Loops the animation
                break
            elif self._count >= counts[i] and self._count < counts[i+1]: 
                if self._image != images[i]:
                    self._image = images[i]
                self._count+=1
    
    def attack_animation_player(self, images, counts,
                                hitbox_activate, hitbox_deactivate,
                                change_left_x,change_right_x,
                                change_left_y,change_right_y,
                                attack_state):
        """
        Does the same thing as animation_player, but updates hitbox

        Parameters:
            images (list(Pygame Image objects)): Loaded images of the specific 
                                                  animation
            counts (tuple(Int)): How long to wait between each animation. Final integer 
                            indicates end of animation. Length is length of images - 1.
            hitbox_activate (Int): Frame hitbox should be activated.
            hitbox_deactivate (Int): Frame hitbox should be deactivated.
        """
        for i in range(len(counts)):
            if self._count >= counts[-1]:
                self._hitbox.deactivate(self._hurtbox) #Make sure hurtbox is deactivated
                self.reset_count() #Loops the animation

                return None #Indicator that the attack is finished
            
            elif self._count >= counts[i] and self._count < counts[i+1]: 
                if i == hitbox_activate:
                    self._hitbox.activate(self._hurtbox,change_left_x,change_right_x,change_left_y,change_right_y)
                elif i == hitbox_deactivate:
                    self._hitbox.deactivate(self._hurtbox)                

                if self._image != images[i]:
                    self._image = images[i]
                self._count+=1

                return attack_state #Attack is still going


class Bowie_Animation(Animation):
    def __init__(self, path, direction,hurtbox,hitbox):
        """
        Initialize Bowie_Animation object.

        Parameters:
            path (str): Path to all of fighter's images
            direction (str): Direction fighter is facing
        """
        super().__init__(path,direction,hurtbox,hitbox)

    def play_attack(self, attack_state):
        if attack_state == "light_attack":

            change_left_x,change_right_x,change_left_y,change_right_y = self._hitbox.set_change_variables(
                50,20,20,-10,self._direction,20)
            
            return self.attack_animation_player(self._light_attack_images, (0,15,50,55,60,75,90,105,120),
                                0, 6,
                                change_left_x,change_right_x,
                                change_left_y,change_right_y,
                                attack_state)

        elif attack_state == "heavy_attack":
            change_left_x,change_right_x,change_left_y,change_right_y = self._hitbox.set_change_variables(
                40,20,0,10,self._direction,20)
            
            return self.attack_animation_player(self._heavy_attack_images, (0,10,20,30,40),
                                2, 3,
                                change_left_x,change_right_x,
                                change_left_y,change_right_y,
                                attack_state)

class Doodles_Animation(Animation):
    def __init__(self, path, direction,hurtbox,hitbox):
        """
        Initialize Doodles_Animation object.

        Parameters:
            path (str): Path to all of fighter's images
            direction (str): Direction fighter is facing
        """
        super().__init__(path,direction,hurtbox,hitbox)

    def play_attack(self, attack_state):
        if attack_state == "light_attack":

            change_left_x,change_right_x,change_left_y,change_right_y = self._hitbox.set_change_variables(
                60,0,30,0,self._direction,30)
            

            return self.attack_animation_player(self._light_attack_images, (0,15),
                                0, 1,
                                change_left_x,change_right_x,
                                change_left_y,change_right_y,
                                attack_state)

        elif attack_state == "heavy_attack":
            change_left_x,change_right_x,change_left_y,change_right_y = self._hitbox.set_change_variables(
                -30,80,10,30,self._direction,-60)

            return self.attack_animation_player(self._heavy_attack_images, (0,10,20,40,50,70),
                                3,4,
                                change_left_x,change_right_x,
                                change_left_y,change_right_y,
                                attack_state)
       

class Venturi_Animation(Animation):
    def __init__(self, path, direction,hurtbox,hitbox):
        """
        Initialize Venturi_Animation object.

        Parameters:
            path (str): Path to all of fighter's images
            direction (str): Direction fighter is facing
        """
        super().__init__(path,direction,hurtbox,hitbox)

    def play_move_forward(self):
        self.animation_player(self._move_forward_images, (0,20))


    def play_move_backward(self):
        self.animation_player(self._move_backward_images, (0,20))


    def play_attack(self, attack_state):
        if attack_state == "light_attack":
            change_left_x,change_right_x,change_left_y,change_right_y = self._hitbox.set_change_variables(
                40,0,40,-20,self._direction,20)
            
            return self.attack_animation_player(self._light_attack_images, (0,15),
                                0, 1,
                                change_left_x,change_right_x,
                                change_left_y,change_right_y,
                                attack_state)

        elif attack_state == "heavy_attack":
            change_left_x,change_right_x,change_left_y,change_right_y = self._hitbox.set_change_variables(
                40,0,-40,80,self._direction,20)
            

            return self.attack_animation_player(self._heavy_attack_images, (0,10,20,30),
                                2,3,
                                change_left_x,change_right_x,
                                change_left_y,change_right_y,
                                attack_state)

    def play_defeat(self):
        self._image = self._defeat_images[0]

