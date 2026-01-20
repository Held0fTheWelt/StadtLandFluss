import wikipedia
import requests
#wikipedia.set_lang("de")

question_types = ["stadt", "land", "fluss"]

def check_answer(value, question_type, current_character):
    # ist der erste buchstabe gleich dem aktuellen buchstaben
    if current_character.lower() != value[0].lower():
        print(f"Das ist nicht der Anfangsbuchstabe, der benötigt wird. Das Wort sollte mit {current_character} beginnen.")
        return False
    # gibt es einen wikipedia eintrag, zu der aktuellen eingabe
    if not if_exists_in_wiki(value):
        print("Es gibt keinen passenden Wikipedia Eintrag")
        return False

    result = getresult_for_wikipedia_term(value)

    if question_type in result["wikipedia"]["extract"]:
        print("Antwort ist richtig")
        return True
    print("Antwort ist nicht richtig")
    return False


TEST_DATA = ["Stuttgart", "Spanien", "Seine"]

def if_exists_in_wiki(term: str) -> bool:
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

#    print("Status:", response.status_code)
#    print("URL:", response.url)
#    print("Text:", response.text[:200])

    response.raise_for_status()  # wirft Fehler, falls HTTP-Fehler
    data = response.json()
    return bool(data[1])



#print(if_exists_in_wikipedia("Berlin"))  # → True
"""
{
   "term":"Dortmund",
   "wikipedia":{
      "found":true,
      "api_url":"https://de.wikipedia.org/api/rest_v1/page/summary/Dortmund",
      "title":"Dortmund",
      "description":"Dortmund [ˈdɔʁtmʊnt]  (Standardaussprache; regional: [ˈdo:ɐ̯tmʊnt]; westfälisch Düörpm) ist eine kreisfreie Großstadt im östlichen Ruhrgebiet in Nordrhein-Westfalen",
      "extract":"Dortmund [ˈdɔʁtmʊnt]  (Standardaussprache; 
            regional: [ˈdo:ɐ̯tmʊnt]; westfälisch Düörpm) ist eine kreisfreie Großstadt im östlichen Ruhrgebiet in Nordrhein-Westfalen. Mit 603.462 Einwohnern am 31. Dezember 2024 ist sie nach der Einwohnerzahl die neuntgrößte Stadt Deutschlands, nach Köln und Düsseldorf die drittgrößte Stadt des Landes Nordrhein-Westfalen, nach Fläche und Einwohnerzahl die größte Stadt des Ruhrgebiets und nach Einwohnerzahl die größte Stadt des Landesteils Westfalen. Dortmund ist a...",
      "type":"city",
      "categories_detected":{
         "is_city":true,
         "is_country":false,
         "is_river":false
      },
      "categories":[
         "Deutsche Universitätsstadt",
         "Dortmund",
         "Ehemalige Kreisstadt in Nordrhein-Westfalen",
         "Ersterwähnung 882",
         "Gemeinde in Nordrhein-Westfalen",
         "Hansestadt",
         "Kreisfreie Stadt in Nordrhein-Westfalen",
         "Ort am Westfälischen Hellweg",
         "Ort an der Ruhr",
         "Ort in Nordrhein-Westfalen"
      ]
   },
   "validation":{
      "Stadt":true,
      "Land":false,
      "Fluss":false
   }
}
"""

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


def detect_city(categories, extract):
    """Erkennt ob es sich um eine Stadt handelt"""
    city_keywords = [
        "stadt", "großstadt", "metropole", "hauptstadt",
        "gemeinde", "ort in", "kreisstadt", "hansestadt"
    ]

    # Prüfe Kategorien
    for category in categories:
        cat_lower = category.lower()
        if any(keyword in cat_lower for keyword in city_keywords):
            return True

    # Prüfe Extract (erste 200 Zeichen)
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
            }
        },
        "validation": {
            "Stadt": False,
            "Land": False,
            "Fluss": False
        }
    }