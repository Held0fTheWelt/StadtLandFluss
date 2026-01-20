import data_transfer
from backend import *
from ui_ux import *

def main():
    """ Main function"""
    # Am Start ggf. Highscore laden
    try:
        highscore = data_transfer.json_load(data_transfer.DATA)
    except:
        highscore = []

    # Begrüßung
    greeting()

    # Hauptmenü-Schleife
    while True:
        if not menu():  # menu() gibt False zurück bei Exit
            exit_game()
            break

    # Am Ende ggf. Highscore speichern (falls noch nötig)
    data_transfer.json_save(data_transfer.DATA, highscore)


if __name__ == "__main__":
    main()
