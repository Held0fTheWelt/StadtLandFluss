
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



"""

import requests
def if_exists_in_wiki(term):
    url = "https://en.wikipedia.org/w/api.php"
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
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{term}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


"""