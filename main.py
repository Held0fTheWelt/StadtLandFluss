import data_transfer
from backend import *
from ui_ux import *
import soundmodul

def main():
    """
    Hauptfunktion für Spieleablauf
    """
    try:
        highscore = data_transfer.json_load(data_transfer.DATA)
    except:
        highscore = []

    # Menü Musik abspielen
    soundmodul.play_menu_music()

    greeting()

    # Hauptmenü-Schleife
    while True:

        if not menu():
            # menu() gibt False zurück bei Exit
            soundmodul.stop_music()
            exit_game()
            break

    # Am Ende ggf. Highscore speichern (falls noch nötig)
    data_transfer.json_save(data_transfer.DATA, highscore)


if __name__ == "__main__":
    main()
