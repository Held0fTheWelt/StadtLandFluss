import pygame

# Automatische Initialisierung beim Import
pygame.mixer.init()

def play_menu_music(volume=0.02):
    """
    Spielt die Menümusik ab

    Args:
        volume: Lautstärke von 0.0 (stumm) bis 1.0 (max)
    """
    pygame.mixer.music.load("sounds/price_is_right.mp3")
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)  # -1 = Endlosschleife


def play_game_music(volume=0.02):
    """Spielt die Spielmusik ab"""
    pygame.mixer.music.load("sounds/thinking.wav")
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)


def stop_music():
    """Stoppt die Musik"""
    pygame.mixer.music.stop()


def set_volume(volume):
    """
    Ändert die Lautstärke während der Wiedergabe

    Args:
        volume: Wert zwischen 0.0 und 1.0
    """
    pygame.mixer.music.set_volume(volume)


def pause_music():
    """Pausiert die Musik"""
    pygame.mixer.music.pause()


def unpause_music():
    """Setzt pausierte Musik fort"""
    pygame.mixer.music.unpause()