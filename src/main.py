from screen import *

if __name__ == "__main__":
    #Initialize pygame
    pg.init()
    pg.font.init()

    #Title & icon
    pg.display.set_caption("Cowboy Cat Clash")
    pg.display.set_icon(pg.image.load("../assets/extra/icon.png"))

    #Initialize musicplayer
    mixer.init()

    #Start the game!
    Start_Screen().loop()