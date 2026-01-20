import wikipedia
import requests
from color import*
#wikipedia.set_lang("de")

question_types = ["stadt", "land", "fluss"]

# --- Hilfsfunktionen zuerst definieren ---

def if_exists_in_wiki(term: str) -> bool:
    """
    Es prüft, ob ein Wort (term) auf Wikipedia existiert.
    """
    url = "https://de.wikipedia.org/w/api.php"
    parameter = {
        "action": "opensearch",
        "search": term,
        "limit": 1,
        "namespace": 0,
        "format": "json"
    }
    headers = {
        "User-Agent": "StadtLandFlussGame/1.0 (https://example.com)"
    }

    response = requests.get(url, params=parameter, headers=headers)
    response.raise_for_status()  # wirft Fehler, falls HTTP-Fehler
    data = response.json()
    return bool(data[1])


def detect_city(categories, extract):
    """Erkennt ob es sich um eine Stadt handelt"""
    city_keywords = [
        "stadt", "großstadt", "metropole", "hauptstadt",
        "gemeinde", "ort in", "kreisstadt", "hansestadt"
    ]
    for category in categories:
        cat_lower = category.lower()
        if any(keyword in cat_lower for keyword in city_keywords):
            return True
    extract_lower = extract[:200].lower()
    if "ist eine stadt" in extract_lower or "ist die hauptstadt" in extract_lower:
        return True
    return False


def detect_country(categories, extract):
    """Erkennt ob es sich um ein Land handelt"""
    country_keywords = [
        "staat in", "land in", "staat (", "mitgliedstaat",
        "republik", "königreich", "fürstentum", "bundesstaat"
    ]
    for category in categories:
        cat_lower = category.lower()
        if any(keyword in cat_lower for keyword in country_keywords):
            return True
    extract_lower = extract[:200].lower()
    if "ist ein staat" in extract_lower or "ist ein land" in extract_lower:
        return True
    return False


def detect_river(categories, extract):
    """Erkennt ob es sich um einen Fluss handelt"""
    river_keywords = [
        "fluss", "strom", "gewässer", "nebenfluss",
        "zufluss", "fließgewässer"
    ]
    for category in categories:
        cat_lower = category.lower()
        if any(keyword in cat_lower for keyword in river_keywords):
            return True
    extract_lower = extract[:200].lower()
    if "ist ein fluss" in extract_lower or "ist ein strom" in extract_lower:
        return True
    return False


def get_description(extract):
    """Extrahiert eine kurze Beschreibung (erster Satz)"""
    first_sentence = extract.split('.')[0]
    return first_sentence if len(first_sentence) < 200 else first_sentence[:200] + "..."


def create_not_found_result(term):
    """Erstellt Ergebnis wenn Begriff nicht gefunden wurde"""
    return {
        "term": term,
        "wikipedia": {
            "found": False,
            "api_url": None,
            "title": None,
            "description": None,
            "extract": None,
            "type": None,
            "categories_detected": {
                "is_city": False,
                "is_country": False,
                "is_river": False
            },
            "categories": []
        },
        "validation": {
            "Stadt": False,
            "Land": False,
            "Fluss": False
        }
    }


def getresult_for_wikipedia_term(term):
    """
    Analysiert einen Begriff und kategorisiert ihn als Stadt, Land oder Fluss
    """
    term_original = term.strip()
    term_normalized = term_original.replace(" ", "_")

    url = "https://de.wikipedia.org/w/api.php"

    # Erweiterte Abfrage: Extract + Kategorien
    params = {
        "action": "query",
        "prop": "extracts|categories",
        "exintro": True,
        "explaintext": True,
        "titles": term_normalized,
        "format": "json",
        "cllimit": 50  # Anzahl der Kategorien
    }

    headers = {
        "User-Agent": "StadtLandFlussGame/1.0 (https://example.com)"
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return create_not_found_result(term_original)

    data = response.json()
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))

    # Prüfen ob Seite existiert
    if "missing" in page or "extract" not in page:
        return create_not_found_result(term_original)

    # Kategorien extrahieren
    categories = []
    if "categories" in page:
        categories = [cat["title"].replace("Kategorie:", "")
                      for cat in page["categories"]]

    # Kategorisierung durchführen
    is_city = detect_city(categories, page["extract"])
    is_country = detect_country(categories, page["extract"])
    is_river = detect_river(categories, page["extract"])

    # Typ bestimmen
    detected_type = None
    if is_city:
        detected_type = "city"
    elif is_country:
        detected_type = "country"
    elif is_river:
        detected_type = "river"

    # Strukturiertes Ergebnis erstellen
    result = {
        "term": term_original,
        "wikipedia": {
            "found": True,
            "api_url": f"https://de.wikipedia.org/api/rest_v1/page/summary/{term_normalized}",
            "title": page.get("title", term_original),
            "description": get_description(page["extract"]),
            "extract": page["extract"][:500] + "..." if len(page["extract"]) > 500 else page["extract"],
            "type": detected_type,
            "categories_detected": {
                "is_city": is_city,
                "is_country": is_country,
                "is_river": is_river
            },
            "categories": categories[:10]  # Erste 10 Kategorien
        },
        "validation": {
            "Stadt": is_city,
            "Land": is_country,
            "Fluss": is_river
        }
    }

    return result


# --- check_answer zuletzt, nachdem alle Hilfsfunktionen existieren ---
def check_answer(value, question_type, current_character):
    """
    Prüft:
    - Beginnt das Wort mit dem richtigen Buchstaben
    - Existiert es auf Wikipedia
    - Ist der Typ korrekt (stadt/land/fluss)
    """
    # ist etwas eingegeben?
    if not value:
        print(f'{RED}"{question_type.capitalize()}"{End} hat keine Eingabe!')
        return False

    # ist der erste buchstabe gleich dem aktuellen buchstaben
    if current_character.lower() != value[0].lower():
        print(f"Das ist nicht der Anfangsbuchstabe, der benötigt wird. Das Wort sollte mit {RED}{current_character}{END} beginnen.")
        return False

    # gibt es einen wikipedia eintrag, zu der aktuellen eingabe
    if not if_exists_in_wiki(value):
        print("Es gibt keinen passenden Wikipedia Eintrag")
        return False

    result = getresult_for_wikipedia_term(value)

    # Typ prüfen
    validation_map = {
        "stadt": result["validation"]["Stadt"],
        "land": result["validation"]["Land"],
        "fluss": result["validation"]["Fluss"]
    }

    if validation_map.get(question_type.lower(), False):
        print(f'Die Antwort {GREEN}"{value}"{END} als "{question_type.capitalize()}" ist korrekt.')
        return True

    print(f'Die Antwort {RED}"{value}"{END} als "{question_type.capitalize()}" ist nicht korrekt.')
    return False


# --- Testdaten ---
TEST_DATA = ["Stuttgart", "Spanien", "Seine"]
