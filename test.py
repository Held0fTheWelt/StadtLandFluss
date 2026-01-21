import pytest
import wiki
import backend

def test_Berlin():
    """
    Berlin als Eingabe für Stadt
    """
    assert wiki.check_answer("Berlin", "stadt", "b") == True, "Diese Stadt existiert nicht"

def test_Fulda():
    """
    Fulda als Eingabe für Stadt
    """
    assert wiki.check_answer("Fulda", "stadt", "f") == True, "Diese Stadt existiert nicht"
    assert wiki.check_answer("Fulda", "fluss", "f") == True, "Dieser Fluss existiert nicht"

def test_Frankfurt():
    """
    Frankfurt als Eingabe für Stadt
    """
    assert wiki.if_exists_in_wiki("Frankfurt") == True, "Diese Seite existiert nicht bei Wikipedia"
    assert wiki.check_answer("Frankfurt", "stadt", "f") == True, "Diese Stadt existiert nicht"

def test_Hamburg():
    """
    Hamburg als Eingabe für Stadt
    """
    assert wiki.check_answer("Hamburg", "stadt", "h") == True, "Diese Stadt existiert nicht"

def test_Donai():
    """
    Donai als Eingabe für Stadt
    """
    assert wiki.check_answer("Donai", "stadt", "d") == True, "Diese Stadt existiert nicht"

def test_Stadt_Richtig_Aber_Buchstabe_Falsch():
    """
    Prüft, ob Buchstabe zur Eingabe als Anfangsbuchstabe passt
    """
    assert wiki.check_answer("Hamburg", "stadt", "g") == False, "Der Buchstabe wird nicht richtig geprüft"


def test_all_caps_answers():
    """
    All caps antworten klappen nicht
    """
    assert wiki.check_answer("PASSAU", "stadt", "p") == True, "Der Buchstabe wird nicht richtig geprüft"

def test_no_caps_answers():
    assert wiki.check_answer("passau", "stadt", "p") == True, "Der Buchstabe wird nicht richtig geprüft"

def test_Schweden_als_Stadt():
    assert wiki.check_answer("Schweden", "stadt", "s") == False, "Schweden ist keine Stadt"

def test_Stuttgart_als_Land():
    assert wiki.check_answer("Stuttgart", "land", "s") == False, "Schweden ist keine Stadt"

def test_Po_als_Land():
    assert wiki.check_answer("Po", "land", "p") == False, "Po ist ein Land"

def test_Po_als_Fluss():
    assert wiki.check_answer("Po", "fluss", "p") == True, "Po ist kein Fluss"

def test_Franken_als_Land():
    assert wiki.check_answer("Franken", "land", "f") == False, "Franken ist ein Land"

def test_Ekbatana_als_Stadt():
    assert wiki.check_answer("Ekbatana", "stadt", "e") == True, "Ekbatana ist keine Stadt"

def test_hyphenated_names():
    """Städte mit Bindestrichen (z.B. Gelsenkirchen-Buer)."""
    assert wiki.check_answer("Villingen-Schwenningen", "stadt", "v") == True, "Villingen-Schwenningen ist keine Stadt"


def test_Luxemburg_as_country():
    """Wenn Stadt und Land gleich heißen (z.B. Luxemburg, Mexiko)."""
    # Luxemburg als Land
    assert wiki.check_answer("Luxemburg", "land", "l") == True, "Luxemburg ist kein Land"

def test_Luxemburg_as_city():
    # Luxemburg als Stadt
    assert wiki.check_answer("Luxemburg", "stadt", "l") == True, "Luxemburg ist keine Stadt"

def test_Zamosc_als_Stadt():
    assert wiki.check_answer("Zamosc", "stadt", "z") == False, "Zamosc ist eine Stadt"

def test_Zamość_als_Stadt():
    assert wiki.check_answer("Zamość", "stadt", "z") == True, "Zamość ist keine Stadt"

def test_El_Paso_als_Stadt():
    assert wiki.check_answer("El Paso", "stadt", "e") == True, "El Paso ist keine Stadt"

def test_Zimbabwe_als_Land():
    assert wiki.check_answer("Zimbabwe", "land", "z") == True, "Zimbabwe ist kein Land"

def test_Zambezi_als_Fluss():
    assert wiki.check_answer("Zambezi", "fluss", "z") == True, "Zambezi ist kein Land"

def test_Jerevan_als_Stadt():
    assert wiki.check_answer("Jerevan", "stadt", "j") == True, "Yerevan ist kein Land"

def test_Yémen_als_Land():
    assert wiki.check_answer("Yémen", "land", "y") == True, "Yémen ist kein Land"

pytest.main()

