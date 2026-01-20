highscore = {}  # Für lokale Anzeige (falls nötig)

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


def lets_play():
    print(f"Lets play: {RED}STADT{END}-{GREEN}LAND{END}-{BLUE}FLUSS{END}")


def get_input(term):
    return input(f"{term}: ")


def greeting():
    print(
        f"""
    {RED} ____  _            _ _   {END}  {GREEN}_                    _ {END}{BLUE}  _____ _{END}
    {RED}/ ___|| |_ __ _  __| | |_  {END}{GREEN}| |    __ _ _ __   __| |{END}{BLUE} |  ___| |_   _ ___ ___{END}
    {RED}\\___ \\| __/ _` |/ _` | __| {END}{GREEN}| |   / _` | '_ \\ / _` |{END}{BLUE} | |_  | | | | / __/ __|{END}
    {RED} ___) | || (_| | (_| | |_  {END}{GREEN}| |__| (_| | | | | (_| |{END}{BLUE} |  _| | | |_| \\__ \\__ \\{END}
    {RED}|____/ \\__\\__,_|\\__,_|\\__| {END}{GREEN}|_____\\__,_|_| |_|\\__,_|{END}{BLUE} |_|   |_|\\__,_|___/___/{END}

    {LIGHT_GREEN}RIVER{END}-{LIGHT_GREEN}PIRATES{END} Entertainment®
    """
    )
    input("➡️  Drücke " + YELLOW + "'Enter' " + END + "zum starten ...")


def show_rules():
    """
    Der Spielablauf funktioniert wie folgt:
    Jeder Spieler spielt 1 Runde basierend auf 3 Buchstaben.
    Das System generiert diese zufällig und fragt den Nutzer zu
    jedem Buchstaben nach einer passenden Stadt, einem Land und
    einem Fluss beginnend mit diesem Buchstaben.
    Wenn der User mit einem Buchstaben fertig ist (entweder duch eingabe oder
    "weiter" mit Enter-taste) wird der nächste Buchstabe generiert.
    """
    print("  🌇🌍🌊")
    print(
        YELLOW + "  Achtung Spieler, die festgelegten Regeln sind wie folgt:\n" + END
        + "- Jeder Spieler spielt 1 Runde basierend auf 1 Buchstaben\n"
        + "- Es muss zu jedem Buchstaben eine Stadt, ein Land und ein Fluss angegeben werden\n"
        + "- Wenn dir nichts einfällt, überspringe eine beliebige Frage mit der Enter-Taste\n"
        + "- VIEL SPASS!"
    )
    print("  🌇🌍🌊")
    input("➡️  Drücke " + YELLOW + "'Enter' " + END + "zum starten ...")


def menu():
    print()
    try:
        user_choice = int(input(
            "\t" + GREEN + "1." + END + " PLAY\n"
            "\t" + GREEN + "2." + END + " HIGHSCORE\n"
            "\t" + GREEN + "3." + END + " HELP\n"
            "\t" + GREEN + "4." + END + " EXIT\n"
        ))
    except ValueError:
        print("Ungültige Eingabe. Bitte Zahl 1-4 eingeben.")
        return True
    print()

    if user_choice == 1:
        # Play erst importieren, wenn benötigt → verhindert zirkuläre Abhängigkeit
        import backend
        backend.play()
    elif user_choice == 2:
        show_highscore()
    elif user_choice == 3:
        show_rules()
    elif user_choice == 4:
        return False
    return True


def exit_game():
    print(
        fr"""
    {GREEN}  ____     ___     ___    ____    ____    __   __  _____ {END}
    {GREEN} / ___|   / _ \   / _ \  |  _ \  | __ )   \ \ / / | ____| {END}
    {GREEN}| |  _   | | | | | | | | | | | | | |_ \    \ V /  |  _|   {END}
    {GREEN}| |_| |  | |_| | | |_| | | |_| | | |_) |    | |   | |___  {END}
    {GREEN} \____|   \___/   \___/  |____/  |____/     |_|   |_____| {END}
    """)
    print("     Danke fürs Spielen! Bis zum nächsten Mal👋")


def show_highscore():
    """
    Zeigt die Highscores an.
    Lädt sie aus daten.json, falls vorhanden.
    """
    import data_transfer
    highscores = data_transfer.json_load(data_transfer.DATA)

    print(
        f"{YELLOW}   ★★★ {END}"
        f"{RED} _   _ ___ ____ _   _ {END}"
        f"{BLUE}  ____   ____ ___  ____  _____ {END}"
        f"{YELLOW} ★★★{END}\n"

        f"{YELLOW}   ★★★ {END}"
        f"{RED}| | | |_ _/ ___| | | |{END}"
        f"{BLUE} / ___| / ___/ _ \\|  _ \\| ____|{END}"
        f"{YELLOW} ★★★{END}\n"

        f"{YELLOW}   ★★★ {END}"
        f"{RED}| |_| || | |  _| |_| |{END}"
        f"{BLUE} \\___ \\| |  | | | | |_) |  _|  {END}"
        f"{YELLOW} ★★★{END}\n"

        f"{YELLOW}   ★★★ {END}"
        f"{RED}|  _  || | |_| |  _  |{END}"
        f"{BLUE}  ___) | |__| |_| |  _ <| |___ {END}"
        f"{YELLOW} ★★★{END}\n"

        f"{YELLOW}   ★★★ {END}"
        f"{RED}|_| |_|___\\____|_| |_|{END}"
        f"{BLUE} |____/ \\____\\___/|_| \\_\\_____|{END}"
        f"{YELLOW} ★★★{END}"
    )

    if not highscores:
        print("Noch keine Highscores vorhanden.")
    else:
        # Sortieren nach Punkte, absteigend
        sorted_scores = sorted(highscores, key=lambda x: x["Punkte"], reverse=True)

        print("╔══════════════════════════════╗")
        print("║ #  Name     Punkte   Zeit    ║")
        print("╠══════════════════════════════╣")

        for i, entry in enumerate(sorted_scores[:10], start=1):
            zeit_str = f"{entry['Zeit']:.2f}s"
            print(f"║ {i:<2} {entry['Name']:<8} {entry['Punkte']:>6}   {zeit_str:>6}  ║")

        print("╚══════════════════════════════╝")
        print("")

    input("➡️  Drücke " + YELLOW + "'Enter' " + END + "um zum Menü zu gelangen ...")
