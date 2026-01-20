import json

DATA='daten.json'

def json_save(DATA, data):
    """
    Diese Funktion basiert auf der json-Datenspeicherung.
    """
    with open(DATA, "w", encoding = "utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def json_load(DATA):
    """
    Es liest die JSON-Datei und gibt sie als dict zurück.
    """
    with open(DATA, "r", encoding = "utf-8") as f:
        return json.load(f)
