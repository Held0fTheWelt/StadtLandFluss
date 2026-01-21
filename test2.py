import pytest
import wiki

def test_El_Paso_als_Stadt():
    assert wiki.check_answer("El Paso", "stadt", "e") == True, "El Paso ist keine Stadt"

def test_Zimbabwe_als_Land():
    assert wiki.check_answer("Zimbabwe", "land", "z") == True, "Zimbabwe ist kein Land"

def test_Zambezi_als_Fluss():
    assert wiki.check_answer("Zambezi", "fluss", "z") == True, "Zambezi ist kein Land"

def test_Yerevan_als_Stadt():
    assert wiki.check_answer("Yerevan", "stadt", "y") == True, "Yerevan ist kein Land"

def test_Yémen_als_Land():
    assert wiki.check_answer("Yémen", "land", "y") == True, "Yerevan ist kein Land"

def test_UlanBator_als_Stadt:
    assert wiki.check_answer("Ulan Bator", "stadt", "u") == True, "Ulan Bator ist keine Stadt"
pytest.main()