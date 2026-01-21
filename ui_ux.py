from color import *
import data_transfer
import backend
import soundmodul
import settings

highscore = {}  # Für lokale Anzeige (falls nötig)

indent = " " * 10

def show_settings():
    """
    Zeigt die Spieleinstellungen an und ermöglicht Anpassungen.
    """
    while True:
        print()
        print(f"{indent}╔════════╦════════════════════════════════════╗")
        print(f"{indent}║   #    ║           GAME SETTINGS            ║")
        print(f"{indent}╠════════╬════════════════════════════════════╣")
        print(f"{indent}║   1    ║ Lautstärke anpassen                ║")
        print(f"{indent}║   2    ║ Logs aktivieren / deaktivieren     ║")
        print(f"{indent}║   3    ║ Highscores löschen (Reset)         ║")  # Neu
        print(f"{indent}║   4    ║ Zurück zum Hauptmenü               ║")
        print(f"{indent}╚════════╩════════════════════════════════════╝")
        print()

        try:
            setting = int(input("➡️  Auswahl: "))
            if setting == 1:
                backend.change_volume()
                break
            elif setting == 2:
                backend.change_active_logging()
                break
            elif setting == 3:
                # Sicherheitsabfrage
                confirm = input(f"Bist du sicher, dass du alle Highscores löschen willst? {YELLOW}(j/n): {END}").lower()
                if confirm == 'j':
                    data_transfer.reset_highscores()
                break
            elif setting == 4:
                print("Kehre zurück.")
                break
            else:
                print("Ungültige Auswahl. Kehre zurück.")
                break
        except ValueError:
            print("Fehler: Bitte eine Zahl eingeben (z.B. 1).")


def lets_play():
    """ Nachricht, die ausgegeben wird, wenn die Spielrunde startet"""
    print(f"Lets play: {RED}STADT{END}-{GREEN}LAND{END}-{BLUE}FLUSS{END}")


def get_input(term):
    """
    Gibt den vom Benutzer eingebenen Inhalt zurück
    """
    return input(f"{term}: ")


def greeting():
    """
    Zeigt den Startbildschirm des Spiels an.
    """
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
    input("➡️  Drücke " + YELLOW + "'Enter' " + END + "zum Starten ...")


def show_rules():
    """
    Überblick über den Spieleablauf.Der Spielablauf funktioniert wie folgt:
    Jeder Spieler spielt 1 Runde basierend auf 1 Buchstaben.
    Das System generiert diesen zufällig und fragt den Nutzer / die Nutzerin
    nach einer passenden Stadt, einem Land und
    einem Fluss beginnend mit diesem Buchstaben.
    Wenn der User mit einem Buchstaben fertig ist (entweder duch Eingabe oder
    "weiter" mit Enter-taste) wird die Eingabe über Wikipedia auf Richtigkeit geprüft und zurückgegeben.
    """
    print("  🌇🌍🌊")
    print(
        YELLOW + "  Achtung Spieler! Die festgelegten Regeln sind wie folgt:\n" + END
        + "- Jede spielende Person spielt 1 Runde basierend auf einen Buchstaben\n"
        + "- Es muss zum Buchstaben jeweils eine Stadt, ein Land und ein Fluss eingegeben werden\n"
        + "- Wenn dir nichts einfällt, überspringe eine beliebige Frage mit der Enter-Taste\n"
        + "- Füge nach dem Spiel deinen Namen hinzu\n"
        + "- Sollten deine erreichten Punkte innerhalb der Top 10 liegen, wirst du dich unter deinen Namen in den Highscores wieder finden\n"
        + "- Du kannst das Spiel allein oder abwechselnd mit Anderen spielen und so eure Highscores verbessern\n"
        + "- Ein Retro-Game neu interpretiert – altbekannter Spaß, frisch programmiert\n"
        + "- VIEL SPASS!\n"
    )
    print("  🌇🌍🌊")
    print()
    input("➡️  Drücke " + YELLOW + "'Enter' " + END + "zum starten ...")


