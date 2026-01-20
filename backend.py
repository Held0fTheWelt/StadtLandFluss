import random
import time
import ui_ux
import datetime
from wiki import *


TIME_FOR_BONUS = 30


def get_random_character():
    """Finde einen beliebigen Buchstaben im Alphabet"""
    random_upper_letter = chr(random.randint(ord('A'), ord('Z')))
    return random_upper_letter


def play():
    """ Spielt eine Runde Stadt Land Fluss und ruft die Auswertung auf"""
    print("Lets play *SLF 3000*\n")
    random_character = "d" #get_random_character()
    print(f"Der aktuelle Buchstabe ist {random_character}\n")
    startzeit = time.time()  # startzeit
    stadt = ui_ux.get_input("Stadt")
    land = ui_ux.get_input("Land")
    fluss = ui_ux.get_input("Fluss")
    endzeit = time.time()  # endzeit
    result = {}
    result["Zeit"] = endzeit - startzeit
    print("Fertig!")
    print(f"Du hast {result["Zeit"]:.2f} Sekunden gebraucht.")
    # Bewerte Result
    get_result(result, stadt, land, fluss, random_character)
    result["Name"] = get_player_name()
    print(f"{result["Name"]}, du hast {result["Punkte"]} Punkte!")
    update_highscore(result)



def get_result(result, stadt, land, fluss, buchstabe):
    """ Berechnet das Ergebnis und zeigt es an """
    result["Punkte"] = 0
    if check_answer(stadt, question_types[0], buchstabe):
        result["Punkte"] += 5
    if check_answer(land, question_types[1], buchstabe):
        result["Punkte"] += 5
    if check_answer(fluss, question_types[2], buchstabe):
        result["Punkte"] += 5


def get_player_name():
    """Erfragt den Namen der Person"""
    player_name = (input("Gib bitte deinen Namen ein! "))
    return player_name


def update_highscore(result):
    """Zeigt den neuen Highscore an"""
    ui_ux.highscore[result["Name"]] = result["Punkte"]

"""
{
    "Yves" : { "Name": "Yves", "Punkte": 5, "Zeit": 12.4 },
}
"""
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
