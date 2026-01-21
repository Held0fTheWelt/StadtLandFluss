import winsound

def play_menu_music():
    winsound.PlaySound("sounds/price_is_right.wav", winsound.SND_FILENAME)
    pass

def stop_menu_music():
    pass

def play_game_music():
    winsound.PlaySound("sounds/thinking.wav", winsound.SND_FILENAME)
    pass

def stop_game_music():
    pass