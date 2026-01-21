import wiki

# ===== KORRIGIERTE TESTS =====
# Änderung 1: 'self' entfernt aus allen drei Funktionen
# Änderung 2: Deutsche Namen statt englischer

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
    # Geändert: "Zimbabwe" → "Simbabwe" (deutsche Wikipedia)
    assert wiki.check_answer("Simbabwe", "land", "s") == True, "Simbabwe ist kein Land"


def test_Zambezi_als_Fluss():
    # Geändert: "Zambezi" → "Sambesi" (deutsche Wikipedia)
    assert wiki.check_answer("Sambesi", "fluss", "s") == True, "Sambesi ist kein Fluss"


def test_Yerevan_als_Stadt():
    # Geändert: "Yerevan" → "Eriwan" (deutsche Wikipedia)
    assert wiki.check_answer("Eriwan", "stadt", "e") == True, "Eriwan ist keine Stadt"


def test_Yémen_als_Land():
    # Geändert: "Yémen" → "Jemen" (deutsche Wikipedia)
    assert wiki.check_answer("Jemen", "land", "j") == True, "Jemen ist kein Land"