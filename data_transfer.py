import json
from color import*

DATA = 'daten.json'  # Datei für Highscores


def json_save(DATA, data):
    """
    Diese Funktion basiert auf der json-Datenspeicherung.
    """
    try:
        with open(DATA, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Fehler beim Speichern der Datei {DATA}: {e}")


def json_load(DATA):
    """
    Es liest die JSON-Datei und gibt sie als dict zurück.
    """
    try:
        with open(DATA, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Datei existiert noch nicht
        return []
    except json.JSONDecodeError:
        # Datei ist leer oder fehlerhaft
        return []
    except Exception as e:
        print(f"Fehler beim Laden der Datei {DATA}: {e}")
        return []
