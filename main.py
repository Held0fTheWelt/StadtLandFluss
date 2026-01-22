import data_transfer
from backend import *
from ui_ux import *
import soundmodul
import settings
import time
import os
clear = lambda: os.system('cls')

def main():
    """
    Hauptfunktion für Spieleablauf
    """
    try:
        highscore = data_transfer.json_load(data_transfer.DATA)
    except:
        highscore = []

    # Menü Musik abspielen
    soundmodul.play_menu_music(settings.volume)

    greeting()

    # Hauptmenü-Schleife
    while True:
        time.sleep(.5)
#        clear()
        if not menu():
            # menu() gibt False zurück bei Exit
            soundmodul.stop_music()
            exit_game()
            break

    soundmodul.stop_music()

if __name__ == "__main__":
    main()
