import winsound

def play_menu_music():
    """
    Importiert die Eingangsmusik fürs Spiel
    """
    winsound.PlaySound("sounds/price_is_right.wav", winsound.SND_FILENAME)
    pass

def stop_music():
    """
    Stoppt die Musik
    """
    winsound.PlaySound(None, winsound.SND_PURGE)
    pass

def play_game_music():
    """
    Importiert einen Soundeffekt fürs Spiel
    """
    winsound.PlaySound("sounds/thinking.wav", winsound.SND_FILENAME)
    pass

def stop_game_music():
    """
    Stoppt einen Soundeffekt fürs Spiel
    """
    pass