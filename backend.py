import random
import time
import ui_ux
import datetime

from wiki import *

Highscore = []

def get_random_character():
    """Finde einen beliebigen Buchstaben im Alphabet"""
    random_upper_letter = chr(random.randint(ord('A'), ord('Z')))
    return random_upper_letter



def play():
    """ Spielt eine Runde Stadt Land Fluss und ruft die Auswertung auf"""

    # Runde startet - Startzeit wird gemessen

    print("Lets play *SLF 3000*\n")
    random_character = get_random_character()
    print(f"Der aktuelle Buchstabe ist {random_character}\n")
    startzeit = time.time()  # startzeit
    stadt = ui_ux.get_input("Stadt")
    land = ui_ux.get_input("Land")
    fluss = ui_ux.get_input("Fluss")
    endzeit = time.time()  # endzeit
    dauer = endzeit - startzeit

    print("Fertig!")
    print(f"Du hast {dauer:.2f} Sekunden gebraucht.")

    # Bewerte Result
    result = get_result(dauer, stadt, land, fluss, random_character)
    update_highscore(result)
   # show_highscore()
TIME_FOR_BONUS = 30


def get_result(dauer, stadt, land, fluss, current_character):
    """ Berechnet das Ergebnis und zeigt es an """
    result = 0
    if check_answer(stadt, question_types[0], current_character):
        result += 5
    if check_answer(land, question_types[1], current_character):
        result += 5
    if check_answer(fluss, question_types[2], current_character):
        result += 5
    player_name = get_player_name()
    print(f"{player_name}, du hast {result} Punkte!")
    return result


def get_player_name():
    """Erfragt den Namen der spielenden Person"""
    player_name = (input("Gib bitte deinen Namen ein! "))
    return player_name

def update_highscore(result):
    """Zeigt den neuen Highscore an"""

    # ist highscore ein neuer bester score ?
        # name abfragen
      #  result["name"] = "Frank"
       # result["datum"] = datetime.datetime.now()
        # highscore eintragen
        #Highscore.append(result)
    # daten speichern ?? Wenn ja, bei show_highscore daten laden
    #[
    #    {
    #       "name" : "Thomas",
    #       "punkte" : 25,
    #       "zeit" : 12.4,
    #       "datum": 20.01.2026
    #    },
    #    {
    #       "name" : "Dieter",
    #       "punkte" : 20,
    #       "zeit" : 15.4,
    #       "datum": 20.01.2026
    #    }
    #]
    pass
