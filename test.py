import wiki
import backend

def test_cities():
    assert wiki.check_answer("Berlin", "stadt", "b") == True, "Diese Stadt existiert nicht"
    assert wiki.check_answer("Fulda", "stadt", "f") == True, "Diese Stadt existiert nicht"
    assert wiki.check_answer("Fulda", "fluss", "f") == True, "Dieser Fluss existiert nicht"
    assert wiki.if_exists_in_wiki("Frankfurt") == True, "Diese Seite existiert nicht bei Wikipedia"
    assert wiki.check_answer("Frankfurt", "stadt", "f") == True, "Diese Stadt existiert nicht"
    assert wiki.check_answer("Hamburg", "stadt", "h") == True, "Dieser Fluss existiert nicht"


if __name__ == "__main__":
    test_cities()