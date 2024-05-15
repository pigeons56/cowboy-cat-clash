import pygame as pg
import os

class Animation():
    def __init__(self, width, height,
                 path,direction):
        self.width = width
        self.height = height
        self.path = path
        self.load_all_images()
        self.direction = "right"
        self.check_direction(direction)
        self.image = self.idle_images[0]
        self.reset_count()
    
    def load_images(self, path, array):
        for i in os.listdir(path):
            array.append(pg.image.load(f"{path}/{i}"))
        return array
    
    def load_jump_images(self):
        self.jump_images = self.load_images(f"{self.path}/jump",[])
    
    def load_idle_images(self):
        self.idle_images = self.load_images(f"{self.path}/idle",[])

    def load_light_attack_images(self):
        self.light_attack_images = self.load_images(f"{self.path}/light_attack",[])
    
    def load_heavy_attack_images(self):
        self.heavy_attack_images = self.load_images(f"{self.path}/heavy_attack",[])

    def load_block_images(self):
        self.block_images = self.load_images(f"{self.path}/block",[])

    def load_move_forward_images(self):
        self.move_forward_images = self.load_images(f"{self.path}/move_forward",[])
    
    def load_move_backward_images(self):
        self.move_backward_images = self.load_images(f"{self.path}/move_backward",[])

    def load_defeat_images(self):
        self.defeat_images = self.load_images(f"{self.path}/defeat",[])

    def load_victory_images(self):
        self.victory_images = self.load_images(f"{self.path}/victory",[])
    
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
        if self.direction != direction:
            self.jump_images = self.flip_images(self.jump_images)
            self.idle_images = self.flip_images(self.idle_images)
            self.light_attack_images = self.flip_images(self.light_attack_images)
            self.heavy_attack_images = self.flip_images(self.heavy_attack_images)
            self.move_forward_images = self.flip_images(self.move_forward_images)
            self.move_backward_images = self.flip_images(self.move_backward_images)
            self.direction = direction

    def flip_images(self,array):
        for i in range(len(array)):
            array[i] = pg.transform.flip(array[i], True, False)
        return array
    
    def reset_count(self):
        self.count = 0

    def play_idle(self):
        if self.count < 20:
            self.image = self.idle_images[0]
            self.count+=1
        elif self.count >= 20:
            self.image = self.idle_images[1]
            self.count+=1
        if self.count >= 40:
            self.reset_count()

    def play_move_forward(self):
        if self.count < 20:
            self.image = self.move_forward_images[0]
            self.count+=1
        elif self.count >= 20:
            self.image = self.move_forward_images[1]
            self.count+=1
        if self.count >= 40:
            self.reset_count()

    def play_move_backward(self):
        if self.count < 20:
            self.image = self.move_backward_images[0]
            self.count+=1
        elif self.count >= 20:
            self.image = self.move_backward_images[1]
            self.count+=1
        if self.count >= 40:
            self.reset_count()

    def play_jump(self):
        self.image = self.jump_images[0]

    def play_attack(self, attack_state):
        if attack_state == "light_attack":
            if self.count < 7:
                self.image = self.light_attack_images[0]
                self.count+=1
            if self.count >= 7:
                self.reset_count()
                return None
            else:
                return attack_state
        elif attack_state == "heavy_attack":
            if self.count < 10:
                self.image = self.heavy_attack_images[0]
                self.count+=1
            elif self.count >= 10 and self.count < 20:
                self.image = self.heavy_attack_images[1]
                self.count+=1
            elif self.count >= 20 and self.count < 30:
                self.image = self.heavy_attack_images[2]
                self.count+=1
            elif self.count >= 30:
                self.image = self.heavy_attack_images[3]
                self.count+=1
            if self.count >= 40:
                self.reset_count() 
                return None
            else:
                return attack_state   
        
    def play_block(self):
        if self.count < 9:
            self.image = self.block_images[0]
            self.count+=1
        if self.count >= 9:
            self.reset_count()
            return False
        else:
            return True