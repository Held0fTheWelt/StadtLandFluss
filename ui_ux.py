from backend import play

""" ANSI color codes """
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NEGATIVE = "\033[7m"
CROSSED = "\033[9m"
END = "\033[0m"

"""def greeting():

    print(BOLD + "Willkommen zum Stadt-Land-Fluss-Spiel" + END)
    print("🕹️🕹️🕹️🕹️🕹️🕹️🕹️🕹️🕹️🕹️🕹️🕹️🕹️🕹️🕹️🕹️🕹️")
    start = input("➡️ Drücke " + YELLOW +  "'Enter' " + END + "zum starten ...")
    if start == "":
        menu()"""

#alternativ
def greeting():
#     #print("🕹️"️ * 20)
#     print(r"""
#      ____  _            _ _     _                    _   _____ _
#     / ___|| |_ __ _  __| | |_  | |    __ _ _ __   __| | |  ___| |_   _ ___ ___
#     \___ \| __/ _` |/ _` | __| | |   / _` | '_ \ / _` | | |_  | | | | / __/ __|
#      ___) | || (_| | (_| | |_  | |__| (_| | | | | (_| | |  _| | | |_| \__ \__ \
#     |____/ \__\__,_|\__,_|\__| |_____\__,_|_| |_|\__,_| |_|   |_|\__,_|___/___/
#     Presentation of RIVER-PIRATES
#         """)
#     print("🕹️"️ * 20)
#     start = input("➡️ Drücke " + YELLOW +  "'Enter' " + END + "zum starten ...")
#     if start == "":
#         menu()
    print(
        f"""
    {RED} ____  _            _ _   {END}  {GREEN}_                    _ {END}{BLUE}  _____ _{END}
    {RED}/ ___|| |_ __ _  __| | |_  {END}{GREEN}| |    __ _ _ __   __| |{END}{BLUE} |  ___| |_   _ ___ ___{END}
    {RED}\\___ \\| __/ _` |/ _` | __| {END}{GREEN}| |   / _` | '_ \\ / _` |{END}{BLUE} | |_  | | | | / __/ __|{END}
    {RED} ___) | || (_| | (_| | |_  {END}{GREEN}| |__| (_| | | | | (_| |{END}{BLUE} |  _| | | |_| \\__ \\__ \\{END}
    {RED}|____/ \\__\\__,_|\\__,_|\\__| {END}{GREEN}|_____\\__,_|_| |_|\\__,_|{END}{BLUE} |_|   |_|\\__,_|___/___/{END}
    
    {FAINT}Presentation of {BOLD}{BLUE}RIVER{END}{FAINT}-{BOLD}{RED}PIRATES{END}
    """
    )



def show_rules():
    """
    Der Spielablauf funktioniert wie folgt:
    Jeder Spieler spielt 1 Runde basierend auf 3 Buchstaben.
    Das System generiert diese zufällig und fragt den Nutzer zu
    jedem Buchstaben nach einer passenden Stadt, einem Land und
    einem Fluss beginnend mit diesem Buchstaben.
    Für die 3 Durchläufe ist ein Zeitfenster von 1 Minute vorgesehen.
    Wenn der User mit einem Buchstaben fertig ist (entweder duch eingabe oder
    "weiter" mit Enter-taste) wird der nächste Buchstabe generiert.
    """
    print("🌇🌍🌊")
    print(
    YELLOW + "Achtung Spieler, die festgelegten Regeln sind wie folgt:\n" + END
    + "- Jeder Spieler spielt 1 Runde basierend auf 3 Buchstaben\n"
    + "- Es muss zu jedem Buchstaben eine Stadt, ein Land und ein Fluss angegeben werden\n"
    + "- Wenn dir nichts einfällt, überspringe eine beliebige Frage mit der Enter-Taste\n"
    + "- Du hast 1 Minute Zeit für deine 3 zufällig generierten Buchstaben\n"
    + "- VIEL SPASS!"
    )
    print("🌇🌍🌊")
    back = input("🥳 Drücke " + YELLOW + "'Enter' " + END + "zum Menü zu gelangen ...")
    if back == "":
        menu()

def menu():
    user_choice = int(input(
        GREEN + "1." + END + "PLAY\n" +
        GREEN + "2." + END + "HIGHSCORE\n" +
        GREEN + "3." + END + "HELP\n" +
        GREEN + "4." + END + "EXIT\n"
    ))
    if user_choice == 1:
        play()
    elif user_choice == 2:
        show_highscore()
    elif user_choice == 3:
        show_rules()
    elif user_choice == 4:
        exit_game()
        return False
    return True

def exit_game():
    print("Danke fürs Spielen! Bis zum nächsten Mal👋")


def show_highscore():
    pass

