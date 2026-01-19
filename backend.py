import random
import time
#from ui_ux import show_highscore

TEST_DATA = ["Stuttgart", "Spanien", "Seine"]

def get_random_character():
    """Finde einen beliebigen Buchstaben im Alphabet"""
    random_upper_letter = chr(random.randint(ord('A'), ord('Z')))
    return random_upper_letter

def play_round():
    startzeit = time.time()  # startzeit
    stadt = input("Stadt: ")
    land = input("Land: ")
    fluss = input("Fluss: ")
    endzeit = time.time()  # endzeit
    dauer = endzeit - startzeit
    return [dauer, stadt, land, fluss]

def play():
    """ Spielt eine Runde Stadt Land Fluss und ruft die Auswertung auf"""

    # Runde startet - Startzeit wird gemessen

    print("Lets play *SLF 3000*")

    dauer, stadt, land, fluss = play_round()

    print("Fertig!")
    print(f"Du hast {dauer:.2f} Sekunden gebraucht.")

    # Bewerte Result
    result = get_result(dauer, stadt, land, fluss)
    update_highscore(result)
   # show_highscore()
TIME_FOR_BONUS = 30


def get_result(dauer, stadt, land, fluss):
    """ Berechnet das Ergebnis """
    result = 0
    if check_answer(stadt, question_types[0]):
        result += 5
    if check_answer(land, question_types[1]):
        result += 5
    if check_answer(fluss, question_types[2]):
        result += 5


    print(f"Du {result} Punkte!")
    return result


question_types = ["city", "country", "lake"]

def check_answer(value, question_type):
    if question_type == "city" and value == TEST_DATA[0]:
        return True
    if question_type == "country" and value == TEST_DATA[1]:
        return True
    if question_type == "lake" and value == TEST_DATA[2]:
        return True
    return False


def update_highscore(result):
    """Zeigt den neuen Highscore an"""
    pass
