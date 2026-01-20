import wikipedia
import requests

wikipedia.set_lang("de")

question_types = ["stadt", "land", "fluss"]


def check_answer(value, question_type, current_character):
    # ist der erste buchstabe gleich dem aktuellen buchstaben
    if current_character.lower() != value[0].lower():
        return False
    # gibt es einen wikipedia eintrag, zu der aktuellen eingabe
    if not if_exists_in_wiki(value):
        return False
    summary = get_wikipedia_summary(value)
    # wenn question_type nicht in der summary, dann return false


    return True


TEST_DATA = ["Stuttgart", "Spanien", "Seine"]


def get_wikipedia_summary(term):
    term = term.strip().replace(" ", "_")

    url = "https://de.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "titles": term,
        "format": "json"
    }

    headers = {
        "User-Agent": "StadtLandFlussGame/1.0 (https://example.com)"
    }

    response = requests.get(url, params=params, headers=headers)

    print("Status:", response.status_code)  # debug

    if response.status_code != 200:
        return None

    data = response.json()
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))

    if "extract" in page:
        return {"extract": page["extract"]}

    return None


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

    print("Status:", response.status_code)
    print("URL:", response.url)
    print("Text:", response.text[:200])

    response.raise_for_status()  # wirft Fehler, falls HTTP-Fehler
    data = response.json()
    return bool(data[1])


"""
def category_detection(summary):
    if summary is None:
        return {"is_city": False, "is_country": False, "is_river": False}

    text = summary.get("extract", "").lower()
    return {"is_city": False, "is_country": False, "is_river": False}
"""

#print(if_exists_in_wikipedia("Berlin"))  # → True
"""
{
  "term": "Berlin",
  "wikipedia": {
    "found": true,
    "api_url": "https://de.wikipedia.org/api/rest_v1/page/summary/Berlin",
    "title": "Berlin",
    "description": "Capital and largest city of Germany",
    "extract": "Berlin is the capital and largest city of Germany by both area and population...",
    "type": "city",
    "categories_detected": {
      "is_city": true,
      "is_country": false,
      "is_river": false
    }
  },
  "validation": {
    "Stadt": true,
    "Land": false,
    "Fluss": false
  }
}
{

}
"""
