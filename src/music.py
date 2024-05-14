from pygame import mixer
import os

class Music():
    @staticmethod
    def load_and_play_infinite(file, path="../assets/music/"):
        mixer.music.load(f"{path}{file}")
        mixer.music.play(-1)
    
    @staticmethod
    def load_and_continue_play(file, path="../assets/music/"):
        if not mixer.music.get_busy():
            mixer.music.load(f"{path}{file}")
            mixer.music.play()

    @staticmethod
    def stop():
        mixer.music.stop() 
    
    @staticmethod
    def pause():
        mixer.music.pause()          
    
    @staticmethod
    def unpause():
        mixer.music.unpause()