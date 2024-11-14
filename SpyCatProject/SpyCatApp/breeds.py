import requests

"""Getting the list of breeds from cats API"""


def get_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        data = []
    return [item.get('name') for item in data]
