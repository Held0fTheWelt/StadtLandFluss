import settings
import requests
from color import RED, GREEN, YELLOW, END

# wikipedia.set_lang("de")

KEYWORDS = {
    "city_keywords": [
        "stadt", "großstadt", "metropole", "hauptstadt",
        "gemeinde", "ort in", "kreisstadt", "hansestadt"
    ],
    "country_keywords": [
        "staat in", "land in", "staat (", "mitgliedstaat",
        "republik", "königreich", "fürstentum", "bundesstaat"
    ],
    "river_keywords": [
        "fluss", "strom", "gewässer", "nebenfluss",
        "zufluss", "fließgewässer", "flüsse in",
        "fluss in", "gewässer in", "längste Fluss"
    ],
    "river_patterns": [
        "längste Fluss"
        "ein fluss", "ist ein strom", "ist ein nebenfluss",
        "ist ein zufluss", "fließt durch", "mündet in",
        "entspringt", "fluss in", "rechter nebenfluss",
        "linker nebenfluss", "Der Fluss"
    ]
}

question_types = ["stadt", "land", "fluss"]


# --- Hilfsfunktionen zuerst definieren ---

def if_exists_in_wiki(term: str) -> bool:
    """
    Es prüft, ob ein Wort (term) auf Wikipedia existiert.
    Gibt False zurück bei Netzwerkfehlern.
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

    try:
        response = requests.get(url, params=parameter, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return bool(data[1])
    except requests.exceptions.ConnectionError:
        print(f'{RED}Fehler: Keine Verbindung zu Wikipedia möglich{END}')
        return False
    except requests.exceptions.Timeout:
        print(f'{RED}Fehler: Wikipedia-Anfrage hat zu lange gedauert (Timeout){END}')
        return False
    except requests.exceptions.HTTPError as e:
        print(f'{RED}Fehler: Wikipedia-Server-Fehler: {e}{END}')
        return False
    except requests.exceptions.RequestException as e:
        print(f'{RED}Fehler bei Wikipedia-Anfrage: {e}{END}')
        return False
    except Exception as e:
        print(f'{RED}Unerwarteter Fehler: {e}{END}')
        return False


def get_term_variants_by_type(term, expected_type=None):
    """
    Generiert Suchvarianten basierend auf dem erwarteten Typ.

    Beispiel:
        get_term_variants_by_type("Fulda", "fluss")
        → ["Fulda", "Fulda (Fluss)", "Fulda (Gewässer)"]
    """
    variants = [term]  # Original immer zuerst

    if expected_type:
        type_suffixes = {
            "stadt": [" (Stadt)", " (Gemeinde)", " (Ort)"],
            "land": [" (Staat)", " (Land)"],
            "fluss": [" (Fluss)", " (Gewässer)", " (Strom)"]
        }

        suffixes = type_suffixes.get(expected_type.lower(), [])
        for suffix in suffixes:
            variants.append(term + suffix)

    return variants


def get_disambiguation_candidates(term):
    """
    Holt alternative Vorschläge von Wikipedia für mehrdeutige Begriffe.
    Gibt eine Liste von möglichen Begriffen zurück.
    """
    url = "https://de.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": term,
        "limit": 10,  # Mehr Ergebnisse für bessere Auswahl
        "namespace": 0,
        "format": "json"
    }
    headers = {
        "User-Agent": "StadtLandFlussGame/1.0 (https://example.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        # data[1] enthält die Titel der gefundenen Artikel
        return data[1] if len(data) > 1 else []
    except requests.exceptions.ConnectionError:
        print(f'{YELLOW}Warnung: Keine Verbindung für Disambiguierung{END}')
        return []
    except requests.exceptions.Timeout:
        print(f'{YELLOW}Warnung: Timeout bei Disambiguierung{END}')
        return []
    except requests.exceptions.RequestException:
        return []
    except Exception:
        return []


def is_disambiguation_page(page_data):
    """
    Prüft ob es sich um eine Begriffsklärungsseite handelt.
    """
    if "categories" in page_data:
        for cat in page_data["categories"]:
            cat_title = cat["title"].lower()
            if "begriffsklärung" in cat_title or "begriffserklärung" in cat_title:
                return True

    # Auch im Extract nach Hinweisen suchen
    extract = page_data.get("extract", "").lower()
    if "bezeichnet:" in extract or "steht für:" in extract:
        return True

    return False


def detect_city(categories, extract):
    """Erkennt ob es sich um eine Stadt handelt"""
    for category in categories:
        cat_lower = category.lower()
        if any(keyword in cat_lower for keyword in KEYWORDS["city_keywords"]):
            return True

    # Längeren Text-Auszug prüfen für bessere Erkennung
    extract_lower = extract[:300].lower()
    city_patterns = [
        "ist eine stadt",
        "ist die hauptstadt",
        "ist eine großstadt",
        "ist eine gemeinde",
        "stadt in",
        "gemeinde in",
        "kreisstadt"
    ]

    if any(pattern in extract_lower for pattern in city_patterns):
        return True

    return False


def detect_country(categories, extract):
    """Erkennt ob es sich um ein Land handelt"""
    for category in categories:
        cat_lower = category.lower()
        if any(keyword in cat_lower for keyword in KEYWORDS["country_keywords"]):
            return True

    # Längeren Text-Auszug prüfen für bessere Erkennung
    extract_lower = extract[:300].lower()
    country_patterns = [
        "ist ein staat",
        "ist ein land",
        "ist eine republik",
        "ist ein königreich",
        "staat in",
        "land in"
    ]

    if any(pattern in extract_lower for pattern in country_patterns):
        return True

    return False


def detect_river(categories, extract):
    """Erkennt ob es sich um einen Fluss handelt"""
    for category in categories:
        cat_lower = category.lower()
        if any(keyword in cat_lower for keyword in KEYWORDS["river_keywords"]):
            return True

    # Längeren Text-Auszug prüfen für bessere Erkennung
    extract_lower = extract[:300].lower()

    if any(pattern in extract_lower for pattern in KEYWORDS["river_patterns"]):
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


def get_wikipedia_page_data(term_normalized):
    """
    Holt die Rohdaten einer Wikipedia-Seite.
    Gibt None zurück bei Netzwerkfehlern.
    """
    url = "https://de.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts|categories",
        "exintro": True,
        "explaintext": True,
        "titles": term_normalized,
        "format": "json",
        "cllimit": 50
    }
    headers = {
        "User-Agent": "StadtLandFlussGame/1.0 (https://example.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code != 200:
            return None

        data = response.json()
        pages = data["query"]["pages"]
        page = next(iter(pages.values()))

        return page
    except requests.exceptions.ConnectionError:
        print(f'{RED}Fehler: Keine Verbindung zu Wikipedia möglich{END}')
        return None
    except requests.exceptions.Timeout:
        print(f'{RED}Fehler: Wikipedia-Anfrage hat zu lange gedauert (Timeout){END}')
        return None
    except requests.exceptions.HTTPError as e:
        print(f'{YELLOW}Warnung: Wikipedia-Server-Fehler: {e}{END}')
        return None
    except requests.exceptions.RequestException as e:
        print(f'{YELLOW}Warnung: Wikipedia-Anfrage fehlgeschlagen: {e}{END}')
        return None
    except Exception as e:
        print(f'{YELLOW}Warnung: Fehler beim Verarbeiten der Wikipedia-Daten: {e}{END}')
        return None


def analyze_wikipedia_page(page, term_original):
    """
    Analysiert eine Wikipedia-Seite und erstellt das Ergebnis-Dictionary.
    """
    term_normalized = term_original.replace(" ", "_")

    # Kategorien extrahieren
    categories = []
    if "categories" in page:
        categories = [cat["title"].replace("Kategorie: ", "")
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
            "extract": page["extract"][:500] + "..." if len(page["extract"])
                                                        > 500 else page["extract"],
            "type": detected_type,
            "categories_detected": {
                "is_city": is_city,
                "is_country": is_country,
                "is_river": is_river
            },
            "categories": categories[:10]
        },
        "validation": {
            "Stadt": is_city,
            "Land": is_country,
            "Fluss": is_river
        }
    }

    return result


def getresult_for_wikipedia_term(term, expected_type=None):
    """
    Analysiert einen Begriff und kategorisiert ihn als Stadt, Land oder Fluss.
    Mit automatischer Disambiguierung für mehrdeutige Begriffe.

    Args:
        term: Der zu suchende Begriff
        expected_type: Optional - erwartet "stadt", "land" oder "fluss"
                      für intelligentere Disambiguierung

    Beispiel:
        - "Frankfurt" wird automatisch zu "Frankfurt am Main" aufgelöst
        - "Paris" wird automatisch zu "Paris (Frankreich)" aufgelöst
        - "Fulda" mit type="fluss" findet "Fulda (Fluss)"
    """
    term_original = term.strip()
    term_normalized = term_original.replace(" ", "_")

    # Erste Seite abrufen
    page = get_wikipedia_page_data(term_normalized)

    if page is None:
        return create_not_found_result(term_original)

    # Prüfen ob Seite existiert
    if "missing" in page or "extract" not in page:
        return create_not_found_result(term_original)

    # Prüfen ob es eine Begriffsklärungsseite ist
    if is_disambiguation_page(page):
        print(f'{YELLOW}"{term_original}" ist mehrdeutig. Suche nach passender Alternative...{END}')

        # Kandidaten holen
        candidates = get_disambiguation_candidates(term)

        if not candidates:
            return create_not_found_result(term_original)

        # Jeden Kandidaten durchprobieren
        for candidate in candidates:
            candidate_lower = candidate.lower()
            term_lower = term_original.lower()

            # 🔒 Schutz vor falschen Treffern wie "Polen"
            if not (
                    candidate_lower == term_lower
                    or candidate_lower.startswith(term_lower + " ")
                    or candidate_lower.startswith(term_lower + " (")
            ):
                continue

            candidate_page = get_wikipedia_page_data(candidate.replace(" ", "_"))

            if candidate_page and "extract" in candidate_page and "missing" not in candidate_page:
                # Prüfen ob es wieder eine Disambiguierungsseite ist
                if is_disambiguation_page(candidate_page):
                    continue

                # Ergebnis analysieren
                result = analyze_wikipedia_page(candidate_page, term_original)

                # Wenn ein erwarteter Typ angegeben wurde, nur passende zurückgeben
                if expected_type:
                    type_map = {
                        "stadt": result["validation"]["Stadt"],
                        "land": result["validation"]["Land"],
                        "fluss": result["validation"]["Fluss"]
                    }

                    if type_map.get(expected_type.lower(), False):
                        print(f'{GREEN}Gefunden: "{result["wikipedia"]["title"]}"{END}')
                        return result
                # Ohne erwarteten Typ: Ersten gültigen Typ zurückgeben
                elif result["wikipedia"]["type"] is not None:
                    print(
                        f'{GREEN}Gefunden: "{result["wikipedia"]["title"]}" '
                        f'(Typ: {result["wikipedia"]["type"]}){END}')
                    return result

        # Kein passender Kandidat gefunden
        print(f'{RED}Keine passende Alternative für "{term_original}" gefunden{END}')
        return create_not_found_result(term_original)

    # Normale Seite gefunden - analysieren
    result = analyze_wikipedia_page(page, term_original)

    # NEUE LOGIK: Wenn expected_type gegeben ist, prüfen ob Typ übereinstimmt
    if expected_type:
        type_map = {
            "stadt": result["validation"]["Stadt"],
            "land": result["validation"]["Land"],
            "fluss": result["validation"]["Fluss"]
        }

        # Wenn der gefundene Artikel NICHT zum erwarteten Typ passt
        if not type_map.get(expected_type.lower(), False):
            if settings.logging:
                print(f'{YELLOW}"{term_original}" passt nicht zum Typ "{expected_type}". '
                      f'Suche nach Varianten...{END}')

            # Versuche Typ-spezifische Varianten (z.B. "Fulda (Fluss)")
            variants = get_term_variants_by_type(term_original, expected_type)

            # Erste Variante überspringen (das ist der Original-Begriff, den wir schon haben)
            for variant in variants[1:]:
                variant_page = get_wikipedia_page_data(variant.replace(" ", "_"))

                if variant_page and "extract" in variant_page and "missing" not in variant_page:
                    variant_result = analyze_wikipedia_page(variant_page, term_original)

                    # Prüfen ob diese Variante zum Typ passt
                    variant_type_map = {
                        "stadt": variant_result["validation"]["Stadt"],
                        "land": variant_result["validation"]["Land"],
                        "fluss": variant_result["validation"]["Fluss"]
                    }

                    if variant_type_map.get(expected_type.lower(), False):
                        print(f'{GREEN}Gefunden: "{variant_result["wikipedia"]["title"]}" (über Suffix-Suche){END}')
                        return variant_result

            # Keine passende Variante gefunden
            if settings.logging:
                print(f'{RED}Keine passende "{expected_type}"-Variante für "{term_original}" gefunden{END}')
            return create_not_found_result(term_original)

    # Typ passt oder kein expected_type angegeben
    return result


def normalize_term(term: str) -> str:
    """
    Normalisiert Benutzereingaben für Wikipedia:
    - Entfernt Leerzeichen
    - Korrigiert Groß-/Kleinschreibung
    """
    return term.strip().title()


# --- check_answer zuletzt, nachdem alle Hilfsfunktionen existieren ---
def check_answer(value, question_type, current_character):
    """
    Prüft:
    - Beginnt das Wort mit dem richtigen Buchstaben
    - Existiert es auf Wikipedia
    - Ist der Typ korrekt (stadt/land/fluss)

    Bei Netzwerkfehlern gibt die Funktion False zurück und zeigt eine Fehlermeldung.
    """
    # ist etwas eingegeben?
    value = normalize_term(value)
    if not value:
        print(f'{RED}"{question_type.capitalize()}"{END} hat keine Eingabe!')
        return False

    # ist der erste buchstabe gleich dem aktuellen buchstaben
    if current_character.lower() != value[0].lower():
        print(
            f"Das ist nicht der Anfangsbuchstabe, der benötigt wird. Das Wort sollte mit {RED}{current_character}{END} beginnen.")
        return False

    # gibt es einen wikipedia eintrag, zu der aktuellen eingabe
    if not if_exists_in_wiki(value):
        print("Es gibt keinen passenden Wikipedia Eintrag")
        return False

    # Typ an getresult übergeben für bessere Disambiguierung
    result = getresult_for_wikipedia_term(value, expected_type=question_type)

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
