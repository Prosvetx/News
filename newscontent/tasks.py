import asyncio
import json

import requests
from news.celery import app
from news.settings import BASE_DIR
from .logic.api.data_apis import start, cities, weather_token
from .models import Rate

data_rates = str(BASE_DIR) + '/newscontent/logic/api/data_files/data_rates.json'
data_weather = str(BASE_DIR) + '/newscontent/logic/api/data_files/data_weather.json'


@app.task
def api_rates():
    """Получение данных о погоде, валюте с помощью OWM API и SBERBANK API в асинхронном потоке"""
    valutes = ['USD', 'EUR', 'CNY']
    data = {}
    res = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    for valute in valutes:
        data.update({valute: round(res['Valute'][valute]['Value'], 2)})
    with open(data_rates, 'w') as data_file:
        data_file.write(json.dumps(data))
        print('Rates updated')


@app.task
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
    print('Weather updated')


@app.task(autostart=False)
def update_rates():
    url_sberbank = 'https://www.cbr-xml-daily.ru/daily_json.js'
    res = requests.get(url_sberbank)
    if res.status_code == 200:
        res = res.json()
        data = res['Valute']
        for valute in data:
            Rate.objects.update_or_create(valute=valute, defaults={'value_rur': round(data[valute]['Value'], 2),
                                                                   'valute_name': data[valute]['Name']})
    else:
        print('update_rates / failed')
    print('rates updated!')

# celery -A news worker -B
# celery -A news beat
