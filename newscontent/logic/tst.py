from news.settings import BASE_DIR
import json
from random import choice

# print(BASE_DIR)
with open(str(BASE_DIR) + '/newscontent/logic/api/data_files/data_weather.json', 'r') as file:
    cities = dict(json.loads(file.read()))
    city = choice(list(cities.keys()))
    temp = cities[city]
