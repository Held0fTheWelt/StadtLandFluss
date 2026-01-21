import pytest
import wiki
import backend

def test_Berlin():
    """ Berlin als Eingabe für Stadt"""
    assert wiki.check_answer("Berlin", "stadt", "b") == True, "Diese Stadt existiert nicht"

def test_Fulda():
    assert wiki.check_answer("Fulda", "stadt", "f") == True, "Diese Stadt existiert nicht"
    assert wiki.check_answer("Fulda", "fluss", "f") == True, "Dieser Fluss existiert nicht"

def test_Frankfurt():
    assert wiki.if_exists_in_wiki("Frankfurt") == True, "Diese Seite existiert nicht bei Wikipedia"
    assert wiki.check_answer("Frankfurt", "stadt", "f") == True, "Diese Stadt existiert nicht"

def test_Hamburg():
    assert wiki.check_answer("Hamburg", "stadt", "h") == True, "Diese Stadt existiert nicht"

def test_Stadt_Richtig_Aber_Buchstabe_Falsch():
    assert wiki.check_answer("Hamburg", "stadt", "g") == False, "Der Buchstabe wird nicht richtig geprüft"



pytest.main()