def menu():
    """
    Zeigt das Auswahlmenü an und führt zu den ausgewhählten Menüinhalten.
    """
    print()
    try:
        user_choice = int(input(
            "\t" + GREEN + "1." + END + " 🕹️ PLAY\n"
            "\t" + GREEN + "2." + END + " 🏆 HIGHSCORE\n"
            "\t" + GREEN + "3." + END + " 🛟 HELP\n"
            "\t" + GREEN + "4." + END + " ⚙️ SETTINGS\n"                                        
            "\t" + GREEN + "5." + END + " ❌ EXIT\n"
        ))
    except ValueError:
        print()
        print("Ungültige Eingabe. Bitte Zahl 1-4 eingeben.")
        return True
    print()

    if user_choice == 1:
        # Play erst importieren, wenn benötigt → verhindert zirkuläre Abhängigkeit
        soundmodul.stop_music()
        soundmodul.play_game_music(settings.volume)
        backend.play()
        soundmodul.stop_music()
        soundmodul.play_menu_music(settings.volume)
    elif user_choice == 2:
        show_highscore()
    elif user_choice == 3:
        show_rules()
    elif user_choice == 4:
        show_settings()
    elif user_choice == 5:
        soundmodul.stop_music()
        return False
    return True


def exit_game():
    """
    Zeigt den Verabschiedungsbildschirm an
    """
    print(
        fr"""
    {GREEN}  ____    ___     ___    ____    ____   __   __  _____ {END}
    {GREEN} / ___|  / _ \   / _ \  |  _ \  | __ )  \ \ / / | ____| {END}
    {GREEN}| |  _  | | | | | | | | | | | | | |_ \   \ V /  |  _|   {END}
    {GREEN}| |_| | | |_| | | |_| | | |_| | | |_) |   | |   | |___  {END}
    {GREEN} \____|  \___/   \___/  |____/  |____/    |_|   |_____| {END}
    """)
    print(f"   {YELLOW} Danke fürs Spielen!{END} Bis zum nächsten Mal & liebe Grüße von den {LIGHT_GREEN}FLUSS-PIRATEN {END}👋")


def show_highscore():
    """
    Zeigt die alten und den neuen Highscores an - mit Medaillen in der Tabelle!
    """
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
    print()
    indent = " " * 11

    if not highscores:
        print(f"{indent}Noch keine Highscores vorhanden.")
    else:
        # Sortieren nach Punkte, absteigend
        sorted_scores = sorted(highscores, key=lambda x: x["Punkte"], reverse=True)

        # Header (breitere #-Spalte für Medaillen)
        print(f"{indent}╔════════╦════════════╦═════════╦═════════╗")
        print(f"{indent}║   #    ║    Name    ║  Punkte ║   Zeit  ║")
        print(f"{indent}╠════════╬════════════╬═════════╬═════════╣")

        # Top 10 Einträge mit Medaillen IN der Tabelle
        for i, entry in enumerate(sorted_scores[:10], start=1):
            # Name auf maximal 10 Zeichen begrenzen
            name = entry.get('Name', 'Unbekannt')
            if len(name) > 10:
                name = name[:9] + '…'

            # Punkte und Zeit formatieren
            punkte = entry.get('Punkte', 0)
            zeit = entry.get('Zeit', 0)

            # Rank-String mit Medaille (rechtsbündig, 6 Zeichen breit)
            if i == 1:
                rank = f"🥇 {i:>2} "  # Emoji + Leerzeichen + Nummer rechtsbündig
            elif i == 2:
                rank = f"🥈 {i:>2} "
            elif i == 3:
                rank = f"🥉 {i:>2} "
            else:
                rank = f"   {i:>2} "  # 3 Leerzeichen + Nummer rechtsbündig

            # Zeile ausgeben
            print(f"{indent}║ {rank} ║ {name:<10} ║ {punkte:>7.2f} ║ {zeit:>6.2f}s ║")

        # Footer
        print(f"{indent}╚════════╩════════════╩═════════╩═════════╝")
        print()

    input("➡️  Drücke " + YELLOW + "'Enter' " + END + "um zum Menü zu gelangen ...")