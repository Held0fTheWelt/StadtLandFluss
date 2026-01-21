import pytest
import wiki
import pytest
import wiki
import backend


def test_Berlin():
    """Testet Berlin als Stadt."""
    assert wiki.check_answer("Berlin", "stadt", "b") == True, "Diese Stadt existiert nicht"


def test_Fulda():
    """Testet Fulda als Stadt und Fluss (Disambiguierung)."""
    assert wiki.check_answer("Fulda", "stadt", "f") == True, "Diese Stadt existiert nicht"
    assert wiki.check_answer("Fulda", "fluss", "f") == True, "Dieser Fluss existiert nicht"


def test_Frankfurt():
    """Testet Frankfurt als Stadt mit Wikipedia-Existenzprüfung."""
    assert wiki.if_exists_in_wiki("Frankfurt") == True, "Diese Seite existiert nicht bei Wikipedia"
    assert wiki.check_answer("Frankfurt", "stadt", "f") == True, "Diese Stadt existiert nicht"


def test_Hamburg():
    """Testet Hamburg als Stadt."""
    assert wiki.check_answer("Hamburg", "stadt", "h") == True, "Diese Stadt existiert nicht"


def test_Donau():
    """Testet Donau als Fluss."""
    assert wiki.check_answer("Donau", "fluss", "d") == True, "Dieser Fluss existiert nicht"


def test_Stadt_Richtig_Aber_Buchstabe_Falsch():
    """Testet dass der Anfangsbuchstabe korrekt geprüft wird."""
    assert wiki.check_answer("Hamburg", "stadt", "g") == False, "Der Buchstabe wird nicht richtig geprüft"


def test_all_caps_answers():
    """Testet Groß-/Kleinschreibung: Antworten in GROSSBUCHSTABEN."""
    assert wiki.check_answer("PASSAU", "stadt", "p") == True, "All-Caps wird nicht akzeptiert"


def test_no_caps_answers():
    """Testet Groß-/Kleinschreibung: Antworten in kleinbuchstaben."""
    assert wiki.check_answer("passau", "stadt", "p") == True, "Kleinschreibung wird nicht akzeptiert"


def test_Schweden_als_Stadt():
    """Testet dass Schweden nicht als Stadt erkannt wird."""
    assert wiki.check_answer("Schweden", "stadt", "s") == False, "Schweden ist keine Stadt"


def test_Stuttgart_als_Land():
    """Testet dass Stuttgart nicht als Land erkannt wird."""
    assert wiki.check_answer("Stuttgart", "land", "s") == False, "Stuttgart ist kein Land"


def test_Po_als_Land():
    """Testet dass Po nicht als Land erkannt wird."""
    assert wiki.check_answer("Po", "land", "p") == False, "Po ist ein Land"


def test_Po_als_Fluss():
    """Testet Po als Fluss (italienischer Fluss)."""
    assert wiki.check_answer("Po", "fluss", "p") == True, "Po ist kein Fluss"


def test_Franken_als_Land():
    """Testet dass Franken nicht als Land erkannt wird."""
    assert wiki.check_answer("Franken", "land", "f") == False, "Franken ist ein Land"


def test_Ekbatana_als_Stadt():
    """Testet Ekbatana als historische Stadt."""
    assert wiki.check_answer("Ekbatana", "stadt", "e") == True, "Ekbatana ist keine Stadt"


def test_hyphenated_names():
    """Testet Stadt mit Bindestrich im Namen."""
    assert wiki.check_answer("Villingen-Schwenningen", "stadt", "v") == True, "Villingen-Schwenningen ist keine Stadt"


def test_Luxemburg_as_country():
    """Testet Luxemburg als Land (Disambiguierung)."""
    assert wiki.check_answer("Luxemburg", "land", "l") == True, "Luxemburg ist kein Land"


def test_Luxemburg_as_city():
    """Testet Luxemburg als Stadt (Disambiguierung)."""
    assert wiki.check_answer("Luxemburg", "stadt", "l") == True, "Luxemburg ist keine Stadt"


def test_Zamosc_als_Stadt():
    """Testet falsche Schreibweise ohne diakritische Zeichen."""
    assert wiki.check_answer("Zamosc", "stadt", "z") == False, "Zamosc ist eine Stadt"


def test_Zamość_als_Stadt():
    """Testet korrekte polnische Schreibweise mit Akzent."""
    assert wiki.check_answer("Zamość", "stadt", "z") == True, "Zamość ist keine Stadt"


def test_El_Paso_als_Stadt():
    """Testet Stadt mit Leerzeichen im Namen."""
    assert wiki.check_answer("El Paso", "stadt", "e") == True, "El Paso ist keine Stadt"


def test_Simbabwe_als_Land():
    """Testet deutsche Schreibweise von Zimbabwe."""
    assert wiki.check_answer("Simbabwe", "land", "s") == True, "Simbabwe ist kein Land"


def test_Sambesi_als_Fluss():
    """Testet deutsche Schreibweise von Zambezi."""
    assert wiki.check_answer("Sambesi", "fluss", "s") == True, "Sambesi ist kein Fluss"


def test_Jerewan_als_Stadt():
    """Testet deutsche Schreibweise von Yerevan."""
    assert wiki.check_answer("Jerewan", "stadt", "j") == True, "Jerewan ist keine Stadt"


def test_Jemen_als_Land():
    """Testet deutsche Schreibweise von Yémen."""
    assert wiki.check_answer("Jemen", "land", "j") == True, "Jemen ist kein Land"


def test_UlanBator_als_Stadt():
    """Testet Ulan Bator als Stadt (Hauptstadt der Mongolei)."""
    assert wiki.check_answer("Ulan Bator", "stadt", "u") == True, "Ulan Bator ist keine Stadt"


def test_Dschibuti_als_Land():
    """Testet deutsche Schreibweise von Djibouti."""
    assert wiki.check_answer("Dschibuti", "land", "d") == True, "Dschibuti ist kein Land"


def test_Xingu_als_Fluss():
    """Testet Xingu als Fluss (brasilianischer Fluss)."""
    assert wiki.check_answer("Xingu", "fluss", "x") == True, "Xingu ist kein Fluss"

def test_Vatican_als_Stadt():
    assert wiki.check_answer("Vatican", "land", "v") == True, "Vatican ist kein Land"

def test_Volga_als_Fluss():
    assert wiki.check_answer("Volga", "fluss", "v") == True, "Volga ist kein Fluss"






pytest.main()