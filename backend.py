import random
import time
import ui_ux
import data_transfer
import json
from color import *
from wiki import *  # check_answer, question_types etc.

TIME_FOR_BONUS = 30


def get_random_character():
    """
    Finde einen beliebigen Buchstaben im Alphabet
    """
    random_upper_letter = chr(random.randint(ord('A'), ord('Z')))
    return random_upper_letter


def play():
    """
    Spielt eine Runde Stadt Land Fluss und ruft die Auswertung auf
    """
    random_character = get_random_character()
    print(f"Der aktuelle Buchstabe ist: {BLUE}{random_character}{END}\n")

    startzeit = time.time()  # startzeit

    # Eingaben vom User (mit Error-Handling für Abbruch)
    try:
        stadt = ui_ux.get_input("Stadt")
        land = ui_ux.get_input("Land")
        fluss = ui_ux.get_input("Fluss")
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Spiel wurde abgebrochen.{END}")
        return None
    except EOFError:
        print(f"\n\n{RED}Eingabe-Fehler. Spiel wird beendet.{END}")
        return None
    except Exception as e:
        print(f"\n\n{RED}Unerwarteter Fehler bei der Eingabe: {e}{END}")
        return None

    endzeit = time.time()  # endzeit

    result = {}
    result["Zeit"] = endzeit - startzeit
    print("\nGutes Spiel! Danke!")
    print(f'Du hast{BLUE} {result["Zeit"]:.2f} {END}Sekunden gebraucht.\n')

    # Auswertung (mit Error-Handling)
    try:
        get_result(result, stadt, land, fluss, random_character)
    except Exception as e:
        print(f"{RED}Fehler bei der Auswertung: {e}{END}")
        result["Punkte"] = 0  # Fallback

    # Name des Spielers abfragen (mit Error-Handling)
    try:
        result["Name"] = get_player_name()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Namenseingabe abgebrochen. Verwende Standardname.{END}")
        result["Name"] = "Unbekannt"
    except EOFError:
        print(f"\n{RED}Eingabe-Fehler. Verwende Standardname.{END}")
        result["Name"] = "Unbekannt"
    except Exception as e:
        print(f"\n{RED}Fehler bei Namenseingabe: {e}. Verwende Standardname.{END}")
        result["Name"] = "Unbekannt"

    result["ABC"] = random_character

    print(f'{result["Name"]}, du hast {YELLOW}{result["Punkte"]:.2f}{END} Punkte!')

    # Highscore aktualisieren (mit Error-Handling)
    try:
        update_highscore(result)
    except Exception as e:
        print(f"{YELLOW}Warnung: Highscore konnte nicht gespeichert werden: {e}{END}")

    return result


def get_result(result, stadt, land, fluss, buchstabe):
    """
    Berechnet das Ergebnis und zeigt es an.
    """
    result["Punkte"] = 0

    # check_answer für jede Kategorie (bereits mit Error-Handling in wiki.py)
    try:
        if check_answer(stadt, "stadt", buchstabe):
            result["Punkte"] += 5
    except Exception as e:
        print(f"{YELLOW}Warnung: Stadt konnte nicht geprüft werden: {e}{END}")

    try:
        if check_answer(land, "land", buchstabe):
            result["Punkte"] += 5
    except Exception as e:
        print(f"{YELLOW}Warnung: Land konnte nicht geprüft werden: {e}{END}")

    try:
        if check_answer(fluss, "fluss", buchstabe):
            result["Punkte"] += 5
    except Exception as e:
        print(f"{YELLOW}Warnung: Fluss konnte nicht geprüft werden: {e}{END}")

    # Bonuszeit berechnen (mit Validierung)
    try:
        bonuszeit = max(0, TIME_FOR_BONUS - result["Zeit"])
        result["Punkte"] = result["Punkte"] * (1 + (bonuszeit / 100))  # Zinseszins formel
    except Exception as e:
        print(f"{YELLOW}Warnung: Bonusberechnung fehlgeschlagen: {e}{END}")
        # Punkte bleiben wie sie sind, ohne Bonus


def get_player_name():
    """
    Erfragt den Namen der Person.
    """
    while True:
        try:
            player_name = input(f"\nGib bitte deinen {YELLOW}Namen{END} ein! ")

            # Validierung: Name darf nicht leer sein
            if not player_name or player_name.strip() == "":
                print(f"{RED}Name darf nicht leer sein! Bitte erneut versuchen.{END}")
                continue

            # Validierung: Name sollte nicht zu lang sein
            if len(player_name) > 50:
                print(f"{RED}Name ist zu lang (max. 50 Zeichen)! Bitte erneut versuchen.{END}")
                continue

            return player_name.strip()

        except KeyboardInterrupt:
            raise  # Wird in play() abgefangen
        except EOFError:
            raise  # Wird in play() abgefangen
        except Exception as e:
            print(f"{RED}Fehler bei der Eingabe: {e}{END}")
            raise


def update_highscore(result):
    """
    Zeigt den neuen Highscore an und speichert ihn.
    """
    try:
        highscore = data_transfer.json_load(data_transfer.DATA)
    except FileNotFoundError:
        print(f"{YELLOW}Info: Noch keine Highscore-Datei vorhanden. Erstelle neue.{END}")
        highscore = []
    except json.JSONDecodeError:
        print(f"{YELLOW}Warnung: Highscore-Datei ist beschädigt. Erstelle neue.{END}")
        highscore = []
    except Exception as e:
        print(f"{YELLOW}Warnung: Fehler beim Laden des Highscores: {e}. Erstelle neue Liste.{END}")
        highscore = []

    # Neues Ergebnis hinzufügen (mit Validierung)
    try:
        highscore.append({
            "Name": result.get("Name", "Unbekannt"),
            "Punkte": float(result.get("Punkte", 0)),
            "Zeit": float(result.get("Zeit", 0)),
        })
    except Exception as e:
        print(f"{YELLOW}Warnung: Ergebnis konnte nicht zum Highscore hinzugefügt werden: {e}{END}")
        return


    # Speichern (mit Error-Handling)
    try:
        data_transfer.json_save(data_transfer.DATA, highscore)
        print(f"{GREEN}Highscore erfolgreich gespeichert!{END}")
    except PermissionError:
        print(f"{RED}Fehler: Keine Berechtigung zum Speichern der Highscore-Datei{END}")
    except OSError as e:
        print(f"{RED}Fehler: Highscore konnte nicht gespeichert werden: {e}{END}")
    except Exception as e:
        print(f"{RED}Unerwarteter Fehler beim Speichern: {e}{END}")
