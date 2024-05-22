from pygame import mixer
import os

class Music():
    @staticmethod
    def load_and_play_infinite(file, path="./assets/music/"):
        """
        Load music file and repeat forever.

        Parameters:
            file (str): Music file name including extension.
            path (str): Folder the music file is stored in.
        """
        mixer.music.load(f"{path}{file}")
        mixer.music.play(-1)
    
    @staticmethod
    def load_and_continue_play(file, path="./assets/music/"):
        """
        Load music file and play until finished.

        Parameters:
            file (str): Music file name including extension.
            path (str): Folder the music file is stored in.
        """
        if not mixer.music.get_busy():
            mixer.music.load(f"{path}{file}")
            mixer.music.play()

    @staticmethod
    def stop():
        """
        Stop all music.
        """
        mixer.music.stop() 