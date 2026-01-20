import requests, json

from http.client import responses

question_types = ["city", "country", "lake"]

def check_answer(value, question_type):
    if question_type == "city" and value == TEST_DATA[0]:
        return True
    if question_type == "country" and value == TEST_DATA[1]:
        return True
    if question_type == "lake" and value == TEST_DATA[2]:
        return True
    return False

TEST_DATA = ["Stuttgart", "Spanien", "Seine"]

def if_exists_in_wiki(term):
    url = "https://de.wikipedia.org/w/api.php"
    parameter = {
        "action": "opensearch",
        "search": term,
        "limit": 1,
        "format": "json"
    }
    response = requests.get(url, params= parameter)
    data = response.json()
    return len(data[1]) > 0

def get_wikipedia_summary(term):
    url = f"https://de.wikipedia.org/api/rest_v1/page/summary/{term}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None




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