import wikipedia
wikipedia.set_lang("de")

question_types = ["city", "country", "lake"]

def check_answer(value, question_type, current_character):
    if question_type == "city" and value == TEST_DATA[0]:
        return True
    if question_type == "country" and value == TEST_DATA[1]:
        return True
    if question_type == "lake" and value == TEST_DATA[2]:
        return True
    return False

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
    response = requests.get(url, params=parameter)

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
"""