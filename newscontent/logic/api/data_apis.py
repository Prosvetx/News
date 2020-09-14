import asyncio
import json
import aiohttp
import json
from random import randint
from datetime import datetime
from news.settings import BASE_DIR

data_rates = str(BASE_DIR) + '/newscontent/logic/api/data_files/data_rates.json'
data_weather = str(BASE_DIR) + '/newscontent/logic/api/data_files/data_weather.json'
weather_token = '6e9178666ae50697fbfd35c5aa83d8f6'
cities = [
    "Delhi",
    "Manila",
    "Seoul-Incheon",
    "Shanghai",
    "Karachi",
    "Beijing",
    "New York",
    "Guangzhou-Foshan",
    "Mexico City",
    "Osaka-Kobe-Kyoto",
    "Moscow",
    "Los Angeles",
    "Astrakhan"
]
async def start(url):
    """Асинхронный запрос  на получение данных по  ссылке API"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            return json.loads(data)


def api_weather():
    """Создание async loop с формированием списка корутин, получение результата
    Фильтр сырых json's (result) с последующим созданием/перезаписыванием json с чистыми данными"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    corutines = [start(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric')
                 for city
                 in cities]
    result = loop.run_until_complete(asyncio.gather(*corutines))
    data = {}
    for i in result:
        if i['cod'] == 200:
            data.update({i['name']: i['main']['temp']})
    with open(data_weather, 'w') as data_file:
        data_file.write(json.dumps(data))



def api_rates():
    """Получение данных о погоде, валюте с помощью OWM API и SBERBANK API в асинхронном потоке"""
    valutes = ['USD', 'EUR', 'CNY']
    data = {}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(start('https://www.cbr-xml-daily.ru/daily_json.js'))
    for valute in valutes:
        data.update({valute: round(res['Valute'][valute]['Value'],2)})
    with open(data_rates, 'w') as data_file:
        data_file.write(json.dumps(data))





api_rates()
api_weather()