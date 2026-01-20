import random
import time
import ui_ux
import data_transfer

from wiki import *  # check_answer, question_types etc.

TIME_FOR_BONUS = 30


def get_random_character():
    """Finde einen beliebigen Buchstaben im Alphabet"""
    random_upper_letter = chr(random.randint(ord('A'), ord('Z')))
    return random_upper_letter


def play():
    """ Spielt eine Runde Stadt Land Fluss und ruft die Auswertung auf"""
    random_character = get_random_character()
    print(f"Der aktuelle Buchstabe ist: {BLUE}{random_character}{END}\n")

    startzeit = time.time()  # startzeit

    # Eingaben vom User
    stadt = ui_ux.get_input("Stadt")
    land = ui_ux.get_input("Land")
    fluss = ui_ux.get_input("Fluss")

    endzeit = time.time()  # endzeit

    result = {}
    result["Zeit"] = endzeit - startzeit
    print("\nGutes Spiel! Danke!")
    print(f'Du hast {result["Zeit"]:.2f} Sekunden gebraucht.\n') # f-string korrigiert

    # Auswertung
    get_result(result, stadt, land, fluss, random_character)

    # Name des Spielers abfragen
    result["Name"] = get_player_name()
    result["ABC"] = random_character

    print(f'{result["Name"]}, du hast {YELLOW}{result["Punkte"]}{END} Punkte!')

    # Highscore aktualisieren
    update_highscore(result)

    return result


def get_result(result, stadt, land, fluss, buchstabe):
    """ Berechnet das Ergebnis und zeigt es an """
    result["Punkte"] = 0

    # check_answer für jede Kategorie
    if check_answer(stadt, "stadt", buchstabe):
        result["Punkte"] += 5
    if check_answer(land, "land", buchstabe):
        result["Punkte"] += 5
    if check_answer(fluss, "fluss", buchstabe):
        result["Punkte"] += 5


def get_player_name():
    """Erfragt den Namen der Person"""
    player_name = input("Gib bitte deinen Namen ein! ")
    return player_name


def update_highscore(result):
    """Zeigt den neuen Highscore an"""
    try:
        highscore = data_transfer.json_load(data_transfer.DATA)
    except (FileNotFoundError, json.JSONDecodeError):
        highscore = []

    # Neues Ergebnis hinzufügen
    highscore.append({
        "Name": result["Name"],
        "Punkte": result["Punkte"],
        "Zeit": result["Zeit"],
    })

    # Speichern
    # data_transfer.json_save(data_transfer.DATA, highscore)
