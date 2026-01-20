import random
import time
import ui_ux
import datetime
from wiki import *
from ui_ux import show_highscore

TIME_FOR_BONUS = 30
highscore = {}

def get_random_character():
    """Finde einen beliebigen Buchstaben im Alphabet"""
    random_upper_letter = chr(random.randint(ord('A'), ord('Z')))
    return random_upper_letter


def play():
    """ Spielt eine Runde Stadt Land Fluss und ruft die Auswertung auf"""
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
    result = get_result(dauer, stadt, land, fluss)
    update_highscore(result)
    ui_ux.highscore()


def get_result(dauer, stadt, land, fluss):
    """ Berechnet das Ergebnis und zeigt es an """
    result = 0
    if check_answer(stadt, question_types[0]):
        result += 5
    if check_answer(land, question_types[1]):
        result += 5
    if check_answer(fluss, question_types[2]):
        result += 5
    player_name = get_player_name()
    print(f"{player_name}, du hast {result} Punkte!")
    return result


def get_player_name():
    """Erfragt den Namen der Person"""
    player_name = (input("Gib bitte deinen Namen ein! "))
    return player_name


def update_highscore(result):
    """Zeigt den neuen Highscore an"""
    new_score = get_result()
    name_of_player = get_player_name()
    highscore["Name"] = name_of_player
    highscore["Zeit"] = new_score
    highscore["Datum"] = datetime.datetime.now()
    highscore["Punkte"] = 0
    # ist highscore ein neuer bester score ?

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
