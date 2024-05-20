import pygame as pg
import os

class Animation():
    def __init__(self, width, height,
                 path,direction):
        self._width = width
        self._height = height
        self._path = path
        self._direction = "right"
        
        self.load_all_images()
        self.check_direction(direction)
        self._image = self._idle_images[0]
        
        self.reset_count()

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
        for i in os.listdir(path):
            array.append(pg.image.load(f"{path}/{i}"))
        return array
    
    def load_jump_images(self):
        self._jump_images = self.load_images(f"{self._path}/jump",[])
    
    def load_idle_images(self):
        self._idle_images = self.load_images(f"{self._path}/idle",[])

    def load_light_attack_images(self):
        self._light_attack_images = self.load_images(f"{self._path}/light_attack",[])
    
    def load_heavy_attack_images(self):
        self._heavy_attack_images = self.load_images(f"{self._path}/heavy_attack",[])

    def load_block_images(self):
        self._block_images = self.load_images(f"{self._path}/block",[])

    def load_move_forward_images(self):
        self._move_forward_images = self.load_images(f"{self._path}/move_forward",[])
    
    def load_move_backward_images(self):
        self._move_backward_images = self.load_images(f"{self._path}/move_backward",[])

    def load_defeat_images(self):
        self._defeat_images = self.load_images(f"{self._path}/defeat",[])

    def load_victory_images(self):
        self._victory_images = self.load_images(f"{self._path}/victory",[])
    
    def load_all_images(self):
        self.load_jump_images()
        self.load_idle_images()
        self.load_light_attack_images()
        self.load_heavy_attack_images()
        self.load_block_images()
        self.load_move_forward_images()
        self.load_move_backward_images()
        self.load_defeat_images()
        self.load_victory_images()

    def check_direction(self, direction):
        if self._direction != direction:
            self._jump_images = self.flip_images(self._jump_images)
            self._idle_images = self.flip_images(self._idle_images)
            self._light_attack_images = self.flip_images(self._light_attack_images)
            self._heavy_attack_images = self.flip_images(self._heavy_attack_images)
            self._move_forward_images = self.flip_images(self._move_forward_images)
            self._move_backward_images = self.flip_images(self._move_backward_images)
            self._direction = direction

    def flip_images(self,array):
        for i in range(len(array)):
            array[i] = pg.transform.flip(array[i], True, False)
        return array
    
    def reset_count(self):
        self._count = 0

    def play_idle(self):
        if self._count < 20:
            self._image = self._idle_images[0]
            self._count+=1
        elif self._count >= 20:
            self._image = self._idle_images[1]
            self._count+=1
        if self._count >= 40:
            self.reset_count()
        

class Bowie_Animation(Animation):
    def __init__(self, width, height,
                 path,direction):
        super().__init__(width,height,path,direction)

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

    def play_jump(self):
        self._image = self._jump_images[0]

    def play_attack(self, attack_state):
        if attack_state == "light_attack":
            if self._count < 7:
                self._image = self._light_attack_images[0]
                self._count+=1
            if self._count >= 7:
                self.reset_count()
                return None

        elif attack_state == "heavy_attack":
            if self._count < 10:
                self._image = self._heavy_attack_images[0]
                self._count+=1
            elif self._count >= 10 and self._count < 20:
                self._image = self._heavy_attack_images[1]
                self._count+=1
            elif self._count >= 20 and self._count < 30:
                self._image = self._heavy_attack_images[2]
                self._count+=1
            elif self._count >= 30:
                self._image = self._heavy_attack_images[3]
                self._count+=1
            if self._count >= 39:
                self.reset_count() 
                return None
                        
        return attack_state   
            
        
    def play_block(self):
        pass